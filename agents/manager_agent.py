import openai
import json
from .executor_agent import ExecutorAgent
from tasks.meta_task import MetaTask
from utils.graph import GraphOptimizer

# Remove unnecessary imports
# import os
# from memory.persistence import PersistenceManager

class ManagerAgent:
    def __init__(self, executor_agents, memory, supervisor):
        self.executor_agents = executor_agents
        self.memory = memory
        self.supervisor = supervisor

    def assign_tasks(self, meta_tasks):
        unassigned_tasks = [task for task in meta_tasks if not task.is_completed()]
        
        while unassigned_tasks:
            for task in unassigned_tasks:
                bids = []
                for agent in self.executor_agents:
                    if set(task.tools).issubset(agent.tools):
                        bid_value = self.calculate_bid(agent, task)
                        bids.append((agent, bid_value))
                
                if bids:
                    selected_agent = max(bids, key=lambda x: x[1])[0]
                    selected_agent.execute_task(task)
                    if task.is_completed():
                        unassigned_tasks.remove(task)

    def calculate_bid(self, agent, task: MetaTask) -> float:
        workload_factor = 1.0 / (len(agent.current_tasks) + 1)
        expertise_factor = agent.get_expertise_score(task.tools)
        complexity_factor = 1.0 / (task.get_complexity() + 1)  
        return workload_factor * expertise_factor * complexity_factor

    def decompose_task(self, main_task):
        decomposition_prompt = f"""
        Decompose the following task into sub-tasks. Specify the tools needed for each sub-task and their dependencies.

        Task: {main_task.description}
        Context: {main_task.context}

        Output format: 
        ```json
        [
            {{ "description": "...", "tools": [...], "dependencies": [...], "input_data": {{...}}, "complexity": 1.0 }},
            // ...
        ]
        ```
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": decomposition_prompt}
                ],
                max_tokens=300,
                n=1,
                stop=None,
                temperature=0.5,
            )
            decomposition_plan = json.loads(response.choices[0].message.content)
            meta_tasks = self.build_meta_tasks(decomposition_plan)
            return GraphOptimizer().optimize(meta_tasks)

        except Exception as e:
            print(f"Error with LLM: {str(e)}")
            return []

    def build_meta_tasks(self, decomposition_plan):
        return [MetaTask(**task) for task in decomposition_plan]

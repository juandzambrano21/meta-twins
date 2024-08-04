# executor_agent.py

from tools.tool_factory import ToolFactory
from memory.contextual_memory import ContextualMemory
from tasks.meta_task import MetaTask
import openai
import os 
from dotenv import load_dotenv
from utils.logger import logger

# agents/executor_agent.py

# agents/executor_agent.py

class ExecutorAgent:
    def __init__(self, name, tools, memory: ContextualMemory):
        self.name = name
        self.tools = tools
        self.memory = memory
        self.current_tasks = []
        self.past_performance = {}

    def execute_task(self, task: MetaTask):
        if task.is_completed():
            logger.info(f"[{self.name}] Task already completed: {task.description}")
            return

        context = self.memory.build_context_for_task(task.description, task.context)
        logger.info(f"[{self.name}] Executing task: {task.description} with context: {context}")


        task.status = 'in_progress'  # Update status to in_progress

        for tool_name in task.tools:
            tool = ToolFactory().create_tool(tool_name)
            if tool:
                try:
                    result = tool.run(task.input_data)
                    validated_result = self.validate_result(task, result)
                    task.set_result(validated_result)
                    logger.info(f"[{self.name}] Executed task: {task.description} with result: {validated_result}")
                except Exception as e:
                    logger.error(f"[{self.name}] Error executing tool {tool_name} for task {task.description}: {str(e)}")
                    task.set_result(f"Failed to execute task: {str(e)}")
            else:
                logger.warning(f"[{self.name}] Tool {tool_name} not available for task {task.description}")
                task.set_result(f"Tool {tool_name} not available")
        
        self.learn_from_experience(task)

    def validate_result(self, task: MetaTask, result):
        validation_prompt = f"""
        Validate the following result based on the task description and context:

        Task: {task.description}
        Context: {task.context}
        Result: {result}

        Provide validation feedback and suggest improvements if necessary.
        """
        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": validation_prompt}
                ],
                max_tokens=300,
                n=1,
                stop=None,
                temperature=0.5,
            )
            validation_feedback = response.choices[0].message.content
            logger.info(f"Validation Feedback: {validation_feedback}")
            
            # Adjust result based on feedback
            if "improvements" in validation_feedback:
                # Example of processing feedback to adjust the result
                result = f"Improved Result: {result}"

            return result

        except openai.error.OpenAIError as e:
            logger.error(f"Error with LLM validation: {str(e)}")
            return result


    def learn_from_experience(self, task: MetaTask):
        self.memory.stm.save(task.description, {"result": task.result})
        if task.description not in self.past_performance:
            self.past_performance[task.description] = 0
        self.past_performance[task.description] += 1

    def get_expertise_score(self, tools):
        expertise = len([tool for tool in tools if tool in self.tools])
        return expertise / len(tools) if tools else 0

    def retrieve_context(self, task):
        return self.memory.build_context_for_task(task.description, task.context)

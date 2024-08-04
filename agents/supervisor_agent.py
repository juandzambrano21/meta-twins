# supervisor_agent.py

import openai
import os 

class SupervisorAgent:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def refine_task(self, task, neighboring_task_results):
        task_context = self.summarize_neighboring_results(neighboring_task_results)
        refined_context = self.refine_with_llm(task, task_context)
        task.set_context(refined_context)
        print(f"Refined task: {task.description} with context: {refined_context}")

    def summarize_neighboring_results(self, neighboring_task_results):
        summary = " ".join([result['summary'] for result in neighboring_task_results])
        return summary

    def refine_with_llm(self, task, context):
        refinement_prompt = f"""
        Refine the context for the following task based on previous results and context:

        Task: {task.description}
        Context: {context}

        Provide refined insights and suggestions.
        """
        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                  messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": refinement_prompt}
                    ],
                max_tokens=150,
                n=1,
                stop=None,
                temperature=0.5,
            )
            refined_insights = response.choices[0].message.content
            return refined_insights

        except Exception as e:
            print(f"Error with LLM refinement: {str(e)}")
            return context

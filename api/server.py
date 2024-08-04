# api/server.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

from agents.manager_agent import ManagerAgent
from agents.executor_agent import ExecutorAgent
from agents.supervisor_agent import SupervisorAgent
from workflows.meta_task import MetaTaskWorkflow
from tasks.meta_task import MetaTask
from tools.tool_factory import ToolFactory
from memory.embeddings import EmbeddingModel

from utils.logger import logger

# Import MemGPT
from memory.memgpt import MemGPT

# FastAPI app initialization
app = FastAPI()

# Define request and response models
class AgentConfig(BaseModel):
    name: str
    tools: List[str]

class InitializationRequest(BaseModel):
    personas: Dict[str, str]
    agent_configs: List[AgentConfig]

class Task(BaseModel):
    description: str
    tools: List[str]
    dependencies: List[str] = []
    input_data: Dict[str, Any] = {}
    complexity: float = 1.0
    context: str = ""

class WorkflowResponse(BaseModel):
    status: str
    results: Dict[str, Any] = {}

class ToolDiscoveryRequest(BaseModel):
    task_description: str

class ToolDiscoveryResponse(BaseModel):
    suggested_tools: List[str]

# Initialize global variables to store agent instances
executor_agents = []
manager_agent = None
supervisor_agent = SupervisorAgent()
memgpt_instance = None  # Use MemGPT for memory management

# Initialize System Endpoint
@app.post("/initialize_system", response_model=dict)
async def initialize_system(request: InitializationRequest):
    try:
        global memgpt_instance

        # Initialize MemGPT
        persona = request.personas.get("persona", "")
        human = request.personas.get("human", "")
        embedding_model = EmbeddingModel()

        # Initialize MemGPT instance
        memgpt_instance = MemGPT(persona, human, embedding_model)

        # Initialize Agents
        global executor_agents, manager_agent
        executor_agents = [
            ExecutorAgent(name=config.name, tools=config.tools, memory=memgpt_instance.contextual_memory)
            for config in request.agent_configs
        ]

        manager_agent = ManagerAgent(executor_agents=executor_agents, memory=memgpt_instance.contextual_memory, supervisor=supervisor_agent)

        logger.info("System initialized successfully using MemGPT")
        return {"status": "System initialized successfully"}

    except Exception as e:
        logger.error(f"Error initializing system: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Execute Meta-Task Workflow
@app.post("/execute_meta_task_workflow", response_model=WorkflowResponse)
async def execute_meta_task_workflow(tasks: List[Task]):
    try:
        # Ensure the system is initialized
        if not manager_agent or not executor_agents:
            raise HTTPException(status_code=400, detail="System is not initialized. Please initialize first.")

        # Convert input tasks to MetaTask objects
        meta_tasks = [
            MetaTask(
                description=task.description,
                tools=task.tools,
                dependencies=task.dependencies,
                input_data=task.input_data,
                complexity=task.complexity,
                context=task.context
            )
            for task in tasks
        ]

        # Initialize and execute workflow
        workflow = MetaTaskWorkflow(
            tasks=meta_tasks,
            manager_agent=manager_agent,
            executor_agents=executor_agents,
            supervisor_agent=supervisor_agent
        )
        results = workflow.execute()

        # Save memory state after task execution
        memgpt_instance.save_all_memories()

        logger.info("Meta-Task Workflow executed successfully")
        return {"status": "Meta-Task Workflow executed successfully", "results": results}

    except Exception as e:
        logger.error(f"Error executing workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Discover Tools
@app.post("/discover_tools", response_model=ToolDiscoveryResponse)
async def discover_tools(request: ToolDiscoveryRequest):
    try:
        tool_factory = ToolFactory()
        suggested_tools = tool_factory.discover_tools(request.task_description)
        logger.debug(f"Discovered tools: {suggested_tools}")
        return {"suggested_tools": suggested_tools}
    except Exception as e:
        logger.error(f"Error discovering tools: {e}")
        raise HTTPException(status_code=500, detail=str(e))

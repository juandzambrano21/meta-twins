# graph.py

import networkx as nx
from tasks.meta_task import MetaTask

class GraphOptimizer:
    """Optimizes a graph of tasks, resolving dependencies."""

    def optimize(self, meta_tasks):
        """Organize tasks into an optimal execution order."""
        workflow_graph = nx.DiGraph()

        for task in meta_tasks:
            workflow_graph.add_node(task.description)
            for dependency in task.dependencies:
                workflow_graph.add_edge(dependency, task.description)

        # Topologically sort tasks based on dependencies
        sorted_tasks = list(nx.topological_sort(workflow_graph))
        return [task for task in meta_tasks if task.description in sorted_tasks]

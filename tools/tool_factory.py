# tool_factory.py

from abc import ABC, abstractmethod
from tools.web_scraper_tool import WebScraperTool
from tools.simple_math import SimpleMathTool
from utils.logger import logger 

class Tool(ABC):
    @abstractmethod
    def run(self, input_data):
        pass

    @property
    def description(self) -> str:
        return "Generic Tool"

class FlightSearchTool(Tool):
    def run(self, input_data):
        # Simulate a flight search operation
        destination = input_data.get("destination")
        date = input_data.get("date")
        return f"Searching flights for destination: {destination} on date: {date}"

class HotelSearchTool(Tool):
    def run(self, input_data):
        # Simulate a hotel search operation
        destination = input_data.get("destination")
        date = input_data.get("date")
        return f"Searching hotels in {destination} on date: {date}"

class ToolFactory:
    def __init__(self):
        self.tool_repository = {
            "FlightSearchAPI": FlightSearchTool(),
            "HotelSearchAPI": HotelSearchTool(),
            "WebScraperTool": WebScraperTool(),
            "SimpleMathTool": SimpleMathTool()
        }

    def create_tool(self, tool_name: str):
        return self.tool_repository.get(tool_name, None)

    def discover_tools(self, task_description: str):
        suggested_tools = []
        keywords = task_description.lower().split()
        
        for tool_name in self.tool_repository.keys():
            if any(keyword in tool_name.lower() for keyword in keywords):
                suggested_tools.append(tool_name)
        
        return list(set(suggested_tools))

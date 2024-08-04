# web_scraper_tool.py

import requests
from bs4 import BeautifulSoup
from utils.logger import logger
import logging

class WebScraperTool:
    def __init__(self):
        self.name = "WebScraperTool"
        self.logger = logger

    def run(self, input_data: dict):
        url = input_data.get('url', '')
        try:
            response = requests.get(url)
        
            if response.status_code != 200:
                raise Exception("Failed to fetch the webpage.")
        
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup.title.string  # Return the title of the page
        except Exception as e:
            self.error(f"Error scraping web: {str(e)}")
            return str(e)

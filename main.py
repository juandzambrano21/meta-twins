import uvicorn
from api.server import app  # Import your FastAPI app instance
from utils.logger import logger
import os

def ensure_data_directory_exists():
    # Create the data directory if it does not exist
    os.makedirs("data", exist_ok=True)

if __name__ == "__main__":
    ensure_data_directory_exists()
    
    # Log the application startup
    logger.info("Starting Third Wish IP Meta-Task System")
    
    try:
        # Run the FastAPI server
        uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
    except Exception as e:
        # Log any errors on startup
        logger.error(f"Error starting server: {e}")

import logging
import sys

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Set logging level for some verbose libraries if necessary
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    
    return logging.getLogger("glowup")

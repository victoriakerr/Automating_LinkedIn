import logging

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def log_info(message):
    print(f"[INFO] {message}")
    logging.info(message)

def log_error(message):
    print(f"[ERROR] {message}")
    logging.error(message)
    

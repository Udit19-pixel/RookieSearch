import logging
import psutil
import requests
import schedule
import time

from logging.handlers import RotatingFileHandler
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from email_alerts import send_error_email


# Set up logging
log_file = 'rookiesearch.log'
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
log_handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=5)
log_handler.setFormatter(log_formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

# Initialize FastAPI app
app = FastAPI()

class VectorStore:
    def get_last_update_time(self):
        return datetime.now() - timedelta(days=1)

    def check_data_quality(self):
        return {"malformed_entries": 0, "duplicates": 0}

class ModelEvaluator:
    def evaluate_on_test_set(self):
        return {"accuracy": 0.85, "f1_score": 0.82}

vector_store = VectorStore()
model_evaluator = ModelEvaluator()

# System Health Monitoring
def monitor_system_health():
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
   
    logger.info(f"System Health: CPU {cpu_usage}%, Memory {memory_usage}%, Disk {disk_usage}%")
   
    if cpu_usage > 75 or memory_usage > 75 or disk_usage > 75:
        error_message = f"High resource usage detected! CPU: {cpu_usage}%, Memory: {memory_usage}%, Disk: {disk_usage}%"
        logger.error(error_message)
        send_error_email("High Resource Usage Alert", error_message)

# Data Quality Monitoring
def monitor_data_quality():
    last_update = vector_store.get_last_update_time()
    if datetime.now() - last_update > timedelta(days=7):
        error_message = "Data hasn't been updated in over a week!"
        logger.error(error_message)
        send_error_email("Data Update Alert", error_message)
   
    quality_check = vector_store.check_data_quality()
    if quality_check["malformed_entries"] > 0 or quality_check["duplicates"] > 0:
        error_message = f"Data quality issues detected: {quality_check}"
        logger.error(error_message)
        send_error_email("Data Quality Alert", error_message)

# Model Performance Monitoring
def monitor_model_performance():
    performance = model_evaluator.evaluate_on_test_set()
    logger.info(f"Model Performance: {performance}")
    if performance["accuracy"] < 0.8:
        error_message = f"Model accuracy has dropped below threshold! Current accuracy: {performance['accuracy']}"
        logger.error(error_message)
        send_error_email("Model Performance Alert", error_message)

# Scheduling tasks
schedule.every(5).minutes.do(monitor_system_health)
schedule.every(1).days.do(monitor_data_quality)
schedule.every(1).weeks.do(monitor_model_performance)

def run_scheduled_tasks():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    import threading
    threading_scheduler = threading.Thread(target=run_scheduled_tasks)
    threading_scheduler.start()
    
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
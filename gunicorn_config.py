import logging
from logging.handlers import RotatingFileHandler

# Gunicorn Configuration
bind = "0.0.0.0:8000"
workers = 2
worker_class = "uvicorn.workers.UvicornWorker"

# Log format
log_format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

# Set log level
loglevel = "debug"  # Now logs everything (DEBUG, INFO, WARNING, ERROR)

# Define separate log files
accesslog = "gunicorn_access.log"  # Logs all requests
errorlog = "gunicorn_error.log"  # By default, logs errors & warnings

# Configure error logger to log **everything**
gunicorn_error_logger = logging.getLogger("gunicorn.error")
gunicorn_error_logger.setLevel(logging.DEBUG)  # Capture all logs

# File handler with rotation
log_file_handler = RotatingFileHandler("gunicorn.log", maxBytes=5 * 1024 * 1024, backupCount=3)
log_file_handler.setFormatter(logging.Formatter(log_format))
log_file_handler.setLevel(logging.DEBUG)

# Apply handler to Gunicorn & Uvicorn
gunicorn_error_logger.addHandler(log_file_handler)
uvicorn_logger = logging.getLogger("uvicorn")
uvicorn_logger.addHandler(log_file_handler)
uvicorn_logger.setLevel(logging.DEBUG)
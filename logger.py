import logging
import json
import sys
from datetime import datetime

class StructuredLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)

        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)

        self.logger.addHandler(handler)

    def _log(self, level: str, message: str, **kwargs):
        """Log a structured message"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat()+"Z",
            "level": level.upper(),
            "message": message,
            **kwargs
        }
        self.logger.log(getattr(logging, level.upper()), json.dumps(log_entry))

    def info(self, message: str, **kwargs):
        """Log an info level message"""
        self._log("info", message, **kwargs)

    def error(self, message: str, **kwargs):
        """Log an error level message"""
        self._log("error", message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log a warning level message"""
        self._log("warning", message, **kwargs)
    
    def debug(self, message: str, **kwargs):
        """Log a debug level message"""
        self._log("debug", message, **kwargs)

logger = StructuredLogger(__name__)
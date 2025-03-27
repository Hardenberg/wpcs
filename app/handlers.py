import logging
from .models import LogEntry

logger = logging.getLogger('django')

class DatabaseLogHandler(logging.Handler):
    def emit(self, record):
        try:
            LogEntry.objects.create(
                level=record.levelname,
                message=record.getMessage(),
                module=record.module
            )
        except Exception as e:
            logger.error(f"Error while logging: {e}")

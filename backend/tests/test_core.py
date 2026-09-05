from app.core.settings import settings
from app.core.sources import CBSL
from app.core.logger import logger

logger.info("Testing configuration")

print(settings.PROJECT_NAME)

print(CBSL)
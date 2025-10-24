import json
from config import settings
from utils.logger import logger

def store_feedback(feedback):
    try:
        with open(settings.FEEDBACK_STORE, "a", encoding="utf-8") as f:
            json.dump(feedback, f, ensure_ascii=False)
            f.write("\n")
        logger.debug("Stored feedback entry")
    except Exception:
        logger.exception("Error storing feedback to %s", settings.FEEDBACK_STORE)

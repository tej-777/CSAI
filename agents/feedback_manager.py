import json
from config import settings

def store_feedback(feedback):
    try:
        with open(settings.FEEDBACK_STORE, "a") as f:
            json.dump(feedback, f)
            f.write("\n")
    except Exception as e:
        print("Error storing feedback:", e)

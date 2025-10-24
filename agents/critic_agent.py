from llms.priorityestimatorllm import estimate_priority

def provide_feedback(summary):
    priority = estimate_priority(summary)
    feedback = {
        "priority": priority,
        "feedback": f"Priority level assigned: {priority}",
        "summary": summary
    }
    return feedback

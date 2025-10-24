from llms.intentanalyzerllm import analyze_intent

def summarize_output(routing_result):
    intent = analyze_intent(routing_result)
    summary = f"Intent: {intent}\nResponse: {routing_result.get('response', routing_result)}"
    return summary

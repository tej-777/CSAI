from llms.topicclassifierllm import classify_topic
from llms.intentanalyzerllm import analyze_intent

def route_to_llm(query):
    topic = classify_topic(query)
    intent = analyze_intent(query)
    # You might choose an LLM based on topic/intent here
    return topic, intent

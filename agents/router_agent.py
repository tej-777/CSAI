from researchers.billingresearcher import handle_billing_query
from researchers.techresearcher import handle_tech_query
from researchers.productresearcher import handle_product_query
from llms.topicclassifierllm import classify_topic

def route_query(query):
    topic = classify_topic(query)
    if topic == "billing":
        return handle_billing_query(query)
    elif topic == "technical":
        return handle_tech_query(query)
    elif topic == "product":
        return handle_product_query(query)
    else:
        return {"error": "Could not classify topic", "original_query": query}

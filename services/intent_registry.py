from services.intents import (
    handle_count,
    handle_attribute,
    handle_details,
    handle_aggregation
)

INTENT_REGISTRY = {
    "count": handle_count,
    "attribute": handle_attribute,
    "details": handle_details,
    "aggregation": handle_aggregation
}
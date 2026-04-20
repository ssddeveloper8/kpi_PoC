from entity_config import ENTITY_CONFIG
from services.intent_registry import INTENT_REGISTRY
from utils.intent_utils import detect_intent


def handle_entity(parsed, connections, entity_type, names, agg):
    intent = detect_intent(parsed, parsed.get("raw_query", ""))

    handler = INTENT_REGISTRY.get(intent)

    if not handler:
        return {"error": "Unsupported intent"}

    return handler(parsed, connections, entity_type, names, agg)
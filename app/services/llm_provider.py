try:
    from syncuze_core import ChatModel, EmbeddingModel
except ImportError:
    try:
        from raavone_core import ChatModel, EmbeddingModel
    except ImportError:
        class ChatModel:
            def generate(self, prompt: str) -> str:
                return "Mocked chat response."

            def generate_json(self, prompt: str, schema: type):
                return schema()

        class EmbeddingModel:
            def embed(self, text: str):
                return [0.0] * 128

try:
    from syncuze import AIService
except ImportError:
    try:
        from raavone import AIService
    except ImportError:
        class AIService:
            def generate_json(self, prompt: str, schema: type):
                return schema(memories=[])

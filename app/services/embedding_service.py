from app.services.llm_provider import EmbeddingModel

model = EmbeddingModel()


def create_embedding(text: str):

    return model.embed(text)

import httpx


class LocalQwenEmbeddings:
    def __init__(
        self,
        model="qwen3-embedding:0.6b",
        base_url="http://localhost:11434",
    ):
        self.model = model
        self.url = f"{base_url.rstrip('/')}/api/embed"

    async def _embed(self, texts):
        async with httpx.AsyncClient(timeout=180.0) as client:
            response = await client.post(
                self.url,
                json={
                    "model": self.model,
                    "input": texts,
                    "truncate": False,
                },
            )
            response.raise_for_status()
            vectors = response.json()["embeddings"]

        if len(vectors) != len(texts):
            raise ValueError(
                "Embedding count does not match input count."
            )

        if any(len(vector) != 1024 for vector in vectors):
            raise ValueError(
                "Expected 1024-dimensional embeddings."
            )

        return vectors

    async def aembed_documents(self, texts):
        """Generate one embedding for each supplied document chunk."""
        return await self._embed(texts)

    async def aembed_query(self, text):
        """Generate one embedding for the supplied search query."""
        query = (
            "Instruct: Retrieve relevant passages "
            "that answer the question.\n"
            f"Query: {text}"
        )
        return (await self._embed([query]))[0]
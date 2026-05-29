from pathlib import Path
from typing import List
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from support_copilot.domain.entities import RetrievedDocument
from support_copilot.infrastructure.config.settings import settings


class ChromaKnowledgeRepository:
    def __init__(self) -> None:
        self._embeddings = OpenAIEmbeddings(
            model=settings.openai_embeddings_model,
            api_key=settings.openai_api_key,
        )
        self._db_path = Path(settings.vector_store_dir)
        self._db_path.mkdir(parents=True, exist_ok=True)
        self._store = Chroma(
            persist_directory=str(self._db_path),
            embedding_function=self._embeddings,
            collection_name="support_docs",
        )

    def index_if_empty(self) -> None:
        if self._store._collection.count() > 0:
            return

        docs_dir = Path(settings.knowledge_base_dir)
        docs = []
        for file in docs_dir.glob("*.md"):
            docs.extend(TextLoader(str(file), encoding="utf-8").load())
        if not docs:
            return

        splitter = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=120)
        chunks = splitter.split_documents(docs)
        self._store.add_documents(chunks)

    def retrieve(self, question: str, k: int = 4) -> List[RetrievedDocument]:
        self.index_if_empty()
        docs = self._store.similarity_search(question, k=k)
        return [
            RetrievedDocument(
                source=(d.metadata.get("source") if d.metadata else "knowledge_base"),
                content=d.page_content,
            )
            for d in docs
        ]

from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from app.config import settings


DOCS_DIR = Path("knowledge_base")


def build_or_load_vectorstore() -> Chroma:
    embeddings = OpenAIEmbeddings(
        model=settings.embeddings_model,
        api_key=settings.openai_api_key,
    )
    db_path = Path(settings.vector_store_dir)
    db_path.mkdir(parents=True, exist_ok=True)

    existing = list(db_path.glob("**/*"))
    if existing:
        return Chroma(
            persist_directory=str(db_path),
            embedding_function=embeddings,
            collection_name="support_docs",
        )

    documents = []
    for path in DOCS_DIR.glob("*.md"):
        documents.extend(TextLoader(str(path), encoding="utf-8").load())

    splitter = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=120)
    chunks = splitter.split_documents(documents)

    return Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(db_path),
        collection_name="support_docs",
    )

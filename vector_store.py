import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self, collection_name="pdf_collection"):
        self.client = chromadb.Client(Settings(persist_directory="./chroma_db"))
        self.collection = self.client.get_or_create_collection(name=collection_name)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def add_text(self, text, metadata=None):
        chunks = self._chunk_text(text)
        embeddings = self.model.encode(chunks)
        ids = [f"id_{i}" for i in range(len(chunks))]
        self.collection.add(
            embeddings=embeddings.tolist(),
            documents=chunks,
            ids=ids,
            metadatas=[metadata] * len(chunks) if metadata else None
        )

    def search(self, query, n_results=5):
        query_embedding = self.model.encode([query]).tolist()
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )
        return results

    def _chunk_text(self, text, chunk_size=1000, overlap=200):
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            if end > len(text):
                end = len(text)
            chunk = text[start:end]
            chunks.append(chunk)
            start = end - overlap
        return chunks

vector_store = VectorStore()

def add_pdf_to_vector_store(pdf_text, pdf_name):
    metadata = {"source": pdf_name}
    vector_store.add_text(pdf_text, metadata)

def search_vector_store(query, n_results=5):
    return vector_store.search(query, n_results)

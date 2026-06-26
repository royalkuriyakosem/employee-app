from langchain_core.documents import Document
from pypdf import PdfReader
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Below is a minimal helper for demonstration purposes.
reader = PdfReader("policy.pdf")
full_text = ""
for page in reader.pages:
    text = page.extract_text()
    if text:
        full_text += text + "\n"

docs = [Document(page_content=full_text, metadata={"source": "policy.pdf"})]


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # chunk size (characters)
    chunk_overlap=200,  # chunk overlap (characters)
    add_start_index=True,  # track index in original document
)
all_splits = text_splitter.split_documents(docs)

print(f"Split blog post into {len(all_splits)} sub-documents.")


embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
    dimensions=1024,
)

vector_store = InMemoryVectorStore(embeddings)
document_ids = vector_store.add_documents(documents=all_splits)
vector_store.dump("agent_store.json")

print(document_ids)

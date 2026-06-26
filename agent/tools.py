from langchain.tools import tool
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings
from employees.router import get_all_employees
from database.connection import AsyncSessionLocal
from employees.schemas import EmployeeResponse


embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
    dimensions=1024,
)

vector_store = InMemoryVectorStore.load(
    "agent_store.json",
    embedding=embeddings,
)


@tool(response_format="content_and_artifact")
def retrieve_context(query: str):
    """Retrieve information to help answer a query."""
    retrieved_docs = vector_store.similarity_search(query, k=2)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\nContent: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs


@tool
async def get_all_employees_by_agent():
    """get all the employees of the company"""
    async with AsyncSessionLocal() as db:
        employees: list[EmployeeResponse] = await get_all_employees(db)
        print("Toool called ", employees)
        return [
            {"id": emp.id, "name": emp.name, "email": emp.email, "role": emp.role}
            for emp in employees
        ]

from langchain_docling import DoclingLoader
from langchain_docling.loader import ExportType
from langchain_community.vectorstores import FAISS
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_core.tools import Tool
from docling.chunking import HybridChunker

def create_retriever_tool(retriever, name: str, description: str) -> Tool:
    """Create a tool to do retrieval from a retriever."""
    def retrieve(query: str) -> str:
        docs = retriever.invoke(query)
        return "\n\n".join([doc.page_content for doc in docs])

    return Tool(
        name=name,
        description=description,
        func=retrieve,
    )

def create_retriever_tool_from_pdf(file_path: str):
    """
    Creates a retriever tool from a PDF file.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        A retriever tool.
    """
    model="sentence-transformers/all-MiniLM-L6-v2"
    
    loader = DoclingLoader(
        file_path=file_path,
        export_type=ExportType.DOC_CHUNKS,
        chunker=HybridChunker(tokenizer=model,max_tokens=512),
    )

    docs = loader.load()

    embedding=HuggingFaceEmbeddings(model_name=model)
    
    faiss=FAISS.from_documents(docs,embedding=embedding)
    db=faiss.as_retriever()
    tool=create_retriever_tool(db,"clause_retriever","returns a data regarding specific clause")

    return tool


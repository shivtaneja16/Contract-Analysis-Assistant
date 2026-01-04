from langgraph.graph import START,END, StateGraph
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage, SystemMessage
from typing import TypedDict, Annotated
from langchain_groq import ChatGroq
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import InMemorySaver
from langchain_docling import DoclingLoader
from langchain_docling.loader import ExportType
from langchain_community.vectorstores import FAISS
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from contract_analysis import create_retriever_tool_from_pdf

import os
os.environ["HF_HUB_DISABLE_SYMLINKS"] = "1"
from dotenv import load_dotenv

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

def create_graph(tool):
    """
    Creates a langgraph graph with the provided tool.

    Args:
        tool: The tool to be used in the graph.

    Returns:
        A compiled langgraph graph.
    """
    llm = ChatGroq(model="meta-llama/llama-4-maverick-17b-128e-instruct")
    llm_with_tools = llm.bind_tools([tool])

    def expert(state: State):
        return {"messages": [llm_with_tools.invoke(state["messages"])]}

    graph = StateGraph(State)
    graph.add_node("expert", expert)
    graph.add_node("tools", ToolNode([tool]))

    graph.add_edge(START, "expert")
    graph.add_conditional_edges("expert", tools_condition)
    graph.add_edge("tools", "expert")
    
    checkpointer=InMemorySaver()
    app = graph.compile(checkpointer=checkpointer)
    return app

def run_graph(app, question):
    """
    Runs the langgraph graph with the provided question.

    Args:
        app: The compiled langgraph graph.
        question (str): The user's question.

    Returns:
        The response from the graph.
    """
    config={"configurable":{"thread_id":"1"}}
    response = app.invoke(
        {
            "messages": [question]},config
    )
    return response["messages"][-1].content


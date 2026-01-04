import streamlit as st
from dotenv import load_dotenv

load_dotenv()

import pypdf
import io
import os
os.environ["HF_HUB_DISABLE_SYMLINKS"] = "1"
from contract_analysis import create_retriever_tool_from_pdf
from legal_expert import create_graph, run_graph

def main():
    st.set_page_config(page_title="PDF Q&A Assistant", layout="wide")

    st.title("📄 Contract Analysis Assistant")

    # Sidebar for file upload
    with st.sidebar:
        st.header("Upload Document")
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        
        if uploaded_file is not None:
            if "processed_file" not in st.session_state or st.session_state.processed_file != uploaded_file.name:
                with st.spinner("Processing PDF..."):
                    try:
                        # Save the uploaded file to a temporary location
                        temp_dir = "temp"
                        if not os.path.exists(temp_dir):
                            os.makedirs(temp_dir)
                        
                        file_path = os.path.join(temp_dir, uploaded_file.name)
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())

                        # Create the retriever tool and the graph
                        tool = create_retriever_tool_from_pdf(file_path)
                        st.session_state.graph = create_graph(tool)
                        
                        st.session_state.processed_file = uploaded_file.name
                        st.success("PDF processed successfully!")
                    except Exception as e:
                        st.error(f"Error processing PDF: {e}")
            
            if "graph" in st.session_state:
                st.info(f"Loaded: {uploaded_file.name}")

    # Main Chat Interface
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about the document..."):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Process the user's query
        if "graph" in st.session_state:
            with st.spinner("Thinking..."):
                response = run_graph(st.session_state.graph, prompt)
                st.session_state.messages.append({"role": "assistant", "content": response})
                with st.chat_message("assistant"):
                    st.markdown(response)
        else:
            st.warning("Please upload a PDF file first.")

if __name__ == "__main__":
    main()
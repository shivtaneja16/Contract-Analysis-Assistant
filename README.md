# Legal Expert - AI Contract Analyst

Legal Expert is a powerful AI-powered application designed to analyze legal contracts. It uses a LangGraph-based agent to retrieve relevant clauses from PDF documents and answer user queries with legal precision.

## Features

-   **PDF Upload**: Securely upload PDF contracts for analysis.
-   **Clause Retrieval**: Intelligent retrieval of specific contract clauses using vector similarity (FAISS).
-   **Legal Q&A**: Interactive chat interface to ask questions about the contract.
-   **Context-Aware**: The AI understands the context of the uploaded document to provide accurate answers.

## Tech Stack

-   **Frontend**: [Streamlit](https://streamlit.io/)
-   **Orchestration**: [LangGraph](https://langchain-ai.github.io/langgraph/) & [LangChain](https://www.langchain.com/)
-   **LLM**: Meta Llama 4 via [Groq](https://groq.com/)
-   **Embeddings**: HuggingFace (`sentence-transformers/all-MiniLM-L6-v2`)
-   **Vector Store**: FAISS
-   **Document Processing**: Docling & PyPDF

## Setup & Installation

### Prerequisites

-   Python 3.10+
-   [Groq API Key](https://console.groq.com/keys)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/legal-expert.git
    cd legal-expert
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the root directory and add your Groq API key:
    ```env
    GROQ_API_KEY=your_groq_api_key_here
    ```

## Usage

1.  **Run the application:**
    ```bash
    streamlit run app.py
    ```

2.  **Analyze a Contract:**
    -   Open the app in your browser (usually `http://localhost:8501`).
    -   Upload a PDF contract using the sidebar.
    -   Wait for the "PDF processed successfully!" notification.
    -   Ask questions like:
        -   "What is the termination clause?"
        -   "Summarize the confidentiality obligations."
        -   "Who are the parties involved?"

## Project Structure

-   `app.py`: The Streamlit frontend application.
-   `legal_expert.py`: The backend logic using LangGraph to orchestrate the AI agent.
-   `contract_analysis.py`: Utilities for document processing, embedding, and tool creation.
-   `requirements.txt`: List of Python dependencies.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

# LLM Microservice Project Report

## 1. Project Overview
This project is a modular, high-performance FastAPI microservice designed to serve state-of-the-art Large Language Models (LLMs) using the **Hugging Face Inference API**.

**Supported Models:**
1.  **Llama 3 8B Instruct** (`meta-llama/Meta-Llama-3-8B-Instruct`)
2.  **Qwen 2.5 7B Instruct** (`Qwen/Qwen2.5-7B-Instruct`)
3.  **Gemma 2 9B Instruct** (`google/gemma-2-9b-it`)

### Key Features & Architecture
*   **Hardware Agnostic**: Zero local RAM/GPU requirements. All inference happens remotely on Hugging Face servers.
*   **Cost**: Free via Hugging Face Access Token.
*   **Architecture**: "Remote Inference" pattern using `huggingface_hub`'s `AsyncInferenceClient`.
*   **Performance Monitoring**: Built-in latency tracking and model usage statistics.

---

## 2. Step-by-Step Implementation Guide

### Prerequisites
*   Python 3.10+
*   A Hugging Face Account & Access Token (Read permissions).

### Installation
1.  **Clone the project**.
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    (Main dependencies: `fastapi`, `uvicorn`, `huggingface_hub`)

3.  **Configure Environment**:
    Create a `.env` file with the following:
    ```ini
    # Security
    API_KEY=your_secure_internal_key
    HUGGINGFACE_TOKEN=hf_your_token_here

    # Model Configuration (Defaults provided in config.py, override here if needed)
    LLAMA_MODEL_ID=meta-llama/Meta-Llama-3-8B-Instruct
    QWEN_MODEL_ID=Qwen/Qwen2.5-7B-Instruct
    GEMMA_MODEL_ID=google/gemma-2-9b-it
    ```

### Running the Application
1.  **Start the Server**:
    ```bash
    uvicorn app.main:app --reload
    ```
    Server will run at `http://127.0.0.1:8000`.

2.  **Verify Functionality**:
    Run the included test script (ensure it is updated for the new endpoints) or use curl:
    ```bash
    python compare.py
    ```

---

## 3. Development Journey: Evolution

This project evolved to leverage the best open-weight models available.

### Phase 1: OpenRouter & Legacy Models (Deprecated)
*   **Original Goal**: Serve Mistral 7B & Phi-3 via OpenRouter.
*   **Lesson**: External APIs can have variable latency and cost structures.

### Phase 2: Embracing Hugging Face (Current)
*   **Goal**: detailed control and access to the newest models immediately upon release.
*   **Solution**: Direct integration with Hugging Face Inference API.
*   **Benefit**: Immediate access to Llama 3, Qwen 2.5, and Gemma 2 without waiting for third-party providers to host them.
*   **Outcome**: A robust, zero-local-footprint inference service.

---

## 4. Deep Dive: Code Structure

### A. Core Components
*   **`.env`**: Stores sensitive `HUGGINGFACE_TOKEN` and Service `API_KEY`.
*   **`app/main.py`**: The entry point. Handles routing logic:
    *   `/generate`: Dispatches requests to the appropriate model handler based on the `model` field.
*   **`app/config.py`**: Centralized configuration management using Pydantic.
*   **`app/models/`**:
    *   `llama.py`: Handler for Llama 3.
    *   `qwen.py`: Handler for Qwen 2.5.
    *   `gemma.py`: Handler for Gemma 2.

### B. Execution Flow
1.  **User Request**: POST to `/generate` with `{"model": "llama", "query": "..."}`.
2.  **Auth**: `app/main.py` validates the `api_key`.
3.  **Dispatch**: Logic selects `LlamaHandler`.
4.  **Inference**: `AsyncInferenceClient` sends payload to Hugging Face.
5.  **Response**: Text is returned to the user with latency metrics.

---

## 5. Developer Guide: Adding New Models

To add a new model (e.g., "Mistral-Nemo"):

1.  **Update Config (`app/config.py`)**:
    Add `mistral_model_id` to the `Settings` class.

2.  **Create Handler (`app/models/mistral.py`)**:
    Create a class `MistralHandler` inheriting the pattern from `LlamaHandler`, initializing with the new model ID.

3.  **Register (`app/main.py`)**:
    Import `MistralHandler`, initialize it, and add a condition in the `generate_text` endpoint:
    ```python
    elif "mistral" in model_name:
        response_text = await mistral_handler.generate(request.query)
    ```

---

## 6. Security Note
This project uses a `.gitignore` file to ensure sensitive keys (like `.env`) are never committed to version control. Always verify your git status before pushing.

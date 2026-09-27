# LLM AI Chatbot

This project is a simple LLM-based chatbot built with Python, FastAPI, Streamlit, LangChain, and Groq.

The frontend and backend are kept separate. The user interacts with the Streamlit application, which sends the question to the FastAPI backend. The backend passes the question through a small LangChain pipeline and sends it to the Groq-hosted `openai/gpt-oss-120b` model. The response then comes back through the API and is displayed in the Streamlit interface.

The project also includes Pytest-based API tests and a GitHub Actions workflow for continuous integration.

## Project Demo

The application is deployed and available for testing.

**Live Application:**
https://quickochat.streamlit.app/

The live application provides a simple chat interface. Enter a question, submit it, and the response from the configured LLM is displayed in the Streamlit application.

The deployed request flow is:

```text
User
  |
  v
Streamlit Application
  |
  | POST /chat
  v
FastAPI Backend
  |
  v
LangChain
  |
  v
Groq
  |
  v
openai/gpt-oss-120b
  |
  v
Response
  |
  v
Streamlit Application
```

The production backend can also be accessed directly:

```text
https://one-chatbot-sep2026-hosted.onrender.com
```

FastAPI API documentation:

```text
https://one-chatbot-sep2026-hosted.onrender.com/docs
```

Backend health check:

```text
https://one-chatbot-sep2026-hosted.onrender.com/health
```

## Project Structure

```text
1_chatbot_sep2026_hosted/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── backend/
│   ├── main.py
│   └── chatbot.py
│
├── frontend/
│   └── app.py
│
├── tests/
│   └── test_api.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

The main idea is to keep each part responsible for one thing.

* `frontend/app.py` contains the Streamlit interface.
* `backend/main.py` contains the FastAPI application and API endpoints.
* `backend/chatbot.py` contains the LangChain and Groq logic.
* `tests/test_api.py` contains the API tests.
* `.github/workflows/ci.yml` contains the GitHub Actions CI workflow.

## Application Flow

A user question follows this path:

```text
User
  |
  v
Streamlit Frontend
  |
  | POST /chat
  v
FastAPI Backend
  |
  v
LangChain Pipeline
  |
  v
Groq LLM
  |
  v
Response
  |
  v
Streamlit Frontend
```

There is no LLM logic in the Streamlit application. The frontend only collects the question, calls the API, and displays the response.

That separation makes it easier to change the frontend or backend independently later.

## LLM Configuration

The chatbot currently uses the following Groq configuration:

```text
Provider:    Groq
Model:       openai/gpt-oss-120b
Temperature: 0
```

The model is configured with `temperature=0`. This keeps the model output more consistent rather than deliberately adding randomness to each response.

The LangChain pipeline is essentially:

```text
Prompt
  |
  v
ChatGroq
  |
  v
StrOutputParser
  |
  v
Text Response
```

## Backend API

The FastAPI application exposes three endpoints.

| Method | Endpoint  | Description                                          |
| ------ | --------- | ---------------------------------------------------- |
| GET    | `/`       | Confirms that the API is running                     |
| GET    | `/health` | Returns the current health status                    |
| POST   | `/chat`   | Accepts a user question and returns the LLM response |

For example, a request to `/chat` looks like this:

```json
{
    "message": "What is machine learning?"
}
```

The API returns:

```json
{
    "response": "Machine learning is ..."
}
```

FastAPI also provides interactive API documentation through:

```text
/docs
```

When running locally, this can be opened at:

```text
http://127.0.0.1:8000/docs
```

This is useful during development because the API can be tested directly from the browser without using the Streamlit frontend.

## Environment Variables

The Groq API key is required when running the chatbot.

Create a `.env` file in the project root:

```text
GROQ_API_KEY=your_groq_api_key
```

The API key is not stored in the Python source code.

The `.env` file should also be excluded from Git using `.gitignore`. Production environments should provide the key through their own environment-variable configuration.

## Local Setup

Clone the repository:

```bash
git clone https://github.com/learnermp09/1_chatbot_sep2026_hosted.git
```

Move into the project directory:

```bash
cd 1_chatbot_sep2026_hosted
```

Create and activate a Python environment as required for the local setup.

Then install the project dependencies:

```bash
pip install -r requirements.txt
```

## Run the Backend

From the project root, start FastAPI with Uvicorn:

```bash
uvicorn backend.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

The interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Run the Frontend

Open another terminal and run:

```bash
streamlit run frontend/app.py
```

Streamlit will open the application in the browser.

The frontend sends the user's question to the FastAPI `/chat` endpoint and displays the returned response.

## Testing

The project uses Pytest for API testing.

Run the complete test suite with:

```bash
python -m pytest
```

The tests cover the main API behavior:

* Root endpoint
* Health endpoint
* Chat endpoint
* Request validation

The chat test does not make a real request to Groq. The `get_response()` function is mocked during the test.

This keeps the tests independent of the external LLM service, network availability, and production API credentials. It also avoids unnecessary Groq API usage during testing.

## Continuous Integration

GitHub Actions is used to run the checks automatically.

The workflow is located at:

```text
.github/workflows/ci.yml
```

The current CI process is:

```text
Git Push / Pull Request
        |
        v
Checkout Code
        |
        v
Set up Python 3.11
        |
        v
Install Dependencies
        |
        v
Check Python Syntax
        |
        v
Run Pytest
        |
        v
CI Pass / Fail
```

The workflow runs when code is pushed to the `main` branch or when a pull request is opened against `main`.

This means the project does not rely only on local testing. The same basic checks are also run by GitHub after code reaches the repository.

## Deployment

### Backend

The FastAPI backend is deployed on Render.

Production API:

```text
https://one-chatbot-sep2026-hosted.onrender.com
```

The main endpoints are:

```text
/
 /health
 /chat
```

Render is configured to deploy the backend after the required GitHub Actions CI checks pass.

So a change is not simply pushed and immediately treated as production-ready. The automated checks run first.

### Frontend

The Streamlit frontend is deployed through Streamlit Community Cloud.

Live application:

```text
https://quickochat.streamlit.app/
```

The frontend is connected to the GitHub repository and communicates with the production FastAPI backend using:

```text
POST /chat
```

The frontend and backend therefore remain separate applications even though they work together as one chatbot.

## CI/CD Flow

The overall backend deployment process looks like this:

```text
Developer
    |
    v
Git Commit
    |
    v
GitHub
    |
    v
GitHub Actions
    |
    +---- Python Syntax Check
    |
    +---- Pytest
    |
    v
CI Pass
    |
    v
Render
    |
    v
Production FastAPI Backend
```

The Streamlit frontend follows its own GitHub-to-Streamlit deployment path:

```text
GitHub
   |
   v
Streamlit Community Cloud
   |
   v
https://quickochat.streamlit.app/
```

The two deployed applications communicate through the FastAPI API.

## Design Approach

The application is intentionally kept small.

There is no need for a large framework structure for the current use case. The frontend, API layer, and LLM logic are separated so that each part can be understood and changed without affecting the others unnecessarily.

`frontend/app.py` handles the user interface.

`backend/main.py` handles HTTP requests, Pydantic validation, and API responses.

`backend/chatbot.py` handles the prompt, Groq model, LangChain chain, and response parsing.

`tests/test_api.py` checks the API behavior without calling the real LLM service.

`.github/workflows/ci.yml` runs the automated checks whenever relevant code changes are pushed to GitHub.

This gives the project a simple structure now while leaving room to add more functionality later.

## Future Extensions

The current application can be extended without changing the basic frontend-backend approach.

Possible additions include:

* Conversation history
* User authentication
* Database integration
* Streaming LLM responses
* Document upload
* Retrieval-Augmented Generation (RAG)
* Vector database integration
* Application logging and monitoring
* Rate limiting
* More detailed production error handling

## Example

A user enters:

```text
What is machine learning?
```

The Streamlit application sends:

```json
{
    "message": "What is machine learning?"
}
```

to:

```text
POST /chat
```

The FastAPI backend processes the request through the LangChain pipeline and sends it to the configured Groq model.

The response is then returned to Streamlit and displayed to the user.

## Source Code

The complete source code is available in the GitHub repository:

```text
https://github.com/learnermp09/1_chatbot_sep2026_hosted
```

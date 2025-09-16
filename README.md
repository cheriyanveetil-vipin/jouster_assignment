# LLM Knowledge Extractor Prototype by Vipin Cheriyanveetil

**About the application**: A small Python FastAPI-based prototype that accepts unstructured text, uses an LLM (open API) and returns:

- Summary
- Title
- Topics
- Sentiment
- keywords

The data of the analyses is stored to SQLite DB. There are two endpoints

- `POST /analyze` -> analyze text, store result, return it.
- `GET /search?topic=xyz` -> search stored analyses.

## Run locally

1. create a virtual environment and activate it:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install requirements:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a .env file:

   ```bash
   OPENAI_API_KEY="sk-..."
   ```

4. Start the app:

   ```bash
   uvicorn main:app --reload --port 8000
   ```

5. Docs :

   ```bash
   http://127.0.0.1:8000/docs
   ```

6. Try it:
   ```bash
   curl -X POST "http://127.0.0.1:8000/analyze" -H "Content-Type: application/json" -d '{"text":"Your text here"}'
   curl "http://127.0.0.1:8000/search?topic=ai"
   ```
7. Run tests :

   ```bash
   pytest
   ```

8. Explanation:
   With the given time i did not structure it well. but i feel i could seperate each logic out to its own file.

   **packages used:**

   - **FastAPI** : easy way to build API in python
   - **uvicorn** : to run the api
   - **openai** : to interact with a LLM
   - **python-dotenv** : to load env configs
   - **pytest** : to run unit tests

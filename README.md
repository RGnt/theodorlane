## TheodorLane
crude AI Coding agent for the [Boot.dev](https://www.boot.dev/courses/build-ai-agent-python) AI Agent course using OpenaI SDK instead of the Gemini, and against local agents.

- Create virtual environment with `uv venv` or `python -m venv venv` and activate it (google is your friend)
- Run ```uv add -r requirements.txt``` or ```pip install -r requirements.txt```
- To run the agent use uv run main.py "user prompt" --verbose (if you want more information what is going on)
- Create `.env` file, and add values `OPENAI_API_KEY=""` with key if provider requires it, and `BASE_URL=""` with the URL where the model is.

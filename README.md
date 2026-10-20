# LazyDesk - [Hacktoberfest Week 3 Dev Challenge](https://dev.to/challenges/hacktoberfest-week3-2026-10-19)

LazyDesk is a local-first productivity assistant that turns messy notes into
organized Markdown. It uses a local Ollama model through a small Streamlit
interface, so your notes are processed on your own computer instead of being
sent to a hosted AI service.

## Features

- **Organize tasks** into a Markdown checklist grouped under short headings.
- **Summarize notes** with a concise overview and key points.
- Preserves relative dates such as “next Friday” exactly as written.
- Keeps possibilities, questions, and uncertain statements tentative instead
  of turning them into committed tasks.
- Treats pasted notes as untrusted content and does not follow instructions
  embedded inside them.
- Validates Ollama responses and displays useful connection, timeout, and
  response errors.
- Download results as a Markdown file.

## Requirements

- Python 3.10 or newer
- [Ollama](https://ollama.com/)
- The `qwen2.5:3b` Ollama model

LazyDesk is configured to call Ollama at:

```text
http://localhost:11434/api/generate
```

## Installation

Clone the repository and create a virtual environment:

```bash
git clone https://github.com/<your-username>/LazyDesk.git
cd LazyDesk
python -m venv .venv
```

Activate the environment:

**Windows PowerShell**

```powershell
.venv\Scripts\Activate.ps1
```

**macOS/Linux**

```bash
source .venv/bin/activate
```

Install the Python dependencies:

```bash
python -m pip install -r requirements.txt
```

Install and start Ollama, then download the configured model:

```bash
ollama pull qwen2.5:3b
```

Make sure the Ollama application or service is running before using the app.

## Run the app

Start the Streamlit server:

```bash
streamlit run app.py
```

Open the local URL shown in the terminal, usually
`http://localhost:8501`.

Choose a mode, paste your notes, and select **Organize my mess**. Review the
generated result before relying on tasks or dates, then use **Download as
Markdown** to save it.

## Run tests

The core prompt and response-validation logic can be tested without starting
Streamlit, Ollama, or a network service:

```bash
python -m unittest discover -v
```

GitHub Actions runs the same test command on pushes, pull requests, and manual
workflow dispatches.

## Project structure

```text
.
├── app.py                  # Streamlit interface and Ollama integration
├── lazydesk_core.py        # Prompt construction and response validation
├── test_lazydesk_core.py   # Unit tests for the core logic
├── requirements.txt        # Python dependencies
└── docs/
    └── COPILOT_USAGE.md    # Development and verification notes
```

## Core module

The reusable logic in `lazydesk_core.py` is intentionally separate from the
UI:

```python
from lazydesk_core import build_prompt, parse_ollama_response

prompt = build_prompt("Finish the report by Friday.", "Organize tasks")
result = parse_ollama_response({"response": "## Tasks\n- Finish the report"})
```

`build_prompt()` supports only these modes:

- `Organize tasks`
- `Summarize notes`

An unsupported mode raises `ValueError`. `parse_ollama_response()` rejects
malformed, empty, non-string, and Ollama-error responses.

## Privacy and limitations

LazyDesk is designed to keep note processing local through Ollama. The app
does not provide authentication, cloud storage, or a database. Generated
content can still be incorrect, so review task assignments, deadlines, and
summaries before acting on them.

## License

A personal project created for Hacktoberfest Week 3 DevChallenge

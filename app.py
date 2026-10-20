
import asyncio
import sys

import requests

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from lazydesk_core import build_prompt, parse_ollama_response
import streamlit as st

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:3b"

st.set_page_config(
    page_title="LazyDesk",
    page_icon="🌿",
    layout="centered",
)

st.title("🌿 LazyDesk")
st.caption("Let your local AI handle the busywork.")
st.write(
    "Paste your messy notes. LazyDesk will organize them "
    "on your computer using Ollama."
)

mode = st.radio(
    "What would you like LazyDesk to do?",
    ["Organize tasks", "Summarize notes"],
    horizontal=True,
)

notes = st.text_area(
    "Your notes",
    placeholder=(
        "Example: finish Java assignment by Wednesday, "
        "email Rahul about the project, buy milk..."
    ),
    height=180,
    max_chars=12000,
)

if len(notes) > 6000:
    st.warning(
        "These notes are quite long. For better results on a "
        "low-memory PC, consider processing a shorter section."
    )

if st.button("✨ Organize my mess", type="primary"):
    if not notes.strip():
        st.warning("Paste some notes first.")
    else:
        try:
            with st.spinner(
                "Your local AI is working. This may take a little while..."
            ):
                response = requests.post(
                    OLLAMA_URL,
                    json={
                        "model": MODEL,
                        "prompt": build_prompt(notes, mode),
                        "stream": False,
                        "options": {
                            "temperature": 0.2,
                            "num_ctx": 2048,
                            "num_predict": 1000,
                        },
                    },
                    timeout=(5, 240),
                )

                response.raise_for_status()
                result = parse_ollama_response(response.json())

            if not result:
                st.error("The model returned an empty response. Try again.")
            else:
                st.session_state["result"] = result
                st.session_state["result_mode"] = mode

        except requests.exceptions.ConnectionError:
            st.error(
                "Cannot connect to Ollama. Make sure the Ollama "
                "application is running on your computer."
            )
        except requests.exceptions.Timeout:
            st.error(
                "The model took too long to respond. Try shorter notes "
                "or close other memory-intensive applications."
            )
        except requests.exceptions.RequestException as exc:
            st.error(f"Ollama request failed: {exc}")
        except ValueError as exc:
            st.error(f"Could not process the model response: {exc}")


if st.session_state.get("result"):
    st.divider()
    st.subheader("Your cleaned-up notes")

    st.markdown(st.session_state["result"])

    export_text = (
        f"# LazyDesk — {st.session_state['result_mode']}\n\n"
        f"{st.session_state['result']}\n"
    )

    st.download_button(
        "⬇️ Download as Markdown",
        data=export_text,
        file_name="lazydesk-notes.md",
        mime="text/markdown",
    )

    st.caption(
        "Processed by Qwen locally through Ollama. "
        "Review generated tasks and dates before relying on them."
    )

st.divider()
st.caption("LazyDesk · Open-weight AI · Local-first by design")

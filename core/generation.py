"""Optional grounded generation using an OpenAI-compatible chat-completions endpoint.

No external model is called unless LLM_BASE_URL, LLM_API_KEY and LLM_MODEL are set.
The default is offline and uses deterministic response templates.
"""
import os
from pathlib import Path
from typing import Any, Dict, List
import requests

ROOT = Path(__file__).resolve().parents[1]
try:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env")
except ImportError:
    pass


def generate_grounded_response(
    description: str,
    category: str,
    priority: str,
    priority_reason: str,
    queue: str,
    next_step: str,
    articles: List[Dict[str, Any]],
    fallback_message: str,
) -> Dict[str, str]:
    base_url = os.getenv("LLM_BASE_URL", "").strip()
    api_key = os.getenv("LLM_API_KEY", "").strip()
    model = os.getenv("LLM_MODEL", "").strip()
    if not (base_url and api_key and model and articles):
        return {"text": fallback_message, "mode": "offline-template-demo", "error": ""}

    evidence = "\n\n".join(
        f"ARTICLE_ID: {a['article_id']}\nTITLE: {a['title']}\nCONTENT:\n{a['content']}"
        for a in articles
    )
    system = (
        "You are a cautious enterprise maintenance decision-support assistant in a synthetic demo. "
        "Use only the provided article evidence and ticket details. Do not invent specifications, thresholds, "
        "measurements, causes or procedures. Never tell a person to touch, repair, stop, start, isolate, "
        "bypass or restart equipment. Do not claim to be a qualified technician. If evidence is incomplete, "
        "say so and route to a qualified human. Refer to article IDs by name. Your output is a draft for human review."
    )
    user = (
        f"TICKET DESCRIPTION:\n{description}\n\nSUGGESTED CATEGORY: {category}\n"
        f"SUGGESTED PRIORITY: {priority}\nPRIORITY RATIONALE: {priority_reason}\n"
        f"SUGGESTED REVIEW QUEUE: {queue}\nNEXT STEP: {next_step}\n\n"
        f"RETRIEVED ARTICLE EVIDENCE:\n{evidence}\n\n"
        "Write a concise draft for a maintenance analyst. Separate observed facts from suggestions. "
        "Include the relevant article IDs and state what needs human verification. Do not execute or authorise actions."
    )
    try:
        response = requests.post(
            base_url.rstrip("/") + "/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={
                "model": model,
                "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
                "temperature": 0.1,
                "max_tokens": 350,
            },
            timeout=(5, 30),
        )
        response.raise_for_status()
        payload = response.json()
        answer = payload["choices"][0]["message"]["content"].strip()
        if not answer:
            raise ValueError("Empty model response")
        return {"text": answer, "mode": "openai-compatible-llm", "error": ""}
    except Exception as exc:
        # Do not propagate credentials, request headers or raw provider response to the UI.
        return {
            "text": fallback_message,
            "mode": "offline-template-fallback",
            "error": f"Configured model call failed ({type(exc).__name__}); used local template fallback.",
        }

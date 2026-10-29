"""Transparent local retrieval baseline over fictional maintenance SOPs.

This is lexical retrieval, not embedding-based semantic search. It provides a small
retrieval baseline that can later be compared with vector/hybrid retrieval.
"""
from pathlib import Path
import re
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE_FILE = ROOT / "data" / "knowledge" / "maintenance_sop.md"
STOPWORDS = {
    "the", "and", "for", "with", "from", "that", "this", "have", "has", "was", "are",
    "were", "into", "then", "than", "when", "where", "what", "which", "whether", "will",
    "you", "your", "our", "not", "can", "could", "should", "would", "about", "issue",
    "reported", "please", "help", "need", "there", "their", "they", "because", "after",
}


def _tokens(text: str) -> set[str]:
    return {t for t in re.findall(r"[a-z0-9]+", text.lower()) if len(t) > 2 and t not in STOPWORDS}


def load_articles() -> List[Dict[str, str]]:
    if not KNOWLEDGE_FILE.exists():
        return []
    text = KNOWLEDGE_FILE.read_text(encoding="utf-8")
    chunks = re.split(r"(?=^## ARTICLE:)", text, flags=re.MULTILINE)
    articles = []
    for chunk in chunks:
        match = re.match(r"## ARTICLE:\s*([^\n]+)\nTitle:\s*([^\n]+)", chunk.strip())
        if not match:
            continue
        article_id, title = match.group(1).strip(), match.group(2).strip()
        articles.append({"article_id": article_id, "title": title, "content": chunk.strip()})
    return articles


def retrieve(query: str, top_k: int = 3) -> List[Dict[str, object]]:
    query_terms = _tokens(query)
    if not query_terms:
        return []
    results = []
    for article in load_articles():
        article_terms = _tokens(article["content"])
        overlap = len(query_terms.intersection(article_terms))
        if overlap == 0:
            continue
        # A simple transparent lexical score: overlap divided by query token count.
        score = overlap / max(1, len(query_terms))
        results.append({
            "article_id": article["article_id"],
            "title": article["title"],
            "score": round(min(1.0, score), 3),
            "content": article["content"],
        })
    results.sort(key=lambda item: (item["score"], item["article_id"]), reverse=True)
    return results[:top_k]

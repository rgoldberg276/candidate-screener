"""
util.py

Utility functions for:
- file extraction
- JSON extraction
- score clamping
- sanitization (analysis, questions, gap analysis, rewrite suggestions)
"""

import json
from typing import Any, Dict, List
from pypdf import PdfReader
from docx import Document


# =========================
# 1. File Extraction
# =========================

def extract_text_from_uploaded_file(uploaded_file) -> str:
    """
    Extracts text from an uploaded file.

    Supports:
    - Plain text (.txt)
    - PDF (.pdf)
    - Word documents (.docx)

    Returns an empty string if:
    - No file
    - Unsupported type
    - Extraction fails
    """
    if uploaded_file is None:
        return ""

    # Plain text files
    if uploaded_file.type == "text/plain":
        try:
            return uploaded_file.read().decode("utf-8", errors="ignore")
        except Exception:
            return ""

    # PDF files
    if uploaded_file.type == "application/pdf":
        try:
            reader = PdfReader(uploaded_file)
            text = []
            for page in reader.pages:
                text.append(page.extract_text() or "")
            return "\n".join(text)
        except Exception:
            return ""

    # Word documents (.docx)
    if uploaded_file.type in [
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/msword",
    ]:
        try:
            doc = Document(uploaded_file)
            paragraphs = [p.text for p in doc.paragraphs]
            return "\n".join(paragraphs)
        except Exception:
            return ""

    return ""


# =========================
# 2. JSON Extraction
# =========================

def extract_json_from_model_text(text: str) -> Dict[str, Any]:
    text = text.strip()

    if text.startswith("```"):
        text = text.strip("`").strip()
        if text.lower().startswith("json"):
            text = text[4:].strip()

    return json.loads(text)


# =========================
# 3. Score Clamping
# =========================

def clamp_score(value: Any, min_val: int, max_val: int) -> int:
    try:
        v = int(value)
    except Exception:
        v = min_val
    return max(min_val, min(max_val, v))


# =========================
# 4. Sanitization
# =========================

def sanitize_analysis(
    analysis_raw: Dict[str, Any],
    allowed_fields: Dict[str, type],
    min_score: int,
    max_score: int,
) -> Dict[str, Any]:
    from typing import Any as _Any  # avoid circular hints

    sanitized: Dict[str, _Any] = {}

    for field, expected_type in allowed_fields.items():
        raw_value = analysis_raw.get(field, None)

        if field.endswith("_score"):
            sanitized[field] = clamp_score(raw_value, min_score, max_score)
            continue

        if field == "risk_flags":
            if isinstance(raw_value, list):
                sanitized[field] = [str(x) for x in raw_value]
            else:
                sanitized[field] = []
            continue

        if expected_type is str:
            sanitized[field] = "" if raw_value is None else str(raw_value)
            continue

    return sanitized


def sanitize_validation_questions(raw_questions: Any) -> List[str]:
    if not isinstance(raw_questions, list):
        return []
    return [str(q) for q in raw_questions]


def sanitize_gap_analysis(raw_gap: Any) -> Dict[str, List[str]]:
    """
    Ensures gap_analysis is a dict of lists of strings.
    """
    default = {
        "missing_skills": [],
        "missing_tools": [],
        "missing_experience_depth": [],
        "missing_domain_knowledge": [],
        "priority_gaps": [],  # we will keep as list of strings for display
    }

    if not isinstance(raw_gap, dict):
        return default

    result = {}
    for key in default.keys():
        val = raw_gap.get(key, [])
        if isinstance(val, list):
            result[key] = [str(x) for x in val]
        else:
            result[key] = []

    return result


def sanitize_rewrite_suggestions(raw_suggestions: Any, min_confidence: float = 0.7) -> List[Dict[str, Any]]:
    """
    Ensures resume_rewrite_suggestions is a list of dicts with:
    - original: str
    - suggestion: str
    - confidence: float (>= min_confidence)
    """
    cleaned: List[Dict[str, Any]] = []

    if not isinstance(raw_suggestions, list):
        return cleaned

    for item in raw_suggestions:
        if not isinstance(item, dict):
            continue

        original = str(item.get("original", "")).strip()
        suggestion = str(item.get("suggestion", "")).strip()
        try:
            confidence = float(item.get("confidence", 0.0))
        except Exception:
            confidence = 0.0

        if not original or not suggestion:
            continue
        if confidence < min_confidence:
            continue

        cleaned.append(
            {
                "original": original,
                "suggestion": suggestion,
                "confidence": confidence,
            }
        )

    return cleaned
# =========================
# 5. ATS Keyword Analysis
# =========================

import re
from collections import Counter

def compute_ats_keyword_analysis(jd_text: str, resume_text: str) -> dict:
    """
    Simple ATS-style keyword extractor:
    - Extracts keywords from JD (nouns + verbs)
    - Counts occurrences in resume
    - Computes match score
    """

    if not jd_text or not resume_text:
        return {
            "jd_keywords": [],
            "resume_keywords": [],
            "missing_keywords": [],
            "match_score": 0,
        }

    # Normalize
    jd = jd_text.lower()
    resume = resume_text.lower()

    # Tokenize
    jd_tokens = re.findall(r"[a-zA-Z]{3,}", jd)
    resume_tokens = re.findall(r"[a-zA-Z]{3,}", resume)

    # Frequency maps
    jd_counts = Counter(jd_tokens)
    resume_counts = Counter(resume_tokens)

    # Extract top keywords from JD (simple heuristic)
    jd_keywords = [word for word, count in jd_counts.items() if count >= 2]

    # If too few keywords, fallback to top 15 unique words
    if len(jd_keywords) < 10:
        jd_keywords = list(jd_counts.keys())[:15]

    # Resume keyword hits
    resume_keywords = [kw for kw in jd_keywords if kw in resume_counts]

    # Missing keywords
    missing_keywords = [kw for kw in jd_keywords if kw not in resume_counts]

    # Match score
    if jd_keywords:
        match_score = int((len(resume_keywords) / len(jd_keywords)) * 100)
    else:
        match_score = 0

    return {
        "jd_keywords": jd_keywords,
        "resume_keywords": resume_keywords,
        "missing_keywords": missing_keywords,
        "match_score": match_score,
    }

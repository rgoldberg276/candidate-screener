"""
pipeline.py

This module orchestrates the full LLM pipeline:
- prompt construction
- model call
- JSON extraction
- guardrails enforcement
- sanitization
- final output assembly

This keeps app.py clean and maintains a real architecture.
"""

import json
from typing import Dict, Any, Tuple

import google.generativeai as genai

from llm_prompts import build_prompt
from guardrails import apply_guardrails

# Import sanitization utilities from app.py (or move them here)
from app import (
    extract_json_from_model_text,
    sanitize_analysis,
    sanitize_validation_questions,
    SCORE_MIN,
    SCORE_MAX,
    MODEL_NAME,
)


# ============================================================
# 1. Model call
# ============================================================

def call_model(prompt: str) -> Dict[str, Any]:
    """
    Calls the LLM and returns parsed JSON.
    """
    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)

    raw_text = (response.text or "").strip()
    parsed = extract_json_from_model_text(raw_text)

    return parsed


# ============================================================
# 2. Pipeline Orchestration
# ============================================================

def run_pipeline(jd_text: str, resume_text: str) -> Tuple[Dict[str, Any], list]:
    """
    Full pipeline:
    - Build prompt
    - Call model
    - Apply guardrails
    - Sanitize output
    - Return analysis + validation questions
    """

    # Build prompt
    prompt = build_prompt(jd_text, resume_text, SCORE_MIN, SCORE_MAX)

    # Call model
    raw_output = call_model(prompt)

    # Apply guardrails
    guarded_output = apply_guardrails(jd_text, resume_text, raw_output)

    # Extract fields
    raw_analysis = guarded_output.get("analysis", {})
    raw_questions = guarded_output.get("validation_questions", [])

    # Sanitize
    analysis = sanitize_analysis(raw_analysis)
    questions = sanitize_validation_questions(raw_questions)

    return analysis, questions
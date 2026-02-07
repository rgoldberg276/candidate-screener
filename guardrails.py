# guardrails.py
from typing import Dict, Any

# ============================================================
# 1. Word-level fuzzy similarity
# ============================================================

def word_level_similarity(a: str, b: str) -> float:
    a_tokens = {w.strip(".,;:()").lower() for w in a.split() if w.strip()}
    b_tokens = {w.strip(".,;:()").lower() for w in b.split() if w.strip()}
    if not a_tokens:
        return 0.0
    intersection = a_tokens.intersection(b_tokens)
    return len(intersection) / len(a_tokens)


def original_matches_resume(original: str, resume_text: str, threshold: float = 0.7) -> bool:
    resume_lines = [line.strip() for line in resume_text.split("\n") if line.strip()]
    original_clean = original.strip()
    for line in resume_lines:
        if word_level_similarity(original_clean, line) >= threshold:
            return True
    return False


# ============================================================
# 2. Evidence-based constraints
# ============================================================

def enforce_evidence_constraints(jd_text: str, resume_text: str, model_output: Dict[str, Any]) -> Dict[str, Any]:
    jd_lower = jd_text.lower()
    resume_lower = resume_text.lower()
    analysis = model_output.get("analysis", {})

    # --- Risk flags ---
    validated_flags = []
    for flag in analysis.get("risk_flags", []):
        f = str(flag).lower()
        if f in jd_lower or f in resume_lower:
            validated_flags.append(flag)
        elif any(k in f for k in ["unclear", "missing", "ambiguous", "gap"]):
            validated_flags.append(flag)
    analysis["risk_flags"] = validated_flags

    # --- Importance of gaps ---
    gaps_text = analysis.get("importance_of_gaps", "")
    if isinstance(gaps_text, str) and gaps_text:
        cleaned = []
        for sentence in gaps_text.split("."):
            s = sentence.strip().lower()
            if not s:
                continue
            if any(word in jd_lower for word in s.split()):
                cleaned.append(sentence)
            elif "gap" in s or "missing" in s:
                cleaned.append(sentence)
        analysis["importance_of_gaps"] = ". ".join(cleaned)

    # --- Resume enhancement ---
    enh_text = analysis.get("resume_enhancement", "")
    if isinstance(enh_text, str) and enh_text:
        cleaned = []
        for sentence in enh_text.split("."):
            s = sentence.strip().lower()
            if not s:
                continue
            if any(word in resume_lower for word in s.split()):
                cleaned.append(sentence)
            elif any(k in s for k in ["clarify", "quantify", "expand", "rewrite", "tighten"]):
                cleaned.append(sentence)
        analysis["resume_enhancement"] = ". ".join(cleaned)

    model_output["analysis"] = analysis

    # --- Gap analysis ---
    gap = model_output.get("gap_analysis", {})
    if isinstance(gap, dict):
        for key in ["missing_skills", "missing_tools", "missing_experience_depth", "missing_domain_knowledge"]:
            items = gap.get(key, [])
            validated = []
            for item in items:
                item_str = str(item).strip()
                if not item_str:
                    continue
                if item_str.lower() in jd_lower:
                    validated.append(item_str)
                elif any(w in item_str.lower() for w in ["gap", "missing", "lack", "no "]):
                    validated.append(item_str)
            gap[key] = validated

        pg = gap.get("priority_gaps", [])
        gap["priority_gaps"] = [str(x) for x in pg] if isinstance(pg, list) else []

        model_output["gap_analysis"] = gap

    # --- Resume rewrite suggestions ---
    suggestions = model_output.get("resume_rewrite_suggestions", [])
    if isinstance(suggestions, list):
        validated = []
        allowed_extra_words = {
            "overall", "platform", "key", "impactful", "cross-functional",
            "strategic", "operational", "technical", "business", "team",
            "stakeholders", "process", "improvements", "delivery", "quality"
        }

        for item in suggestions:
            if not isinstance(item, dict):
                continue

            original = str(item.get("original", "")).strip()
            suggestion = str(item.get("suggestion", "")).strip()
            try:
                confidence = float(item.get("confidence", 0.0))
            except:
                confidence = 0.0

            if not original or not suggestion or confidence < 0.7:
                continue

            if not original_matches_resume(original, resume_text, threshold=0.7):
                continue

            suggestion_words = [w.strip(".,;:()").lower() for w in suggestion.split()]
            foreign_count = 0

            for w in suggestion_words:
                if not w:
                    continue
                if w in resume_lower or w in jd_lower:
                    continue
                if w in allowed_extra_words:
                    continue
                if w in ["and", "or", "the", "a", "an", "to", "for", "with", "of", "in", "on", "as", "by"]:
                    continue
                if w in ["led", "managed", "drove", "improved", "increased", "reduced", "delivered", "supported"]:
                    continue
                foreign_count += 1

            if foreign_count > 12:
                continue

            validated.append({
                "original": original,
                "suggestion": suggestion,
                "confidence": confidence,
            })

        model_output["resume_rewrite_suggestions"] = validated

    return model_output


# ============================================================
# 3. Reasoning policy enforcement
# ============================================================

def enforce_reasoning_policy(model_output: Dict[str, Any]) -> Dict[str, Any]:
    analysis = model_output.get("analysis", {})

    forbidden = [
        "personality", "attitude", "motivation", "intent",
        "race", "gender", "ethnicity", "religion", "political",
        "mental", "psychological", "predict", "future",
        "will succeed", "will fail"
    ]

    for key, value in analysis.items():
        if isinstance(value, str):
            lower = value.lower()
            if any(p in lower for p in forbidden):
                analysis[key] = ""
        elif isinstance(value, list):
            analysis[key] = [
                item for item in value
                if not any(p in str(item).lower() for p in forbidden)
            ]

    model_output["analysis"] = analysis
    return model_output


# ============================================================
# 4. Main entry point
# ============================================================

def apply_guardrails(jd_text: str, resume_text: str, model_output: Dict[str, Any]) -> Dict[str, Any]:
    model_output = enforce_evidence_constraints(jd_text, resume_text, model_output)
    model_output = enforce_reasoning_policy(model_output)
    return model_output

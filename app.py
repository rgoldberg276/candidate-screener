# app.py

import os
import json

import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

from util import (
    extract_text_from_uploaded_file,
    compute_ats_keyword_analysis,
)
from guardrails import apply_guardrails
from llm_prompts import SYSTEM_PROMPT


# =========================
# 1. Environment + Model
# =========================

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in environment. Check your .env file.")

genai.configure(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-3-flash-preview"


# =========================
# 2. Streamlit UI
# =========================

st.set_page_config(page_title="Candidate Screener", layout="wide")
st.title("Candidate Screener")

# ---- Job Description Input ----
st.subheader("1. Job Description")

jd_file = st.file_uploader("Upload Job Description (TXT or PDF)", type=["txt", "pdf"])

if jd_file:
    jd_text = extract_text_from_uploaded_file(jd_file)
    if not jd_text.strip():
        st.warning("Could not extract text from the uploaded Job Description file.")
        jd_text = st.text_area("Or paste Job Description here", height=200)
else:
    jd_text = st.text_area("Paste Job Description", height=200)

# ---- Resume upload ----
st.subheader("2. Resume")

resume_file = st.file_uploader("Upload Resume (PDF, TXT, or DOCX)", type=["pdf", "txt", "docx"])

if not resume_file:
    resume_text = st.text_area("Or paste Resume", height=200)
else:
    resume_text = ""  # will be filled on Analyze


# =========================
# 3. Analyze Button
# =========================

if st.button("Analyze"):

    if not jd_text.strip():
        st.warning("Please provide a Job Description.")
        st.stop()

    if resume_file:
        resume_text = extract_text_from_uploaded_file(resume_file)
        if not resume_text.strip():
            st.error("Could not extract text from resume file.")
            st.stop()
    else:
        if not resume_text.strip():
            st.warning("Please provide a Resume (upload or paste).")
            st.stop()

    # --------------------------
    # 3.1 ATS Keyword Analysis
    # --------------------------
    st.markdown("## 1. ATS Keyword Match Analysis")

    ats = compute_ats_keyword_analysis(jd_text, resume_text)
    ats_score = ats.get("match_score", 0)

    if ats_score >= 70:
        color = "green"
    elif ats_score >= 40:
        color = "orange"
    else:
        color = "red"

    st.markdown(
        f"**ATS Match Score:** "
        f"<span style='color:{color}; font-size: 22px;'>{ats_score}%</span>",
        unsafe_allow_html=True,
    )

    st.progress(ats_score / 100)

    st.markdown("### Job Description Keywords Detected")
    st.write(", ".join(ats.get("jd_keywords", [])) or "None detected.")

    st.markdown("### Resume Keywords Detected")
    st.write(", ".join(ats.get("resume_keywords", [])) or "None detected.")

    st.markdown("### Missing Keywords")
    if ats.get("missing_keywords"):
        st.write(", ".join(ats["missing_keywords"]))
    else:
        st.write("None — all JD keywords are present in the resume.")

    st.markdown("---")

    # --------------------------
    # 3.2 LLM-Based Resume Analysis
    # --------------------------
    st.markdown("## 2. LLM-Based Resume Analysis")

    prompt = f"""
Job Description:
{jd_text}

Resume:
{resume_text}

Return JSON only.
"""

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(
            SYSTEM_PROMPT + "\n\n" + prompt,
            generation_config={
                "temperature": 0,
                "max_output_tokens": 4096
            }
        )
        raw_output = (response.text or "").strip()
    except Exception as e:
        st.error(f"Gemini API error: {e}")
        st.stop()

    # Parse JSON
    try:
        model_output = json.loads(raw_output)
    except Exception:
        st.error("Model returned invalid JSON.")
        st.text(raw_output)
        st.stop()

    # Apply guardrails
    model_output = apply_guardrails(jd_text, resume_text, model_output)

    analysis = model_output.get("analysis", {}) or {}
    validation_questions = model_output.get("validation_questions", []) or []
    gap_analysis = model_output.get("gap_analysis", {}) or {}
    rewrite_suggestions = model_output.get("resume_rewrite_suggestions", []) or []
    gap_text = model_output.get("gap_analysis_text", "")

    # --------------------------
    # 2.1 Match Analysis Metrics
    # --------------------------
    st.subheader("Match Analysis")

    overall_score = int(analysis.get("overall_score", 0) or 0)
    skills_score = int(analysis.get("skills_score", 0) or 0)
    experience_score = int(analysis.get("experience_score", 0) or 0)
    impact_score = int(analysis.get("impact_score", 0) or 0)
    leadership_score = int(analysis.get("leadership_score", 0) or 0)

    cols = st.columns(5)
    cols[0].metric("Overall", overall_score)
    cols[1].metric("Skills", skills_score)
    cols[2].metric("Experience", experience_score)
    cols[3].metric("Impact", impact_score)
    cols[4].metric("Leadership", leadership_score)

    st.write("**Summary:**", analysis.get("summary", ""))
    st.write("**Recommendation:**", analysis.get("recommendation", ""))
    st.write("**Importance of Gaps:**", analysis.get("importance_of_gaps", ""))
    st.write("**Potential Areas of Enhancement:**", analysis.get("resume_enhancement", ""))

    risk_flags = analysis.get("risk_flags", []) or []
    if risk_flags:
        st.write("**Risk / Uncertainty Flags:**")
        for flag in risk_flags:
            st.write(f"- {flag}")

    # --------------------------
    # 2.2 Gap Analysis
    # --------------------------
    st.subheader("Gap Analysis")

    if any(gap_analysis.values()):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Missing Skills**")
            if gap_analysis.get("missing_skills"):
                for s in gap_analysis["missing_skills"]:
                    st.write(f"- {s}")
            else:
                st.write("_None detected._")

            st.markdown("**Missing Tools / Technologies**")
            if gap_analysis.get("missing_tools"):
                for t in gap_analysis["missing_tools"]:
                    st.write(f"- {t}")
            else:
                st.write("_None detected._")

        with col2:
            st.markdown("**Missing Experience Depth**")
            if gap_analysis.get("missing_experience_depth"):
                for e in gap_analysis["missing_experience_depth"]:
                    st.write(f"- {e}")
            else:
                st.write("_None detected._")

            st.markdown("**Missing Domain Knowledge**")
            if gap_analysis.get("missing_domain_knowledge"):
                for d in gap_analysis["missing_domain_knowledge"]:
                    st.write(f"- {d}")
            else:
                st.write("_None detected._")

        st.markdown("**High-Priority Gaps**")
        if gap_analysis.get("priority_gaps"):
            for g in gap_analysis["priority_gaps"]:
                st.write(f"- {g}")
        else:
            st.write("_No high-priority gaps identified._")

        # --------------------------
        # NEW: Narrative Gap Summary (below structured lists)
        # --------------------------
        if gap_text:
            st.markdown("---")
            st.markdown("### Gap Analysis Summary")
            st.write(gap_text)

    else:
        st.write("_No structured gaps identified._")

    # --------------------------
    # 2.3 Resume Rewrite Suggestions
    # --------------------------
    st.subheader("Resume Rewrite Suggestions")

    if rewrite_suggestions:
        for item in rewrite_suggestions:
            original = item.get("original", "")
            suggestion = item.get("suggestion", "")
            confidence = float(item.get("confidence", 0.0) or 0.0)

            st.markdown("**Original:**")
            st.write(original)
            st.markdown("**Suggested Rewrite:**")
            st.write(suggestion)
            st.caption(f"Confidence: {confidence:.2f}")
            st.markdown("---")
    else:
        st.write("_No high-confidence rewrite suggestions generated._")

    # --------------------------
    # 2.4 Validation Questions
    # --------------------------
    st.subheader("Validation Questions (Phone Screen)")

    if validation_questions:
        for i, q in enumerate(validation_questions, start=1):
            st.markdown(f"**Q{i}.** {q}")
    else:
        st.write("_No validation questions generated._")
        

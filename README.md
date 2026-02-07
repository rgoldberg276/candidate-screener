Candidate Screener
A simple, user‑friendly tool that lets you test how well a resume matches a job description. The app combines ATS‑style keyword matching with structured AI analysis to highlight strengths, gaps, and opportunities to improve a resume for a specific role.
Built with Streamlit, Google Gemini, and a lightweight guardrails system for safe, predictable output.

⭐ What This App Does
Upload:
- A Job Description (PDF or text)
- A Resume (PDF, DOCX, or text)
The app will:
1. Perform ATS Keyword Analysis
- Extracts keywords from the job description
- Detects which appear in the resume
- Highlights missing keywords
- Computes a match score
2. Run AI‑Powered Resume Analysis
Using a structured Gemini prompt, the app returns:
- Match scores (skills, experience, impact, leadership)
- A recruiter‑style summary
- Risk or uncertainty flags
- Gap analysis (skills, tools, domain knowledge, experience depth)
- A narrative explanation of why the gaps matter
- Resume rewrite suggestions
- Validation questions for a phone screen
3. Apply Guardrails
The guardrails.py module ensures:
- No hallucinated claims
- No invented experience
- No personality or demographic inferences
- Rewrite suggestions only come from text that actually exists in the resume


PROJECT Structure:
candidate-screener/
│
├── app.py                 # Streamlit UI and main application logic
├── util.py                # File parsing, ATS keyword extraction, helpers
├── pipeline.py            # LLM orchestration, JSON parsing, guardrails integration
├── guardrails.py          # Evidence checks, rewrite validation, safety filters
├── llm_prompts.py         # System prompt and structured JSON schema
├── requirements.txt       # Dependencies for Streamlit Cloud
└── README.md              # This file
# ats_dictionary.py
"""
Workday-style ATS keyword dictionary (hybrid mode, cross-industry).

- Literal, lowercased strings only
- Multi-word skills/tools included as atomic phrases
- No synonyms, no embeddings, no semantic expansion
- Designed to be used with simple token/phrase matching

You can safely extend any of these lists over time.
"""

# ============================================================
# Core skills (cross-industry, technical + business)
# ============================================================

SKILLS = [
    # General / business
    "project management",
    "program management",
    "product management",
    "business analysis",
    "business intelligence",
    "data analysis",
    "data analytics",
    "requirements gathering",
    "stakeholder management",
    "process improvement",
    "change management",
    "risk management",
    "strategic planning",
    "operational excellence",
    "continuous improvement",
    "customer experience",
    "customer success",
    "contact center operations",
    "workforce management",

    # Software engineering
    "software development",
    "software engineering",
    "object oriented programming",
    "test driven development",
    "continuous integration",
    "continuous delivery",
    "microservices",
    "api design",
    "rest api",
    "graphql",
    "system design",
    "distributed systems",
    "performance optimization",
    "code review",
    "version control",

    # Data / AI / ML / NLP
    "machine learning",
    "deep learning",
    "natural language processing",
    "nlp",
    "computer vision",
    "data engineering",
    "data warehousing",
    "data modeling",
    "feature engineering",
    "model deployment",
    "model monitoring",
    "mlops",
    "prompt engineering",
    "retrieval augmented generation",
    "rag",
    "vector search",
    "recommendation systems",
    "time series analysis",
    "statistical modeling",
    "a b testing",
    "experiment design",

    # Cloud / DevOps
    "cloud computing",
    "infrastructure as code",
    "configuration management",
    "continuous deployment",
    "site reliability engineering",
    "sre",
    "observability",
    "monitoring and alerting",
    "capacity planning",
    "disaster recovery",
    "high availability",
    "scalability",

    # Contact center / CX / CCaaS
    "contact center modernization",
    "omnichannel routing",
    "interactive voice response",
    "ivr design",
    "workforce optimization",
    "quality management",
    "speech analytics",
    "conversation analytics",
    "sentiment analysis",
    "agent assist",
    "knowledge management",
    "case management",

    # Healthcare / clinical
    "clinical workflows",
    "care coordination",
    "care management",
    "population health",
    "clinical documentation",
    "clinical decision support",
    "prior authorization",
    "utilization management",
    "revenue cycle management",
    "claims processing",
    "medical coding",
    "risk adjustment",
    "value based care",
    "electronic health records",
    "ehr integration",
    "health information exchange",

    # Finance / operations
    "financial analysis",
    "budgeting and forecasting",
    "cost optimization",
    "revenue optimization",
    "supply chain management",
    "inventory management",
    "logistics planning",
    "procurement management",

    # Misc cross-industry
    "agile methodologies",
    "scrum",
    "kanban",
    "waterfall",
    "lean",
    "six sigma",
    "design thinking",
    "user research",
    "user experience design",
    "ux design",
    "ui design",
    "requirements prioritization",
]

# ============================================================
# Tools & technologies (languages, frameworks, platforms)
# ============================================================

TOOLS = [
    # Programming languages
    "python",
    "java",
    "javascript",
    "typescript",
    "c",
    "c++",
    "c sharp",
    "c#",
    "go",
    "golang",
    "ruby",
    "php",
    "r",
    "scala",
    "kotlin",
    "swift",
    "objective c",

    # Web / backend frameworks
    "django",
    "flask",
    "fastapi",
    "spring",
    "spring boot",
    "node js",
    "express",
    "next js",
    "nest js",
    "rails",
    "laravel",
    "asp net",
    "asp net core",

    # Frontend frameworks
    "react",
    "react js",
    "angular",
    "vue",
    "svelte",
    "redux",
    "webpack",

    # Databases / data stores
    "postgresql",
    "mysql",
    "mariadb",
    "sql server",
    "oracle database",
    "mongodb",
    "cassandra",
    "redis",
    "elasticsearch",
    "dynamodb",
    "snowflake",
    "bigquery",
    "redshift",
    "databricks",
    "hive",
    "spark",

    # Cloud platforms
    "aws",
    "amazon web services",
    "azure",
    "microsoft azure",
    "google cloud",
    "gcp",
    "ibm cloud",

    # DevOps / infra
    "docker",
    "kubernetes",
    "helm",
    "terraform",
    "ansible",
    "jenkins",
    "github actions",
    "gitlab ci",
    "circleci",
    "prometheus",
    "grafana",
    "datadog",
    "new relic",
    "splunk",

    # Analytics / bi
    "tableau",
    "power bi",
    "looker",
    "qlik",
    "mode analytics",

    # CRM / service / ccaaS
    "salesforce",
    "salesforce service cloud",
    "salesforce health cloud",
    "servicenow",
    "zendesk",
    "freshdesk",
    "genesys cloud",
    "nice cxone",
    "five9",
    "amazon connect",
    "twilio flex",
    "talkdesk",
    "cisco contact center",

    # Healthcare platforms
    "epic",
    "epic hyperspace",
    "epic clarity",
    "cerner",
    "allscripts",
    "meditech",
    "athenahealth",

    # AI / ML tooling
    "pytorch",
    "tensorflow",
    "keras",
    "scikit learn",
    "hugging face",
    "langchain",
    "mlflow",
    "kubeflow",

    # Collaboration / pm
    "jira",
    "confluence",
    "asana",
    "trello",
    "monday com",
    "slack",
    "microsoft teams",
    "sharepoint",
]

# ============================================================
# Certifications (cross-industry)
# ============================================================

CERTIFICATIONS = [
    # Project / agile
    "pmp",
    "project management professional",
    "prince2",
    "certified scrum master",
    "csm",
    "professional scrum master",
    "psm",
    "safe agilist",
    "safe practitioner",

    # Cloud
    "aws certified solutions architect",
    "aws certified developer",
    "aws certified sysops administrator",
    "aws certified devops engineer",
    "microsoft certified azure administrator",
    "microsoft certified azure solutions architect",
    "google professional cloud architect",
    "google professional data engineer",

    # Security
    "cissp",
    "certified information systems security professional",
    "cism",
    "certified information security manager",
    "ceh",
    "certified ethical hacker",
    "security plus",
    "comp tia security plus",

    # Networking
    "ccna",
    "cisco certified network associate",
    "ccnp",
    "cisco certified network professional",

    # Healthcare
    "registered nurse",
    "rn",
    "licensed practical nurse",
    "lpn",
    "board certified",
    "epic certified",
    "epic resolute certified",
    "epic cadence certified",
    "epic beacon certified",
    "cpc",
    "certified professional coder",
    "rhia",
    "registered health information administrator",
    "rhitr",
    "registered health information technician",

    # Data / analytics
    "google data analytics professional certificate",
    "ibm data science professional certificate",
    "tableau desktop specialist",
    "tableau certified professional",

    # IT service / governance
    "itil foundation",
    "itil practitioner",
]

# ============================================================
# Seniority / level indicators
# ============================================================

SENIORITY = [
    "junior",
    "associate",
    "mid level",
    "senior",
    "lead",
    "principal",
    "staff",
    "manager",
    "senior manager",
    "director",
    "senior director",
    "vice president",
    "vp",
    "senior vice president",
    "svp",
    "executive vice president",
    "evp",
    "chief",
    "head of",
    "global head",
]

# ============================================================
# Action verbs (resume-style impact verbs)
# ============================================================

ACTION_VERBS = [
    "led",
    "managed",
    "owned",
    "delivered",
    "designed",
    "architected",
    "implemented",
    "developed",
    "built",
    "created",
    "launched",
    "deployed",
    "migrated",
    "optimized",
    "improved",
    "enhanced",
    "streamlined",
    "automated",
    "reduced",
    "increased",
    "accelerated",
    "scaled",
    "stabilized",
    "resolved",
    "troubleshot",
    "debugged",
    "analyzed",
    "evaluated",
    "assessed",
    "prioritized",
    "coordinated",
    "collaborated",
    "partnered",
    "facilitated",
    "negotiated",
    "influenced",
    "mentored",
    "coached",
    "trained",
    "documented",
    "standardized",
    "implemented best practices",
    "drove",
    "spearheaded",
    "championed",
    "orchestrated",
    "owned end to end",
]

# ============================================================
# Domain terms (populated dynamically by LLM; kept here for type clarity)
# ============================================================

DOMAIN_TERMS: list[str] = []

# ============================================================
# Helper: convert lists to sets for fast lookup
# ============================================================

SKILLS_SET = set(SKILLS)
TOOLS_SET = set(TOOLS)
CERTIFICATIONS_SET = set(CERTIFICATIONS)
SENIORITY_SET = set(SENIORITY)
ACTION_VERBS_SET = set(ACTION_VERBS)

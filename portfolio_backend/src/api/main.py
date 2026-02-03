from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers import achievements, contact_messages, education, profiles, projects, skills

openapi_tags = [
    {"name": "System", "description": "Health, version, and system endpoints."},
    {"name": "Profiles", "description": "About/Profile section CRUD."},
    {"name": "Projects", "description": "Projects section CRUD."},
    {"name": "Skills", "description": "Skills section CRUD."},
    {"name": "Education", "description": "Education section CRUD."},
    {"name": "Achievements", "description": "Achievements section CRUD."},
    {"name": "Contact", "description": "Contact messages CRUD."},
]

app = FastAPI(
    title="Student Portfolio Hub API",
    description="Backend API for managing student portfolio sections (profile, projects, skills, education, achievements, contact).",
    version="1.0.0",
    openapi_tags=openapi_tags,
)

app.add_middleware(
    CORSMiddleware,
    # Frontend origin is environment-dependent; permissive CORS is used for this template.
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/",
    tags=["System"],
    summary="Health check",
    description="Basic health check endpoint.",
    operation_id="health_check",
)
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@app.get(
    "/version",
    tags=["System"],
    summary="API version",
    description="Return API version metadata.",
    operation_id="get_version",
)
def get_version():
    """Return API version metadata."""
    return {"name": app.title, "version": app.version}


# Routers
app.include_router(profiles.router)
app.include_router(projects.router)
app.include_router(skills.router)
app.include_router(education.router)
app.include_router(achievements.router)
app.include_router(contact_messages.router)

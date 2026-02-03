from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, HttpUrl


class ORMBase(BaseModel):
    """Base schema enabling ORM attribute reading."""

    model_config = {"from_attributes": True}


# -----------------------
# Profile
# -----------------------
class ProfileCreate(BaseModel):
    full_name: str = Field(..., max_length=200, description="Student full name.")
    headline: Optional[str] = Field(None, max_length=300, description="Short headline/tagline.")
    bio: Optional[str] = Field(None, description="About me / bio.")
    location: Optional[str] = Field(None, max_length=200)
    email: Optional[EmailStr] = Field(None, description="Public contact email.")
    phone: Optional[str] = Field(None, max_length=50)
    website: Optional[HttpUrl] = Field(None, description="Personal website URL.")
    github_url: Optional[HttpUrl] = Field(None, description="GitHub profile URL.")
    linkedin_url: Optional[HttpUrl] = Field(None, description="LinkedIn profile URL.")


class ProfileUpdate(BaseModel):
    full_name: Optional[str] = Field(None, max_length=200)
    headline: Optional[str] = Field(None, max_length=300)
    bio: Optional[str] = None
    location: Optional[str] = Field(None, max_length=200)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=50)
    website: Optional[HttpUrl] = None
    github_url: Optional[HttpUrl] = None
    linkedin_url: Optional[HttpUrl] = None


class ProfileOut(ORMBase):
    id: int
    full_name: str
    headline: Optional[str]
    bio: Optional[str]
    location: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    website: Optional[HttpUrl]
    github_url: Optional[HttpUrl]
    linkedin_url: Optional[HttpUrl]
    created_at: datetime
    updated_at: datetime


# -----------------------
# Projects
# -----------------------
class ProjectCreate(BaseModel):
    title: str = Field(..., max_length=200)
    description: Optional[str] = None
    tech_stack: Optional[str] = Field(None, max_length=500, description="Comma-separated stack (optional).")
    project_url: Optional[HttpUrl] = None
    repo_url: Optional[HttpUrl] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class ProjectUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    tech_stack: Optional[str] = Field(None, max_length=500)
    project_url: Optional[HttpUrl] = None
    repo_url: Optional[HttpUrl] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None


class ProjectOut(ORMBase):
    id: int
    title: str
    description: Optional[str]
    tech_stack: Optional[str]
    project_url: Optional[HttpUrl]
    repo_url: Optional[HttpUrl]
    start_date: Optional[date]
    end_date: Optional[date]
    created_at: datetime
    updated_at: datetime


# -----------------------
# Skills
# -----------------------
class SkillCreate(BaseModel):
    name: str = Field(..., max_length=120)
    level: Optional[str] = Field(None, max_length=50, description="Proficiency level (optional).")
    category: Optional[str] = Field(None, max_length=120, description="Category (e.g. Backend, Frontend).")


class SkillUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=120)
    level: Optional[str] = Field(None, max_length=50)
    category: Optional[str] = Field(None, max_length=120)


class SkillOut(ORMBase):
    id: int
    name: str
    level: Optional[str]
    category: Optional[str]
    created_at: datetime
    updated_at: datetime


# -----------------------
# Education
# -----------------------
class EducationCreate(BaseModel):
    institution: str = Field(..., max_length=250)
    degree: Optional[str] = Field(None, max_length=250)
    field_of_study: Optional[str] = Field(None, max_length=250)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    grade: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None


class EducationUpdate(BaseModel):
    institution: Optional[str] = Field(None, max_length=250)
    degree: Optional[str] = Field(None, max_length=250)
    field_of_study: Optional[str] = Field(None, max_length=250)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    grade: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None


class EducationOut(ORMBase):
    id: int
    institution: str
    degree: Optional[str]
    field_of_study: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]
    grade: Optional[str]
    description: Optional[str]
    created_at: datetime
    updated_at: datetime


# -----------------------
# Achievements
# -----------------------
class AchievementCreate(BaseModel):
    title: str = Field(..., max_length=250)
    issuer: Optional[str] = Field(None, max_length=250)
    date_awarded: Optional[date] = None
    description: Optional[str] = None
    url: Optional[HttpUrl] = None


class AchievementUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=250)
    issuer: Optional[str] = Field(None, max_length=250)
    date_awarded: Optional[date] = None
    description: Optional[str] = None
    url: Optional[HttpUrl] = None


class AchievementOut(ORMBase):
    id: int
    title: str
    issuer: Optional[str]
    date_awarded: Optional[date]
    description: Optional[str]
    url: Optional[HttpUrl]
    created_at: datetime
    updated_at: datetime


# -----------------------
# Contact Messages
# -----------------------
class ContactMessageCreate(BaseModel):
    sender_name: str = Field(..., max_length=200)
    sender_email: EmailStr = Field(..., description="Email for reply.")
    subject: Optional[str] = Field(None, max_length=250)
    message: str = Field(..., min_length=1, description="Message content.")


class ContactMessageUpdate(BaseModel):
    sender_name: Optional[str] = Field(None, max_length=200)
    sender_email: Optional[EmailStr] = None
    subject: Optional[str] = Field(None, max_length=250)
    message: Optional[str] = Field(None, min_length=1)


class ContactMessageOut(ORMBase):
    id: int
    sender_name: str
    sender_email: EmailStr
    subject: Optional[str]
    message: str
    created_at: datetime

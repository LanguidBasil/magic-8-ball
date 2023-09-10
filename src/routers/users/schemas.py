from enum import auto, StrEnum
from datetime import datetime

from fastapi import Query
from pydantic import BaseModel, Field, EmailStr, conint

from routers.questions.schemas import Post_Response as QuestionsPost_Response


class Get_IncludeEnum(StrEnum):
    questions = auto()

class GetByID_Query(BaseModel):
    user_id: int
    include: list[Get_IncludeEnum] = Field(Query([]))

class GetByEmail_Query(BaseModel):
    email: EmailStr
    include: list[Get_IncludeEnum] = Field(Query([]))

class Get_Response(BaseModel):
    id: conint(strict=True, ge=1)
    
    creation_date: datetime
    email: EmailStr
    
    questions: list[QuestionsPost_Response] = None


class Post_Body(BaseModel):
    email: EmailStr

class Post_Response(BaseModel):
    id: conint(strict=True, ge=1)
    
    creation_date: datetime
    email: EmailStr

import re
import random
from datetime import datetime

from pydantic import BaseModel, field_validator, Field, EmailStr, conint, constr

from config import ANSWER_OPTIONS
from api.database import User, Question


_r_only_words_and_space = r"[^\w ]"

class QuestionResponse(BaseModel):
    id: conint(strict=True, ge=1)
    
    creation_date: datetime
    text: constr(
        strip_whitespace=True, 
        to_lower=True, 
    ) = Field(examples=["Найду ли я настоящую любовь?"])
    total_voices: conint(strict=True, ge=1)
    
    @field_validator("text")
    @classmethod
    def format_text(cls, value: str):
        return re.sub(_r_only_words_and_space, "", value, flags=re.UNICODE)
    
    def __init__(self, question: Question, total_voices: int, **kwargs):
        super().__init__(
            id = question.id,
            creation_date = question.creation_date,
            text = question.text,
            total_voices = total_voices,
            **kwargs,
        )

class PostAsk_Body(BaseModel):
    # pattern is for any unicode character and space
    text: constr(
        strip_whitespace=True, 
        to_lower=True, 
    ) = Field(examples=["Найду ли я настоящую любовь?"])
    
    @field_validator("text")
    @classmethod
    def format_text(cls, value: str):
        return re.sub(_r_only_words_and_space, "", value, flags=re.UNICODE)

class PostAsk_Response(BaseModel):
    question: QuestionResponse
    
    answer: constr(
        strip_whitespace=True, 
        to_lower=True, 
    ) = Field(examples=["абсолютно точно"])
    
    def __init__(self, question: Question, total_voices: int, **kwargs):
        super().__init__(
            question = QuestionResponse(question, total_voices),
            answer = random.choice(ANSWER_OPTIONS),
            **kwargs,
        )


class GetByEmail_Query(BaseModel):
    email: EmailStr

class Get_Response(BaseModel):
    id: conint(strict=True, ge=1)
    
    creation_date: datetime
    email: EmailStr
    
    questions: list[QuestionResponse]
    
    def __init__(self, user: User, questions: list[tuple[Question, int]] = None, **kwargs):
        super().__init__(
            id = user.id,
            creation_date = user.creation_date,
            email = user.email,
            questions = [
                QuestionResponse(q, total_asked) 
                for q, total_asked in 
                questions
            ] if questions is not None else [],
            **kwargs,
        )


class Post_Body(BaseModel):
    email: EmailStr

class Post_Response(BaseModel):
    id: conint(strict=True, ge=1)
    
    creation_date: datetime
    email: EmailStr
    
    def __init__(self, user: User, **kwargs):
        super().__init__(
            id = user.id,
            creation_date = user.creation_date,
            email = user.email,
            **kwargs,
        )

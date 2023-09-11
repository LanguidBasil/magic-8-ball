from datetime import datetime

from pydantic import BaseModel, Field, EmailStr, conint, constr

from database import User, Question


_r_any_unicode_character_and_space = "[\p{L}\p{M}* ]"

class PostAsk_Body(BaseModel):    
    # pattern is for any unicode character and space
    text: constr(
        strip_whitespace=True, 
        to_lower=True, 
        pattern=_r_any_unicode_character_and_space
    ) = Field(examples=["Найду ли я настоящую любовь?"])

class PostAsk_Response(BaseModel):
    id: conint(strict=True, ge=1)
    
    creation_date: datetime
    text: constr(
        strip_whitespace=True, 
        to_lower=True, 
        pattern=_r_any_unicode_character_and_space
    ) = Field(examples=["Абсолютно точно"])
    total_voices: conint(strict=True, ge=1)
    
    def __init__(self, question: Question, total_voices: int, **kwargs):
        super().__init__(
            id = question.id,
            creation_date = question.creation_date,
            text = question.text,
            total_voices = total_voices,
            **kwargs,
        )


class GetByEmail_Query(BaseModel):
    email: EmailStr

class Get_Response(BaseModel):
    id: conint(strict=True, ge=1)
    
    creation_date: datetime
    email: EmailStr
    
    questions: list[PostAsk_Response]
    
    def __init__(self, user: User, questions: list[tuple[Question, int]] = None, **kwargs):
        super().__init__(
            id = user.id,
            creation_date = user.creation_date,
            email = user.email,
            questions = [
                PostAsk_Response(q, total_asked) 
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

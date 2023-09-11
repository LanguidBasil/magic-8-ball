import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from routers._utils.schemas import make_dependable
from routers.users.schemas import (
    GetByEmail_Query,
    Get_Response, 
    Post_Body,
    Post_Response,
    PostAsk_Response,
    PostAsk_Body,
) 
from routers.users.service import (
    get_user_by_id as s_get_user_by_id,
    get_user_by_email as s_get_user_by_email,
    create_user as s_create_user,
    add_question_to_user as s_add_question_to_user,
    count_times_question_asked as s_count_times_question_asked,
) 


router = APIRouter(prefix="/users")
logger = logging.getLogger("default")


@router.get("/{user_id}", response_model=Get_Response | None)
async def get_user_by_id(user_id: int):
    user, questions = await s_get_user_by_id(user_id, include_questions=True)
    if user is None and questions is None:
        return None
    
    return Get_Response(user, questions)

@router.get("/", response_model=Get_Response | None)
async def get_user_by_email(
        query: Annotated[GetByEmail_Query, Depends(make_dependable(GetByEmail_Query))],
    ):
    user, questions = await s_get_user_by_email(query.email, include_questions=True)
    if user is None:
        return None
    
    return Get_Response(user, questions)

@router.post("/", response_model=Post_Response)
async def create_user(body: Post_Body):
    user = await s_get_user_by_email(body.email)
    if user is not None:
        raise HTTPException(404, f"User {body.email} already exists")
        
    return Post_Response(await s_create_user(body.email))

@router.post(
    "/{user_id}/ask", 
    response_model=PostAsk_Response,
    description="""
Will create question if not exists otherwise add to history

Will strip whitespaces, make every character lower case and remove all characters except unicode letters and spaces
""",
)
async def user_ask(
        user_id: int,
        question: PostAsk_Body,
    ):
    u = await s_get_user_by_id(user_id)
    if u is None:
        raise HTTPException(404, f"User {user_id} not exists")
    
    q = await s_add_question_to_user(u, question.text)
    
    return PostAsk_Response(q, total_voices=await s_count_times_question_asked(q))

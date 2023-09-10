import logging
from typing import Annotated

from fastapi import APIRouter, Depends

from routers._utils.schemas import make_dependable
from routers.users.schemas import (
    GetByID_Query,
    GetByEmail_Query,
    Get_Response, 
    Post_Body,
    Post_Response,
) 


router = APIRouter(prefix="/users")
logger = logging.getLogger("default")


@router.get("/{user_id}", response_model=Get_Response)
async def get_user_by_id(
        query: Annotated[GetByID_Query, Depends(make_dependable(GetByID_Query))],
    ):
    return Get_Response()

@router.get("/", response_model=Get_Response)
async def get_user_by_email(
        query: Annotated[GetByEmail_Query, Depends(make_dependable(GetByEmail_Query))],
    ):
    return Get_Response()

@router.post("/", response_model=Post_Response)
async def create_user(body: Post_Body):
    pass

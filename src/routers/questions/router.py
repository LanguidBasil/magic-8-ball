import logging

from fastapi import APIRouter

from routers.questions.schemas import Post_Body, Post_Response


router = APIRouter(prefix="/questions")
logger = logging.getLogger("default")


@router.post("/", response_model=Post_Response)
async def ask(question: Post_Body):
    """Will create question if not exists otherwise incease total_asked"""
    pass

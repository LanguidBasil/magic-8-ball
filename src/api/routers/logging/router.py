import re
from typing_extensions import Annotated

import aiofiles
from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse

from config import APP_LOGS_PATH
from api.utils.schemas import make_dependable
from api.routers.logging.schemas import GetLogs_Query


router = APIRouter(prefix="/logging")

@router.get("/", response_class=PlainTextResponse)
async def get_logs(query: Annotated[GetLogs_Query, Depends(make_dependable(GetLogs_Query))]):
    
    async with aiofiles.open(APP_LOGS_PATH) as f:
        text = await f.read()
        
        
    if query.contains is not None:
        query.regex = fr"^.*\b{query.contains}\b.*$"
    
    if query.regex is None:
        return text
        
    return "\n".join(re.findall(query.regex, text, re.MULTILINE))

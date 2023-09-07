import logging
import json

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from asgi_correlation_id import CorrelationIdMiddleware, CorrelationIdFilter

from routers.profiles.router import router as profiles_router
from routers.logging.router import router as logging_router


app_v1 = FastAPI(title="Tomoru. Custom integrations", version="1.0", redoc_url=None)


app_v1.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# generate id for each request for easier log parsing
app_v1.add_middleware(CorrelationIdMiddleware)


logger = logging.getLogger("default")

def configure_loggers():
    from config import APP_LOGS_PATH
    
    filter = CorrelationIdFilter()
        
    formatter = logging.Formatter(
        "[%(correlation_id)s %(asctime)s %(levelname)-8s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    handler = logging.FileHandler(APP_LOGS_PATH, encoding="UTF-8")
    handler.setFormatter(formatter)
    
    
    logger.setLevel("INFO")
    logger.addFilter(filter)
    logger.addHandler(handler)
configure_loggers()

@app_v1.exception_handler(Exception)
async def log_general_exception(request: Request, e: Exception):
    logger.error(json.dumps({
        "exception code": 500,
        "detail": str(e),
    }))
    return JSONResponse(status_code=500, content="Internal Error")
    
@app_v1.exception_handler(HTTPException)
async def log_http_exception(request: Request, e: HTTPException):
    logging_func = None
    if 400 <= e.status_code < 500:
        logging_func = logger.warning
        res = JSONResponse(status_code=e.status_code, content={ "detail": e.detail })
    elif 500 <= e.status_code < 600:
        logging_func = logger.error
        res = JSONResponse(status_code=e.status_code, content="Internal Error")
    
    logging_func(json.dumps({
        "exception code": e.status_code,
        "detail": e.detail,
    }))
    return res

async def log_request(request: Request):
    # can't use middleware here because of bug in Starlette' request body caching
    # detail on problem and solution on this thread
    # https://github.com/tiangolo/fastapi/issues/394#issuecomment-513051977
    
    info = {
        "path": request.url.path,
        "headers": dict(request.headers),
        "path params": request.path_params,
        "query params": dict(request.query_params),
    }
    if request.headers.get("Content-Length") is not None:
        info["body"] = await request.json()
    
    logger.info(json.dumps(info))


app_v1.include_router(profiles_router, tags=["Profiles"], dependencies=[Depends(log_request)])
app_v1.include_router(logging_router,  tags=["Loggging"])


app = FastAPI()
app.mount("/v1", app_v1)

@app.get("/health-check")
async def health_check():
    return "Ok"

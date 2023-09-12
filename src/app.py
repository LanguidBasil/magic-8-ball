import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from asgi_correlation_id import CorrelationIdMiddleware, CorrelationIdFilter

from api.routers.users.router import router as users_router
from api.routers.logging.router import router as logging_router

from root.routers.index.router import router as index_router


def configure_loggers():
    from config import APP_LOGS_PATH
    
    filter = CorrelationIdFilter()
        
    formatter = logging.Formatter(
        "[%(correlation_id)s %(asctime)s %(levelname)-8s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    handler = logging.FileHandler(APP_LOGS_PATH, encoding="UTF-8")
    handler.setFormatter(formatter)
    
    
    logger = logging.getLogger("default")
    logger.setLevel("INFO")
    logger.addFilter(filter)
    logger.addHandler(handler)
configure_loggers()


app = FastAPI()


app_api_v1 = FastAPI(title="Softorium. Magic 8 ball", version="1.0", redoc_url=None)

app_api_v1.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# generate id for each request for easier log parsing
app_api_v1.add_middleware(CorrelationIdMiddleware)

app_api_v1.include_router(users_router, tags=["Users"])
app_api_v1.include_router(logging_router,  tags=["Loggging"])

app.mount("/api/v1", app_api_v1)


app_root = FastAPI(title="Softorium. Magic 8 ball", version="1.0", redoc_url=None)

app_root.include_router(index_router, tags=["Index"])

app.mount("/", app_root)

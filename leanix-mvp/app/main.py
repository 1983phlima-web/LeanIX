from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routes.analysis import router as analysis_router
from app.api.routes.factsheets import router as factsheets_router
from app.api.routes.health import router as health_router
from app.api.routes.query import router as query_router
from app.api.routes.suggest import router as suggest_router
from app.core.config import get_settings
from app.core.logging import configure_logging, set_correlation_id
from app.domain.policies import PolicyError

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    configure_logging(settings.log_level)
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)


@app.middleware("http")
async def correlation_middleware(request: Request, call_next):
    correlation_id = request.headers.get("x-correlation-id")
    set_correlation_id(correlation_id)
    response = await call_next(request)
    response.headers["x-correlation-id"] = correlation_id or "generated"
    return response


@app.exception_handler(PolicyError)
async def policy_error_handler(_: Request, exc: PolicyError):
    return JSONResponse(status_code=422, content={"detail": str(exc)})


app.include_router(health_router, prefix=settings.api_v1_prefix)
app.include_router(query_router, prefix=settings.api_v1_prefix)
app.include_router(factsheets_router, prefix=settings.api_v1_prefix)
app.include_router(analysis_router, prefix=settings.api_v1_prefix)
app.include_router(suggest_router, prefix=settings.api_v1_prefix)

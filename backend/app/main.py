from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import ApplicationException


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)


@app.exception_handler(ApplicationException)
async def application_exception_handler(
    request: Request,
    exc: ApplicationException
):
    logger.error(exc.message)

    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


@app.get("/")
def home():
    return {"message": "AI Customer Support Agent is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
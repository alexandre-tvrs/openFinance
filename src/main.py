import uvicorn
from fastapi import FastAPI
from utils import setup as setup_utils
from contextlib import asynccontextmanager
from fastapi.responses import RedirectResponse

metadata = setup_utils.get_project_metadata()


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_utils.create_db_and_tables()
    setup_utils.get_project_routers(app)
    yield


app = FastAPI(
    title=metadata["name"],
    version=metadata["version"],
    description=metadata["description"],
    lifespan=lifespan,
)


@app.get("/", include_in_schema=False)
async def redirect_to_docs() -> RedirectResponse:
    return RedirectResponse("/docs")


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)

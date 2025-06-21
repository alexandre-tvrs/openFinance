import tomllib
from pathlib import Path
from importlib import util
from sqlmodel import SQLModel
from core.database import setup as db
from fastapi import APIRouter, FastAPI
from models import ExpenseModel


def get_project_metadata() -> dict:
    pyproject_path = Path(__file__).parent.parent.parent / "pyproject.toml"
    with pyproject_path.open("rb") as f:
        pyproject_data = tomllib.load(f)
    project: dict = pyproject_data.get("project", {})
    return {
        "name": project.get("name"),
        "version": project.get("version"),
        "description": project.get("description"),
        "authors": project.get("authors"),
    }


def get_project_routers(app: FastAPI, routers_dir: str = "src/routers") -> None:
    base_path = Path(routers_dir)

    for file in base_path.glob("*.py"):
        if not file.name.startswith("_"):
            module_name = f"{routers_dir.replace("/", ".")}.{file.stem}"
            spec = util.spec_from_file_location(module_name, str(file))
            module = util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, "router") and isinstance(module.router, APIRouter):
                tag = file.stem
                prefix = f"/{tag}"
                app.include_router(module.router, prefix=prefix, tags=[tag])
                print(f"🔗 Loaded router: {module_name}")


def create_db_and_tables():
    SQLModel.metadata.create_all(db.engine)

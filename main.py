from fastapi import FastAPI
from middleware import configure_middleware
from database import create_tables
from contextlib import asynccontextmanager
from employees.router import router as employee_router
from department.router import router as department_router
from associations.router import router as associations_router
from agent.router import router as agent_router
from config import settings
from exceptions.handlers import register_exception_handler
from auth.router import router as auth_router
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(
    title="Employee App",
    description="A web app for employee management system",
    version="1.0.0",
    lifespan=lifespan,
)

configure_middleware(app)
app.exception_handler(register_exception_handler(app))
app.include_router(employee_router)
app.include_router(department_router)
app.include_router(auth_router)
app.include_router(associations_router)
app.include_router(agent_router)


@app.get("/health", tags=["root"])
async def root():
    return {
        "status": "healthy",
        "message": "Welcome to Employee App",
        "env": settings.app_env,
    }


_employee = {}
_id = 0


def get_next_id():
    return _id + 1


# TODO
# Delete the association related to employee before deleting the employee

# TODO
# Do proper logging


# TODO
# write tests

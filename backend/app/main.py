from fastapi import FastAPI

from db import create_db_and_tables
from ecg.routers import ecg_router
from auth.routers import auth_router
from auth.utils import initialize_admin_user

app = FastAPI()

# Register routers
app.include_router(ecg_router)
app.include_router(auth_router)

@app.get("/")
async def health_check():
    """
    Health check endpoint.

    Returns:
        dict: A dictionary with a message indicating the server status.
    """
    return {"message": "Hello, World!"}

@app.on_event("startup")
def on_startup():
    """
    Startup event handler. It creates the necessary database tables and
    initializes the admin user if not already present.

    Returns:
        None
    """
    create_db_and_tables()
    initialize_admin_user()

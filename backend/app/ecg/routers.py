from fastapi import APIRouter, Depends
from typing import List

from db import SessionDep
from auth.utils import UserRequired, user_required

from .models import Lead
from .crud import create_ecg, retrieve_ecgs, retrieve_ecg_by_id, compute_insights

ecg_router = APIRouter(
    prefix="/ecg",
    tags=["ECG Endpoints"]
)


@ecg_router.get("/get_all", description="Retrieve all ECG records.")
async def get_ecgs(user: UserRequired, session: SessionDep):
    """
    Retrieve all ECG records from the database. Requires user role.

    Args:
        user (UserRequired): The authenticated user making the request.
        session (SessionDep): The database session dependency.

    Returns:
        dict: A dictionary containing a message and all ECG records.
    """
    response = retrieve_ecgs(user, session)

    return {"message": "All ecgs", "data": response}


@ecg_router.get("/get/{ecg_id}", description="Retrieve ECG record by its ID.")
async def get_ecg(user: UserRequired, ecg_id: int, session: SessionDep):
    """
    Retrieve a specific ECG record by its ID. Requires user role.

    Args:
        user (UserRequired): The authenticated user making the request.
        ecg_id (int): The ID of the ECG record to retrieve.
        session (SessionDep): The database session dependency.

    Returns:
        dict: A dictionary containing the ECG record associated with the specified ID.
    """
    response = retrieve_ecg_by_id(user, session, ecg_id)
    return {"message": f"ECG with ID: {ecg_id}", "data": response}


@ecg_router.post("/create", description="Create a new ECG record from leads.")
async def create_ecg_from_leads(leads: List[Lead], user: UserRequired, session: SessionDep):
    """
    Create a new ECG record from a list of leads. Requires user role.

    Args:
        leads (List[Lead]): A list of Lead objects to associate with the new ECG record.
        user (UserRequired): The authenticated user creating the ECG record.
        session (SessionDep): The database session dependency.

    Returns:
        dict: A dictionary confirming the creation of the new ECG record.
    """
    response = create_ecg(user, session, leads)
    return {"data": response, "message": "Created ecg"}


@ecg_router.get("/get_insight/{ecg_id}", description="Retrieve insights for a specific ECG record.")
async def get_insight(ecg_id: int, user: UserRequired, session: SessionDep):
    """
    Retrieve insights for a specific ECG record.

    Args:
        ecg_id (int): The ID of the ECG record to compute insights for.
        user (UserRequired): The authenticated user making the request.
        session (SessionDep): The database session dependency.

    Returns:
        dict: A dictionary containing the computed insights for the ECG record.
    """
    response = compute_insights(user, session, ecg_id)
    return {"message": f"Insight for ecg_id: {ecg_id}", "data": response}

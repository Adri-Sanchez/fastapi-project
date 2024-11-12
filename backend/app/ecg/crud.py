from datetime import datetime
from typing import List

from fastapi import HTTPException
from sqlmodel import Session, select

from auth.models import User

from .models import ECG, Lead
from .utils import count_zero_crossings

def create_ecg(user: User, session: Session, leads: List[Lead]) -> ECG:
    """
    Create an ECG record with the given leads.

    Args:
        session (Session): SQLModel session used to interact with the database.
        leads (List[Lead]): List of Lead objects that represent the ECG channels.

    Returns:
        ECG: The created ECG record, including the assigned id and timestamp.
    """
    ecg = ECG(date=datetime.now(), leads=leads, user_id=user.id)
    session.add(ecg)
    session.commit()
    session.refresh(ecg)

    return ecg

def retrieve_ecgs(user: User, session: Session) -> List[ECG]:
    """
    Retrieve all ECG records from the database.

    Args:
        user (User): The user making the request.
        session (Session): SQLModel session used to interact with the database.

    Returns:
        List[ECG]: A list of all ECG records stored in the database.
    """
    return session.query(ECG).filter(ECG.user_id == user.id).all()

def retrieve_ecg_by_id(user: User, session: Session, ecg_id: int) -> ECG:
    """
    Retrieve an ECG record by its ID.

    Args:
        user (User): The user making the request.
        session (Session): SQLModel session used to interact with the database.
        ecg_id (int): The unique identifier of the ECG record to retrieve.

    Raises:
        HTTPException: If the ECG record is not found, a 404 error is raised.

    Returns:
        ECG: The ECG record corresponding to the provided ID.
    """
    ecg = session.exec(select(ECG).where(ECG.id == ecg_id, ECG.user_id == user.id)).first()

    if not ecg:
        raise HTTPException(status_code=404, detail="ECG not found")

    return ecg

def compute_insights(user: User, session: Session, ecg_id: int) -> dict:
    """
    Compute insights based on an ECG record's leads.

    Args:
        user (User): The user making the request.
        session (Session): SQLModel session used to interact with the database.
        ecg_id (int): The ID of the ECG record for which to compute insights.

    Returns:
        dict: A dictionary containing insights (e.g., zero-crossings) for the ECG.
    """
    ecg = retrieve_ecg_by_id(user, session, ecg_id)

    # Response data
    insights = {
        "zero_crossings": count_zero_crossings(ecg.leads),
    }

    return insights

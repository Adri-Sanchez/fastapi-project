import pytest
from fastapi import HTTPException
from sqlmodel import Session
from typing import List

from auth.models import User, Role
from ecg.crud import create_ecg, retrieve_ecgs, retrieve_ecg_by_id, compute_insights
from ecg.models import Lead
from ecg.utils import count_zero_crossings


@pytest.fixture
def test_leads() -> List[Lead]:
    return [
        Lead(identifier="I", signal=[1, 2, 3, 4, 5]),
        Lead(identifier="II", signal=[5, -1, 3, -5, -10, 10])
    ]


def test_create_ecg(session: Session, test_leads: List[Lead], test_user: User):
    ecg = create_ecg(user=test_user, session=session, leads=test_leads)

    assert ecg.id is not None
    assert ecg.date is not None
    assert len(ecg.leads) == 2
    assert ecg.user_id == test_user.id


def test_retrieve_ecgs(session: Session, test_leads: List[Lead]):
    test_user = User(username="test_user", hashed_password="password")
    session.add(test_user)
    session.commit()

    create_ecg(user=test_user, session=session, leads=test_leads)
    create_ecg(user=test_user, session=session, leads=test_leads)

    ecgs = retrieve_ecgs(user=test_user, session=session)

    assert len(ecgs) == 2
    assert all(ecg.user_id == test_user.id for ecg in ecgs)


def test_retrieve_ecg_by_id(session: Session, test_user: User, test_leads: List[Lead]):
    ecg = create_ecg(user=test_user, session=session, leads=test_leads)
    retrieved_ecg = retrieve_ecg_by_id(user=test_user, session=session, ecg_id=ecg.id)

    assert retrieved_ecg.id == ecg.id
    assert retrieved_ecg.user_id == test_user.id
    assert retrieved_ecg.leads == ecg.leads


def test_retrieve_ecg_by_id_not_found(session: Session, test_user: User):
    with pytest.raises(HTTPException) as exc_info:
        retrieve_ecg_by_id(user=test_user, session=session, ecg_id=999)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "ECG not found"


def test_compute_insights(session: Session, test_user: User, test_leads: List[Lead]):
    ecg = create_ecg(user=test_user, session=session, leads=test_leads)
    insights = compute_insights(user=test_user, session=session, ecg_id=ecg.id)

    expected_zero_crossings = count_zero_crossings(test_leads)
    assert insights["zero_crossings"] == expected_zero_crossings

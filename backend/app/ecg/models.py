from datetime import datetime
from typing import List, Optional

from sqlalchemy import Column, Integer
from sqlalchemy.dialects import postgresql
from sqlmodel import Field, SQLModel, Relationship


class Lead(SQLModel, table=True):
    """
    Represents a Lead in an ECG record.

    Attributes:
        id (Optional[int]): The unique identifier of the Lead.
        identifier (str): The identifier of the lead (e.g., I, II, III, etc.).
        number_of_samples (Optional[int]): The number of samples in the lead's signal.
        signal (List[int]): The list of signal values
        ecg_id (Optional[int]): The ID of the associated ECG record.
        ecg (Optional[ECG]): The ECG record to which the lead belongs.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    identifier: str
    number_of_samples: Optional[int] = None
    signal: List[int] = Field(sa_column=Column(postgresql.ARRAY(Integer)))

    ecg_id: Optional[int] = Field(default=None, foreign_key="ecg.id")
    ecg: Optional["ECG"] = Relationship(back_populates="leads")


class ECG(SQLModel, table=True):
    """
    Represents an ECG record, which can have multiple leads.

    The ECG model stores information about the ECG record such as its ID, date,
    and associated leads. Each ECG can have multiple Leads, and the relationship
    is handled through the 'leads' attribute.

    Attributes:
        id (Optional[int]): The unique identifier of the ECG record.
        date (datetime): The date and time when the ECG was recorded.
        leads (List[Lead]): The list of Lead objects associated with this ECG.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    date: datetime = Field(default_factory=datetime.now)
    leads: List[Lead] = Relationship(back_populates="ecg")
    user_id: int = Field(foreign_key="user.id")

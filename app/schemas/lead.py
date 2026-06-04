from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Extra, Field, validator

from app.core.constants import (COMMENT_MAX_LEN, COMPANY_MAX_LEN,
                                COMPANY_MIN_LEN, NAME_MAX_LEN, NAME_MIN_LEN,
                                PHONE_MAX_LEN, PHONE_MIN_LEN)


class LeadBase(BaseModel):
    name: Optional[str] = Field(
        None, min_length=NAME_MIN_LEN, max_length=NAME_MAX_LEN
    )
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(
        None, min_length=PHONE_MIN_LEN, max_length=PHONE_MAX_LEN
    )
    company: Optional[str] = Field(
        None, min_length=COMPANY_MIN_LEN, max_length=COMPANY_MAX_LEN
    )
    comment: Optional[str] = Field(None, max_length=COMMENT_MAX_LEN)
    consent: Optional[bool] = None


class LeadCreate(LeadBase):
    name: str = Field(..., min_length=NAME_MIN_LEN, max_length=NAME_MAX_LEN)
    company: str = Field(
        ..., min_length=COMPANY_MIN_LEN, max_length=COMPANY_MAX_LEN
    )
    consent: bool = Field(...)

    @validator("phone", always=True)
    def email_or_phone_required(cls, value: Optional[str], values):
        if not value and not values.get("email"):
            raise ValueError("Укажите email или телефон.")
        return value

    @validator("consent")
    def consent_is_required(cls, value: bool):
        if value is not True:
            raise ValueError("Нужно согласие на обработку данных.")
        return value

    class Config:
        extra = Extra.forbid


class LeadDB(LeadCreate):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True

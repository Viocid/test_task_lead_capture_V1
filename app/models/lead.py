from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, String, Text

from app.core.constants import (COMMENT_MAX_LEN, COMPANY_MAX_LEN,
                                CONTACT_MAX_LEN, NAME_MAX_LEN, PHONE_MAX_LEN)
from app.core.db import Base


class Lead(Base):
    name = Column(String(NAME_MAX_LEN), nullable=False)
    email = Column(String(CONTACT_MAX_LEN), nullable=True)
    phone = Column(String(PHONE_MAX_LEN), nullable=True)
    company = Column(String(COMPANY_MAX_LEN), nullable=False)
    comment = Column(Text(COMMENT_MAX_LEN), nullable=True)
    consent = Column(Boolean, nullable=False)
    create_date = Column(DateTime, default=datetime.now, index=True)

    def __repr__(self) -> str:
        contact = self.email or self.phone
        return f'Заявка от "{self.name}" ({contact})'

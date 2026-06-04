from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field, model_validator

DATA_FILE = Path("data/leads.json")
DATA_FILE.parent.mkdir(exist_ok=True)
if not DATA_FILE.exists():
    DATA_FILE.write_text("[]", encoding="utf-8")

write_lock = Lock()

app = FastAPI(title="Alakris Lead Capture Prototype")


class LeadCreate(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, min_length=5, max_length=30)
    company: str = Field(min_length=2, max_length=120)
    comment: str | None = Field(default=None, max_length=1000)
    consent: Literal[True]

    @model_validator(mode="after")
    def email_or_phone_required(self):
        if not self.email and not self.phone:
            raise ValueError("Укажите email или телефон")
        return self


class Lead(LeadCreate):
    id: int
    created_at: str


def read_leads() -> list[dict]:
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def write_leads(leads: list[dict]) -> None:
    DATA_FILE.write_text(
        json.dumps(leads, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


@app.post("/api/leads", response_model=Lead, status_code=201)
def create_lead(payload: LeadCreate):
    with write_lock:
        leads = read_leads()
        next_id = max((lead["id"] for lead in leads), default=0) + 1
        lead = {
            "id": next_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            **payload.model_dump(),
        }
        leads.append(lead)
        write_leads(leads)
        return lead


@app.get("/api/leads", response_model=list[Lead])
def list_leads():
    leads = read_leads()
    return sorted(leads, key=lambda item: item["created_at"], reverse=True)


@app.get("/health")
def health():
    return {"status": "ok"}

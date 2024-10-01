from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from uuid import UUID

class Mail(BaseModel):
    mail_id: str

    class Config:
        orm_mode = True

class MailCreate(Mail):
    user_id: str
    title: Optional[str] = None
    body: Optional[str] = None
    your_name: Optional[str] = None
    your_mail_address: Optional[str] = None
    ai_answer: Optional[str] = None
    answer: Optional[str] = None
    rank: Optional[str] = None
    send_time: Optional[str] = None
    send_flag: Optional[bool] = False

class MailAllResponse(Mail):
    title: str
    body: str
    your_name: str
    your_mail_address:str
    rank: str
    send_time: str
    send_flag: Optional[bool]


class MailDetail(Mail):
    title: str
    body: str
    your_name: str
    your_mail_address:str
    ai_answer: Optional[str] = None
    rank: str
    send_time: str

class MailSendRequest(Mail):
    your_mail_address: str
    title: str
    body: str
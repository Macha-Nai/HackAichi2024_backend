from database import Base
from sqlalchemy import Column, String, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType
from uuid import uuid4
from .mixins import TimestampMixin


class Mail(Base, TimestampMixin):
    __tablename__ = 'mails'

    mail_id = Column(String(1024), nullable=False,
                     primary_key=True, server_default="ogrojojo332nk")
    user_id = Column(String(1024), nullable=False, server_default="3")
    title = Column(String(1024), nullable=True, server_default="質問のタイトル")
    body = Column(Text, nullable=True, server_default="質問の本文")
    your_name = Column(String(1024), nullable=True, server_default="送ってきた名前")
    your_mail_address = Column(
        String(1024), nullable=True, server_default="example@example.com")
    ai_answer = Column(Text, nullable=True, server_default="AIに投げた回答")
    answer = Column(Text, nullable=True, server_default="実際に回答した内容")
    rank = Column(String(1024), nullable=True, server_default="1")
    send_time = Column(String(1024), nullable=True, server_default="1798")
    send_flag = Column(Boolean, nullable=True, server_default="1")

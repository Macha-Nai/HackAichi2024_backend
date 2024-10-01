from fastapi import HTTPException
from models import Mail
from sqlalchemy.orm import Session
from schemas import mail
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64


def get_message_by_mail_id(db: Session, mail_id: str):
    return db.query(Mail).filter(Mail.mail_id == mail_id).first()

def create_message(db: Session, message: mail.MailCreate):
    db_message = Mail(
        mail_id = message.mail_id,
        user_id = message.user_id,
        title = message.title,
        your_name = message.your_name,
        your_mail_address =  message.your_mail_address,
        body = message.body,
        send_time = message.send_time,
        rank = message.rank,
        send_flag = False,
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)

def get_message_by_user_id(db: Session, user_id: str):
     skip = 0
     limit = 100
     return db.query(Mail).filter(Mail.user_id == user_id).offset(skip).limit(limit).all()

def send_mail_by_access_token(message: mail.MailSendRequest, access_token: str):
    try:
        creds = Credentials(token=access_token)
        service = build('gmail', 'v1', credentials=creds)
        message = create_mail(message.your_mail_address, message.title,message.body)
        sent_message = service.users().messages().send(userId='me', body=message).execute()
        return {"message_id": sent_message['id']}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def create_mail(to, subject, body):
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw}

def save_answer_by_access_token(db: Session, mail_id: str, answer: str):
    mail: Mail = db.query(Mail).get(mail_id)
    mail.answer = answer
    db.commit()
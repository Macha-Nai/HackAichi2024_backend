import cruds.user as crud
from database import get_db
from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy.orm import Session
from typing import List
from schemas.mail import MailAllResponse as MailAllResponseSchema, MailDetail as MailDetailSchema, MailCreate as MailCreateSchema, MailSendRequest as MailSendRequestSchema
import cruds.mail as crud_mail
import cruds.mail_send_flag as crud_send_flag
from app.cruds.mail_send_flag import store_send_flag_by_mail_id as store_send_flag
import app.cruds.login as login
from app.cruds.chatgpt import get_email_importance
from fastapi.responses import RedirectResponse
from app.cruds import google_api



router = APIRouter()

@router.get('/all', response_model=List[MailAllResponseSchema])
async def get_message_by_user_id(request: Request, db: Session = Depends(get_db), user_id="3"):
    access_token = request.cookies.get("access_token")
    if access_token:
        mail_list = login.get_all_emails(access_token)
        for mail in mail_list:
            db_mail = crud_mail.get_message_by_mail_id(db, mail_id=mail[0])
            if db_mail:
                pass
            else:
                rank = get_email_importance(mail[4])
                rank = str(rank)
                mail_create = MailCreateSchema(
                    mail_id = mail[0],
                    user_id = "3",
                    title = mail[1],
                    your_name = mail[2],
                    your_mail_address = mail[3],
                    body = mail[4],
                    send_time = mail[5],
                    rank = rank,
                )
                crud_mail.create_message(db, mail_create)
        return crud_mail.get_message_by_user_id(db=db, user_id=user_id)
    response = google_api.auth()
    return response



@router.get('/{mail_id}', response_model=MailDetailSchema)
async def read_user(mail_id: str, db: Session = Depends(get_db)):
    return crud_mail.get_message_by_mail_id(db=db, mail_id=mail_id)


@router.get('/{mail_id}/send_flag')
async def store_send_flag_by_mail_id(mail_id: str, db: Session = Depends(get_db)):
    store_send_flag(db=db, mail_id=mail_id)
    return Response(status_code=status.HTTP_200_OK)

@router.post('/send')
async def send_mail_by_access_token(request: Request, message: MailSendRequestSchema, db: Session = Depends(get_db)):
    access_token = request.cookies.get("access_token")
    crud_mail.send_mail_by_access_token(message, access_token)
    store_send_flag(db=db, mail_id=message.mail_id)
    crud_mail.save_answer_by_access_token(db=db, mail_id=message.mail_id, answer=message.body)
    return Response(status_code=status.HTTP_200_OK)


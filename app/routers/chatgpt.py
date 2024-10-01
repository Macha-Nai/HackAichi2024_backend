from fastapi import APIRouter, Depends
from schemas.chatgpt import Chatgpt as ChatgptSchema
from app.cruds.chatgpt import generate_email_reply, get_reply, save_answer, is_ai_answered, get_title_and_content, get_ai_answer
from app.cruds.rag import get_similar_mail_id
from sqlalchemy.orm import Session
from database import get_db


router = APIRouter()


@router.get("/chatgpt/{mail_id}", response_model=ChatgptSchema)
async def read_users(mail_id: str, db: Session = Depends(get_db)):
    if is_ai_answered(db, mail_id):
        return ChatgptSchema(
            text=get_ai_answer(db, mail_id),
        )
    title, content = get_title_and_content(db, mail_id)
    similar_mail_id = get_similar_mail_id(title, content)
    past_mail_answer = get_reply(db, similar_mail_id)
    reply = generate_email_reply(content, past_mail_answer)
    save_answer(db, mail_id, reply)
    return ChatgptSchema(
        text=reply,
    )

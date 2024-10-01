from sqlalchemy.orm import Session
from models import Mail

def store_send_flag_by_mail_id(db: Session, mail_id: str):
    mail_id = mail_id.replace('"', "")
    item: Mail = db.query(Mail).get(mail_id)
    item.send_flag = True
    db.commit()

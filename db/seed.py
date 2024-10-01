from database import SessionLocal
from models import Mail
import csv

db = SessionLocal()


def seed():
    mails = []
    with open('./output.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            mail = Mail(mail_id=row[0], user_id="333", body=row[1], answer=row[2])
            mails.append(mail)
    db.add_all(mails)
    db.commit()


if __name__ == '__main__':
    BOS = '\033[92m'
    EOS = '\033[0m'

    print(f'{BOS}Seeding data...{EOS}')
    seed()

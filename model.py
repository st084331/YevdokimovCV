from pathlib import Path
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from config import SQLITE_DATABASE_NAME, SQLITE_DATABASE_BACKUP_NAME
import shutil

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512), nullable=False)
    text = db.Column(db.String(2048), nullable=False)
    created_on = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_on = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), server_onupdate=db.func.now())

def db_init():
    guestbook_init = [{'name' : 'Данил', 'text' : 'Вы на дне!'}]
    db_file = Path(SQLITE_DATABASE_NAME)
    if db_file.is_file():
        shutil.copyfile(SQLITE_DATABASE_NAME, SQLITE_DATABASE_BACKUP_NAME)

    # Init DB
    db.session.commit()  # https://stackoverflow.com/questions/24289808/drop-all-freezes-in-flask-with-sqlalchemy
    db.drop_all()
    db.create_all()

    print("Create Guestbook")
    for q in guestbook_init:
        gb = Post(name=q['name'], text=q['text'])
        db.session.add(gb)
        db.session.commit()
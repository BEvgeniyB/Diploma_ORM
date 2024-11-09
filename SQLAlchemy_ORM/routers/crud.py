from sqlalchemy.orm import Session
from models import Task,User



def create_db(db:Session,creates_user):
    db_user = User(username=creates_user.username,firstname=creates_user.firstname,
                   lastname=creates_user.lastname,age=creates_user.age)
    db.add(db_user)
    db.commit()
    return "Successful"
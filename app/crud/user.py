from sqlalchemy.orm import Session
from app.models.user import User

def get_user_by_username(db: Session, username: str):
    if db is None or not isinstance(db, Session):
        return None
    if not isinstance(username, str) or not username.strip():
        return None
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user):
    if not db or not user:
        return None
    try:
        db_user = User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise e

def get_user(db: Session, user_id: int):
    if not db or not isinstance(user_id, int):
        return None
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    if not db:
        return []
    if not isinstance(skip, int) or not isinstance(limit, int):
        skip, limit = 0, 100
    return db.query(User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, user):
    if not db or not user_id or not user:
        return None
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            for key, value in user.dict().items():
                setattr(db_user, key, value)
            db.commit()
            db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise e

def delete_user(db: Session, user_id: int):
    if not db or not isinstance(user_id, int):
        return None
    try:
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user:
            db.delete(db_user)
            db.commit()
        return db_user
    except Exception as e:
        db.rollback()
        raise e
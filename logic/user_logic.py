from sqlalchemy.orm import Session
from models import User
from DTOs.user_dto import UserDTO, CreateUserDTO
from mapper import map_to_dto, map_to_model, update_model_from_dto


class UserService:
    @staticmethod
    def create_user(db: Session, user_data: CreateUserDTO) -> UserDTO:
        user = map_to_model(user_data, User)
        db.add(user)
        db.commit()
        db.refresh(user)
        return map_to_dto(user, UserDTO)

    @staticmethod
    def get_user(db: Session, user_id: int) -> UserDTO | None:
        user = db.query(User).filter(User.id == user_id).first()
        return map_to_dto(user, UserDTO) if user else None

    @staticmethod
    def get_all_users(db: Session) -> list[UserDTO]:
        users = db.query(User).all()
        return [map_to_dto(u, UserDTO) for u in users]

    @staticmethod
    def update_user(
        db: Session, user_id: int, user_data: CreateUserDTO
    ) -> UserDTO | None:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        user = update_model_from_dto(user, user_data)
        db.commit()
        db.refresh(user)
        return map_to_dto(user, UserDTO)

    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        db.delete(user)
        db.commit()
        return True

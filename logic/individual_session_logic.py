from sqlalchemy.orm import Session
from models import IndividualSession
from DTOs.individual_session_dto import IndividualSessionDTO, CreateIndividualSessionDTO, UpdateIndividualSessionDTO
from mapper import map_to_dto, map_to_model, update_model_from_dto


class IndividualSessionService:
    @staticmethod
    def create_session(
        db: Session, session_data: CreateIndividualSessionDTO
    ) -> IndividualSessionDTO:
        session_obj = map_to_model(session_data, IndividualSession)
        db.add(session_obj)
        db.commit()
        db.refresh(session_obj)
        return map_to_dto(session_obj, IndividualSessionDTO)

    @staticmethod
    def get_session(db: Session, session_id: int) -> IndividualSessionDTO | None:
        session_obj = (
            db.query(IndividualSession)
            .filter(IndividualSession.id == session_id)
            .first()
        )
        return map_to_dto(session_obj, IndividualSessionDTO) if session_obj else None

    @staticmethod
    def get_all_sessions(db: Session) -> list[IndividualSessionDTO]:
        sessions = db.query(IndividualSession).all()
        return [map_to_dto(s, IndividualSessionDTO) for s in sessions]

    @staticmethod
    def update_session(
        db: Session, session_id: int, session_data: UpdateIndividualSessionDTO
    ) -> IndividualSessionDTO | None:
        session_obj = (
            db.query(IndividualSession)
            .filter(IndividualSession.id == session_id)
            .first()
        )
        if not session_obj:
            return None
        session_obj = update_model_from_dto(session_obj, session_data)
        db.commit()
        db.refresh(session_obj)
        return map_to_dto(session_obj, IndividualSessionDTO)

    @staticmethod
    def delete_session(db: Session, session_id: int) -> bool:
        session_obj = (
            db.query(IndividualSession)
            .filter(IndividualSession.id == session_id)
            .first()
        )
        if not session_obj:
            return False
        db.delete(session_obj)
        db.commit()
        return True

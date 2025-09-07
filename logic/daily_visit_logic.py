from sqlalchemy.orm import Session
from DTOs.daily_finance_dto import UpdateDailyVisitDTO
from models import DailyVisit
from DTOs.daily_visit_dto import DailyVisitDTO, CreateDailyVisitDTO
from mapper import map_to_dto, map_to_model, update_model_from_dto


class DailyVisitService:
    @staticmethod
    def create_visit(db: Session, visit_data: CreateDailyVisitDTO) -> DailyVisitDTO:
        visit = map_to_model(visit_data, DailyVisit)
        db.add(visit)
        db.commit()
        db.refresh(visit)
        return map_to_dto(visit, DailyVisitDTO)

    @staticmethod
    def get_visit(db: Session, visit_id: int) -> DailyVisitDTO | None:
        visit = db.query(DailyVisit).filter(DailyVisit.id == visit_id).first()
        return map_to_dto(visit, DailyVisitDTO) if visit else None

    @staticmethod
    def get_all_visits(db: Session) -> list[DailyVisitDTO]:
        visits = db.query(DailyVisit).all()
        return [map_to_dto(v, DailyVisitDTO) for v in visits]

    @staticmethod
    def update_visit(
        db: Session, visit_id: int, visit_data: UpdateDailyVisitDTO
    ) -> DailyVisitDTO | None:
        visit = db.query(DailyVisit).filter(DailyVisit.id == visit_id).first()
        if not visit:
            return None
        visit = update_model_from_dto(visit, visit_data)
        db.commit()
        db.refresh(visit)
        return map_to_dto(visit, DailyVisitDTO)

    @staticmethod
    def delete_visit(db: Session, visit_id: int) -> bool:
        visit = db.query(DailyVisit).filter(DailyVisit.id == visit_id).first()
        if not visit:
            return False
        db.delete(visit)
        db.commit()
        return True

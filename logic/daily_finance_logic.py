from sqlalchemy.orm import Session
from models import DailyFinance
from DTOs.daily_finance_dto import (
    DailyFinanceDTO,
    CreateDailyFinanceDTO,
    UpdateDailyFinanceDTO,
)
from mapper import map_to_dto, map_to_model, update_model_from_dto


class DailyFinanceService:
    @staticmethod
    def create_finance(
        db: Session, finance_data: CreateDailyFinanceDTO
    ) -> DailyFinanceDTO:
        finance = map_to_model(finance_data, DailyFinance)
        db.add(finance)
        db.commit()
        db.refresh(finance)
        return map_to_dto(finance, DailyFinanceDTO)

    @staticmethod
    def get_finance(db: Session, finance_id: int) -> DailyFinanceDTO | None:
        finance = db.query(DailyFinance).filter(DailyFinance.id == finance_id).first()
        return map_to_dto(finance, DailyFinanceDTO) if finance else None

    @staticmethod
    def get_all_finances(db: Session) -> list[DailyFinanceDTO]:
        finances = db.query(DailyFinance).all()
        return [map_to_dto(f, DailyFinanceDTO) for f in finances]

    @staticmethod
    def update_finance(
        db: Session, finance_id: int, finance_data: UpdateDailyFinanceDTO
    ) -> DailyFinanceDTO | None:
        finance = db.query(DailyFinance).filter(DailyFinance.id == finance_id).first()
        if not finance:
            return None
        finance = update_model_from_dto(finance, finance_data)
        db.commit()
        db.refresh(finance)
        return map_to_dto(finance, DailyFinanceDTO)

    @staticmethod
    def delete_finance(db: Session, finance_id: int) -> bool:
        finance = db.query(DailyFinance).filter(DailyFinance.id == finance_id).first()
        if not finance:
            return False
        db.delete(finance)
        db.commit()
        return True

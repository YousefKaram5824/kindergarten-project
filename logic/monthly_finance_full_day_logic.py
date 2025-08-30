from sqlalchemy.orm import Session
from models import MonthlyFinanceFullDay
from DTOs.monthly_finance_full_day_dto import (
    MonthlyFinanceFullDayDTO,
    CreateMonthlyFinanceFullDayDTO,
)
from mapper import map_to_dto, map_to_model, update_model_from_dto


class MonthlyFinanceFullDayService:
    @staticmethod
    def create_monthly(
        db: Session, data: CreateMonthlyFinanceFullDayDTO
    ) -> MonthlyFinanceFullDayDTO:
        month = map_to_model(data, MonthlyFinanceFullDay)
        db.add(month)
        db.commit()
        db.refresh(month)
        return map_to_dto(month, MonthlyFinanceFullDayDTO)

    @staticmethod
    def get_monthly(db: Session, month_id: int) -> MonthlyFinanceFullDayDTO | None:
        month = (
            db.query(MonthlyFinanceFullDay)
            .filter(MonthlyFinanceFullDay.id == month_id)
            .first()
        )
        return map_to_dto(month, MonthlyFinanceFullDayDTO) if month else None

    @staticmethod
    def get_all_monthly(db: Session) -> list[MonthlyFinanceFullDayDTO]:
        months = db.query(MonthlyFinanceFullDay).all()
        return [map_to_dto(m, MonthlyFinanceFullDayDTO) for m in months]

    @staticmethod
    def update_monthly(
        db: Session, month_id: int, data: CreateMonthlyFinanceFullDayDTO
    ) -> MonthlyFinanceFullDayDTO | None:
        month = (
            db.query(MonthlyFinanceFullDay)
            .filter(MonthlyFinanceFullDay.id == month_id)
            .first()
        )
        if not month:
            return None
        month = update_model_from_dto(month, data)
        db.commit()
        db.refresh(month)
        return map_to_dto(month, MonthlyFinanceFullDayDTO)

    @staticmethod
    def delete_monthly(db: Session, month_id: int) -> bool:
        month = (
            db.query(MonthlyFinanceFullDay)
            .filter(MonthlyFinanceFullDay.id == month_id)
            .first()
        )
        if not month:
            return False
        db.delete(month)
        db.commit()
        return True

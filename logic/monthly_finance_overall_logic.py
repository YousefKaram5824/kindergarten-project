from sqlalchemy.orm import Session
from models import MonthlyFinanceOverall
from DTOs.monthly_finance_overall_dto import (
    MonthlyFinanceOverallDTO,
    CreateMonthlyFinanceOverallDTO,
    UpdateMonthlyFinanceOverallDTO,
)
from mapper import map_to_dto, map_to_model, update_model_from_dto


class MonthlyFinanceOverallService:
    @staticmethod
    def create_monthly(
        db: Session, data: CreateMonthlyFinanceOverallDTO
    ) -> MonthlyFinanceOverallDTO:
        month = map_to_model(data, MonthlyFinanceOverall)
        db.add(month)
        db.commit()
        db.refresh(month)
        return map_to_dto(month, MonthlyFinanceOverallDTO)

    @staticmethod
    def get_monthly(db: Session, month_id: int) -> MonthlyFinanceOverallDTO | None:
        month = (
            db.query(MonthlyFinanceOverall)
            .filter(MonthlyFinanceOverall.id == month_id)
            .first()
        )
        return map_to_dto(month, MonthlyFinanceOverallDTO) if month else None

    @staticmethod
    def get_all_monthly(db: Session) -> list[MonthlyFinanceOverallDTO]:
        months = db.query(MonthlyFinanceOverall).all()
        return [map_to_dto(m, MonthlyFinanceOverallDTO) for m in months]

    @staticmethod
    def update_monthly(
        db: Session, month_id: int, data: UpdateMonthlyFinanceOverallDTO
    ) -> MonthlyFinanceOverallDTO | None:
        month = (
            db.query(MonthlyFinanceOverall)
            .filter(MonthlyFinanceOverall.id == month_id)
            .first()
        )
        if not month:
            return None
        month = update_model_from_dto(month, data)
        db.commit()
        db.refresh(month)
        return map_to_dto(month, MonthlyFinanceOverallDTO)

    @staticmethod
    def delete_monthly(db: Session, month_id: int) -> bool:
        month = (
            db.query(MonthlyFinanceOverall)
            .filter(MonthlyFinanceOverall.id == month_id)
            .first()
        )
        if not month:
            return False
        db.delete(month)
        db.commit()
        return True

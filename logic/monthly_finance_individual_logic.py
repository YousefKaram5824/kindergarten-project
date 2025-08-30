from sqlalchemy.orm import Session
from models import MonthlyFinanceIndividual
from DTOs.monthly_finance_individual_dto import (
    MonthlyFinanceIndividualDTO,
    CreateMonthlyFinanceIndividualDTO,
)
from mapper import map_to_dto, map_to_model, update_model_from_dto


class MonthlyFinanceIndividualService:
    @staticmethod
    def create_monthly(
        db: Session, data: CreateMonthlyFinanceIndividualDTO
    ) -> MonthlyFinanceIndividualDTO:
        month = map_to_model(data, MonthlyFinanceIndividual)
        db.add(month)
        db.commit()
        db.refresh(month)
        return map_to_dto(month, MonthlyFinanceIndividualDTO)

    @staticmethod
    def get_monthly(db: Session, month_id: int) -> MonthlyFinanceIndividualDTO | None:
        month = (
            db.query(MonthlyFinanceIndividual)
            .filter(MonthlyFinanceIndividual.id == month_id)
            .first()
        )
        return map_to_dto(month, MonthlyFinanceIndividualDTO) if month else None

    @staticmethod
    def get_all_monthly(db: Session) -> list[MonthlyFinanceIndividualDTO]:
        months = db.query(MonthlyFinanceIndividual).all()
        return [map_to_dto(m, MonthlyFinanceIndividualDTO) for m in months]

    @staticmethod
    def update_monthly(
        db: Session, month_id: int, data: CreateMonthlyFinanceIndividualDTO
    ) -> MonthlyFinanceIndividualDTO | None:
        month = (
            db.query(MonthlyFinanceIndividual)
            .filter(MonthlyFinanceIndividual.id == month_id)
            .first()
        )
        if not month:
            return None
        month = update_model_from_dto(month, data)
        db.commit()
        db.refresh(month)
        return map_to_dto(month, MonthlyFinanceIndividualDTO)

    @staticmethod
    def delete_monthly(db: Session, month_id: int) -> bool:
        month = (
            db.query(MonthlyFinanceIndividual)
            .filter(MonthlyFinanceIndividual.id == month_id)
            .first()
        )
        if not month:
            return False
        db.delete(month)
        db.commit()
        return True

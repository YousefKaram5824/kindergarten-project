from sqlalchemy.orm import Session
from models import UniformForSale
from DTOs.uniform_for_sale_dto import UniformForSaleDTO, CreateUniformForSaleDTO
from mapper import map_to_dto, map_to_model, update_model_from_dto


class UniformForSaleService:
    @staticmethod
    def create_uniform(
        db: Session, uniform_data: CreateUniformForSaleDTO
    ) -> UniformForSaleDTO:
        uniform = map_to_model(uniform_data, UniformForSale)
        db.add(uniform)
        db.commit()
        db.refresh(uniform)
        return map_to_dto(uniform, UniformForSaleDTO)

    @staticmethod
    def get_uniform(db: Session, uniform_id: int) -> UniformForSaleDTO | None:
        uniform = (
            db.query(UniformForSale).filter(UniformForSale.id == uniform_id).first()
        )
        return map_to_dto(uniform, UniformForSaleDTO) if uniform else None

    @staticmethod
    def get_all_uniforms(db: Session) -> list[UniformForSaleDTO]:
        uniforms = db.query(UniformForSale).all()
        return [map_to_dto(u, UniformForSaleDTO) for u in uniforms]

    @staticmethod
    def update_uniform(
        db: Session, uniform_id: int, uniform_data: CreateUniformForSaleDTO
    ) -> UniformForSaleDTO | None:
        uniform = (
            db.query(UniformForSale).filter(UniformForSale.id == uniform_id).first()
        )
        if not uniform:
            return None
        uniform = update_model_from_dto(uniform, uniform_data)
        db.commit()
        db.refresh(uniform)
        return map_to_dto(uniform, UniformForSaleDTO)

    @staticmethod
    def delete_uniform(db: Session, uniform_id: int) -> bool:
        uniform = (
            db.query(UniformForSale).filter(UniformForSale.id == uniform_id).first()
        )
        if not uniform:
            return False
        db.delete(uniform)
        db.commit()
        return True

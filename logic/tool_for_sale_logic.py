from sqlalchemy.orm import Session
from models import ToolForSale
from DTOs.tool_for_sale_dto import ToolForSaleDTO, CreateToolForSaleDTO
from mapper import map_to_dto, map_to_model, update_model_from_dto

class ToolForSaleService:
    @staticmethod
    def create_tool(db: Session, tool_data: CreateToolForSaleDTO) -> ToolForSaleDTO:
        tool = map_to_model(tool_data, ToolForSale)
        db.add(tool)
        db.commit()
        db.refresh(tool)
        return map_to_dto(tool, ToolForSaleDTO)

    @staticmethod
    def get_tool(db: Session, tool_id: int) -> ToolForSaleDTO | None:
        tool = db.query(ToolForSale).filter(ToolForSale.id == tool_id).first()
        return map_to_dto(tool, ToolForSaleDTO) if tool else None

    @staticmethod
    def get_all_tools(db: Session) -> list[ToolForSaleDTO]:
        tools = db.query(ToolForSale).all()
        return [map_to_dto(t, ToolForSaleDTO) for t in tools]

    @staticmethod
    def update_tool(db: Session, tool_id: int, tool_data: CreateToolForSaleDTO) -> ToolForSaleDTO | None:
        tool = db.query(ToolForSale).filter(ToolForSale.id == tool_id).first()
        if not tool:
            return None
        tool = update_model_from_dto(tool, tool_data)
        db.commit()
        db.refresh(tool)
        return map_to_dto(tool, ToolForSaleDTO)

    @staticmethod
    def delete_tool(db: Session, tool_id: int) -> bool:
        tool = db.query(ToolForSale).filter(ToolForSale.id == tool_id).first()
        if not tool:
            return False
        db.delete(tool)
        db.commit()
        return True

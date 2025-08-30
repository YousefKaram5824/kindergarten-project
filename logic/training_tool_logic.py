from sqlalchemy.orm import Session
from models import TrainingTool
from DTOs.training_tool_dto import TrainingToolDTO, CreateTrainingToolDTO
from mapper import map_to_dto, map_to_model, update_model_from_dto


class TrainingToolService:
    @staticmethod
    def create_tool(db: Session, tool_data: CreateTrainingToolDTO) -> TrainingToolDTO:
        tool = map_to_model(tool_data, TrainingTool)
        db.add(tool)
        db.commit()
        db.refresh(tool)
        return map_to_dto(tool, TrainingToolDTO)

    @staticmethod
    def get_tool(db: Session, tool_id: int) -> TrainingToolDTO | None:
        tool = db.query(TrainingTool).filter(TrainingTool.id == tool_id).first()
        return map_to_dto(tool, TrainingToolDTO) if tool else None

    @staticmethod
    def get_all_tools(db: Session) -> list[TrainingToolDTO]:
        tools = db.query(TrainingTool).all()
        return [map_to_dto(t, TrainingToolDTO) for t in tools]

    @staticmethod
    def update_tool(
        db: Session, tool_id: int, tool_data: CreateTrainingToolDTO
    ) -> TrainingToolDTO | None:
        tool = db.query(TrainingTool).filter(TrainingTool.id == tool_id).first()
        if not tool:
            return None
        tool = update_model_from_dto(tool, tool_data)
        db.commit()
        db.refresh(tool)
        return map_to_dto(tool, TrainingToolDTO)

    @staticmethod
    def delete_tool(db: Session, tool_id: int) -> bool:
        tool = db.query(TrainingTool).filter(TrainingTool.id == tool_id).first()
        if not tool:
            return False
        db.delete(tool)
        db.commit()
        return True

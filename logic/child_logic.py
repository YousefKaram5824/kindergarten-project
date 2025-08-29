from sqlalchemy.orm import Session
from models import Child
from DTOs.child_dto import ChildDTO, CreateChildDTO
from mapper import map_to_dto, map_to_model, update_model_from_dto

class ChildService:
    @staticmethod
    def create_child(db: Session, child_data: CreateChildDTO) -> ChildDTO:
        child = map_to_model(child_data, Child)
        db.add(child)
        db.commit()
        db.refresh(child)
        return map_to_dto(child, ChildDTO)

    @staticmethod
    def get_all_children(db: Session) -> list[ChildDTO]:
        children = db.query(Child).all()
        return [map_to_dto(c, ChildDTO) for c in children]
    
    @staticmethod
    def update_child(db: Session, child_id: int, child_data: CreateChildDTO) -> ChildDTO | None:
        child = db.query(Child).filter(Child.id == child_id).first()
        if not child:
            return None
        # 
        update_model_from_dto(child, child_data)
        db.commit()
        db.refresh(child)
        return map_to_dto(child, ChildDTO)


    @staticmethod
    def delete_child(db: Session, child_id: int) -> bool:
        child = db.query(Child).filter(Child.id == child_id).first()
        if not child:
            return False
        db.delete(child)
        db.commit()
        return True

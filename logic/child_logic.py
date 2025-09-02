from sqlalchemy.orm import Session
from models import Child, ChildTypeEnum
from DTOs.child_dto import ChildDTO, CreateChildDTO
from mapper import map_to_dto, map_to_model, update_model_from_dto
from sqlalchemy.exc import IntegrityError as SQLAlchemyIntegrityError
import datetime



class ChildService:
    @staticmethod
    def create_child(db: Session, child_data: CreateChildDTO) -> ChildDTO:
        
        if not hasattr(child_data, "id") or child_data.id is None:
            raise ValueError("يجب إدخال الرقم التعريفي للطالب")
        if child_data.id <= 100:
            raise ValueError("الرقم التعريفي يجب أن يكون أكبر من 100")

        # (soft delete)
        existing = db.query(Child).filter(Child.id == child_data.id).first()
        if existing:
            raise ValueError(f"الرقم التعريفي {child_data.id} مستخدم من قبل")

        child = map_to_model(child_data, Child)
        # force is_deleted to False for new child
        if hasattr(child, "is_deleted"):
            child.is_deleted = False

        db.add(child)
        try:
            db.commit()
        except SQLAlchemyIntegrityError:
            db.rollback()
            raise ValueError("الرقم التعريفي مستخدم بالفعل أو هناك تعارض في قاعدة البيانات")
        db.refresh(child)
        return map_to_dto(child, ChildDTO)

    @staticmethod
    def get_all_children(db: Session) -> list[ChildDTO]:
        children = db.query(Child).filter(Child.is_deleted == False).all()
        return [map_to_dto(c, ChildDTO) for c in children]

    @staticmethod
    def update_child(
        db: Session, child_id: int, child_data: CreateChildDTO
    ) -> ChildDTO | None:
        child = db.query(Child).filter(Child.id == child_id,Child.is_deleted == False).first()
        if not child:
            return None
        #
        update_model_from_dto(child, child_data)
        child.updated_at = datetime.datetime.now() 
        db.commit()
        db.refresh(child)
        return map_to_dto(child, ChildDTO)

    @staticmethod
    def delete_child(db: Session, child_id: int) -> bool:
        child = db.query(Child).filter(Child.id == child_id, Child.is_deleted == False).first()
        if not child:
            return False
        child.is_deleted = True
        db.commit()
        return True

    @staticmethod
    def get_child_by_id(db: Session, child_id: int) -> ChildDTO | None:
        child = db.query(Child).filter(Child.id == child_id,Child.is_deleted == False).first()
        if not child:
            return None
        return map_to_dto(child, ChildDTO)

    @staticmethod
    def search_children(db: Session, query: str) -> list[ChildDTO]:
        if not query:
            return ChildService.get_all_children(db)

        # Search in name, phone_number, father_job, mother_job, notes
        search_filter = f"%{query}%"
        children = db.query(Child).filter(
            (Child.name.ilike(search_filter)) |
            (Child.phone_number.ilike(search_filter)) |
            (Child.father_job.ilike(search_filter)) |
            (Child.mother_job.ilike(search_filter)) |
            (Child.notes.ilike(search_filter))
        ).all()
        return [map_to_dto(c, ChildDTO) for c in children]

    @staticmethod
    def get_children_count_by_type(db: Session, child_type: ChildTypeEnum) -> int:
        """Get count of children by child type"""
        return db.query(Child).filter(Child.child_type == child_type).count()

    @staticmethod
    def get_full_day_children_count(db: Session) -> int:
        """Get count of full day children"""
        return ChildService.get_children_count_by_type(db, ChildTypeEnum.FULL_DAY)

    @staticmethod
    def get_sessions_children_count(db: Session) -> int:
        """Get count of sessions children"""
        return ChildService.get_children_count_by_type(db, ChildTypeEnum.SESSIONS)

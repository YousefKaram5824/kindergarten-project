from sqlalchemy.orm import Session
from models import FullDayProgram
from DTOs.full_day_program_dto import (
    FullDayProgramDTO,
    CreateFullDayProgramDTO,
    UpdateFullDayProgramDTO,
)
from mapper import map_to_dto, map_to_model, update_model_from_dto


class FullDayProgramService:
    @staticmethod
    def create_program(
        db: Session, program_data: CreateFullDayProgramDTO, child_id: int
    ) -> FullDayProgramDTO:
        program = map_to_model(program_data, FullDayProgram)
        program.child_id = child_id
        db.add(program)
        db.commit()
        db.refresh(program)
        return map_to_dto(program, FullDayProgramDTO)

    @staticmethod
    def get_program(db: Session, program_id: int) -> FullDayProgramDTO | None:
        program = (
            db.query(FullDayProgram).filter(FullDayProgram.id == program_id).first()
        )
        return map_to_dto(program, FullDayProgramDTO) if program else None

    @staticmethod
    def get_all_programs(db: Session) -> list[FullDayProgramDTO]:
        programs = db.query(FullDayProgram).all()
        return [map_to_dto(p, FullDayProgramDTO) for p in programs]

    @staticmethod
    def get_program_by_child_id(db: Session, child_id: int) -> FullDayProgramDTO | None:
        program = (
            db.query(FullDayProgram).filter(FullDayProgram.child_id == child_id).first()
        )
        return map_to_dto(program, FullDayProgramDTO) if program else None

    @staticmethod
    def update_program(
        db: Session, program_id: int, program_data: UpdateFullDayProgramDTO
    ) -> FullDayProgramDTO | None:
        program = (
            db.query(FullDayProgram).filter(FullDayProgram.id == program_id).first()
        )
        if not program:
            return None
        program = update_model_from_dto(program, program_data)
        db.commit()
        db.refresh(program)
        return map_to_dto(program, FullDayProgramDTO)

    @staticmethod
    def delete_program(db: Session, program_id: int) -> bool:
        program = (
            db.query(FullDayProgram).filter(FullDayProgram.id == program_id).first()
        )
        if not program:
            return False
        db.delete(program)
        db.commit()
        return True

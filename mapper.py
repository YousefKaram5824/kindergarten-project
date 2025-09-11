# logic/mapper.py
from typing import Type


def map_to_dto(model_instance, dto_class: Type):
    
    dto = dto_class.from_orm(model_instance)
    # Handle special fields for Child
    if dto_class.__name__ == 'ChildDTO' and hasattr(model_instance, 'full_day_program') and model_instance.full_day_program:
        dto.attendance_status = model_instance.full_day_program.attendance_status
    if dto_class.__name__ == 'ChildDTO' and hasattr(model_instance, 'individual_sessions'):
        attended_total = sum(s.attended_sessions_count or 0 for s in model_instance.individual_sessions)
        monthly_total = sum(s.monthly_sessions_count or 0 for s in model_instance.individual_sessions)
        dto.attended_sessions_total = attended_total if attended_total > 0 else None
        dto.monthly_sessions_total = monthly_total if monthly_total > 0 else None
    return dto
        
def map_to_model(dto_instance, model_class: Type):
    """حول DTO instance لـ Model"""
    return model_class(**dto_instance.dict())


def update_model_from_dto(model_instance, dto_instance):
    """حدث الـ Model بالـ DTO (exclude unset)"""
    for key, value in dto_instance.dict(exclude_unset=True).items():
        setattr(model_instance, key, value)
    return model_instance

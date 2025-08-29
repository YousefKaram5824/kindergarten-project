# logic/mapper.py
from typing import Type

def map_to_dto(model_instance, dto_class: Type):
    """حول Model instance لـ DTO"""
    return dto_class.from_orm(model_instance)

def map_to_model(dto_instance, model_class: Type):
    """حول DTO instance لـ Model"""
    return model_class(**dto_instance.dict())

def update_model_from_dto(model_instance, dto_instance):
    """حدث الـ Model بالـ DTO (exclude unset)"""
    for key, value in dto_instance.dict(exclude_unset=True).items():
        setattr(model_instance, key, value)
    return model_instance

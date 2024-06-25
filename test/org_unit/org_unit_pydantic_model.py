from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, validator

class OrgUnitPydanticModel(BaseModel):
    id_org_unit: UUID = Field(..., alias='ID организационной единицы')
    name_org_unit: str = Field(..., alias='Название организационной единицы', max_length=256)
    manager_id: Optional[UUID] = Field(None, alias='ID Руководителя этой организационной единицы')
    parent_org_unit_name: Optional[str] = Field(None, alias='Название вышестоящей организационной единицы', max_length=256)
    parent_org_unit_id: Optional[UUID] = Field(None, alias='ID вышестоящей организационной единицы')

    @validator('*', pre=True, allow_reuse=True)
    def strip_whitespace(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v
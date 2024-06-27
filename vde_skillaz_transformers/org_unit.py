from typing import Optional

from pydantic import BaseModel

class OrgUnitVde(BaseModel):
    orgunitid: str 
    name: str
    headid: Optional[str] = None
    heademail: Optional[str]
    address: Optional[str] = None
    superiorname: Optional[str] = None
    superiorid: Optional[str] 
        
    model_config = { 'str_strip_whitespace': True }


class OrgUnitSkillaz(BaseModel):
    Id: str
    Name: str

    model_config = { 'str_strip_whitespace': True }

def validate_vde_org_unit(record):
    validated = OrgUnitVde(**record)
    return validated

def transform_org_unit_vde_to_skillaz(record):
    vde_record = validate_vde_org_unit(record)
    skillaz_record = OrgUnitSkillaz(Id = vde_record.orgunitid, Name =
                                    vde_record.name) 
    return skillaz_record

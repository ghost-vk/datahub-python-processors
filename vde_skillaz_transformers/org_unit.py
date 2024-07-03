from typing import Any, Optional, TypedDict

from pydantic import BaseModel, EmailStr, ValidationError

from exceptions import TransformException

class OrgUnitVde(BaseModel):
    orgunitid: str 
    name: str
    headid: Optional[str] = None
    heademail: Optional[EmailStr] = None
    address: Optional[str] = None
    superiorname: Optional[str] = None
    superiorid: Optional[str] = None
    flowuuid: Optional[str] = None
        
    model_config = { 'str_strip_whitespace': True }

class OrgUnitVdeInsertReady(TypedDict):
    orgunitid: str 
    name: str
    headid: Optional[str]
    heademail: Optional[EmailStr]
    address: Optional[str]
    superiorname: Optional[str]
    superiorid: Optional[str]
    flowuuid: Optional[str]
    record_name: str

class OrgUnitVdeDbMeta(OrgUnitVde):
    id: str 
    record_name: Optional[str] = None
    default_order: Optional[int] = None

OrgUnitSkillazData = TypedDict('OrgUnitSkillazData', {
    'ExtraData.Manager': Optional[str]
})

class OrgUnitSkillaz(TypedDict):
    Id: str
    ExternalId: str
    Name: str
    ParentId: Optional[str]
    Address: Optional[str]
    IsArchived: bool
    Data: OrgUnitSkillazData

def transform_org_unit_vde_to_skillaz(record: dict[str, Any]) -> OrgUnitSkillaz:
    try:
        validated = OrgUnitVdeDbMeta(**record)
        skillaz_record: OrgUnitSkillaz = {
            'Id': validated.orgunitid,
            'ExternalId': validated.orgunitid,
            'Name': validated.name,
            'ParentId': validated.superiorid,
            'Address': validated.address,
            'IsArchived': False,
            'Data': {
                'ExtraData.Manager': validated.heademail,
            },
        }
        return skillaz_record 
    except ValidationError:
        raise TransformException

def transform_ort_unit_insert(record: dict[str, Any]) -> OrgUnitVdeInsertReady:
    try:
        validated = OrgUnitVde(**record)    
        insert_record: OrgUnitVdeInsertReady = {
            'record_name': validated.name,
            'orgunitid': validated.orgunitid,
            'name': validated.name,
            'headid': validated.headid,
            'heademail': validated.heademail,
            'address': validated.address,
            'superiorname': validated.superiorname,
            'superiorid': validated.superiorid,
            'flowuuid': validated.flowuuid,
        }
        return insert_record
    except ValidationError:
        raise TransformException

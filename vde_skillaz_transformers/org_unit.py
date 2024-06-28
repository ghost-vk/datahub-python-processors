from typing import Optional

from pydantic import BaseModel, EmailStr

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

class OrgUnitVdeDbMeta(OrgUnitVde):
    id: str 
    record_name: Optional[str] = None
    default_order: Optional[int] = None

def validate_vde_org_unit_db_meta(record):
    validated = OrgUnitVdeDbMeta(**record)
    return validated

def transform_org_unit_vde_to_skillaz(record):
    vde_record = validate_vde_org_unit_db_meta(record)
    skillaz_record = {
        'Id': vde_record.orgunitid,
        'ExternalId': vde_record.orgunitid,
        'Name': vde_record.name,
        'ParentId': vde_record.superiorid,
        'Address': vde_record.address,
        'IsArchived': False,
        'Data': {
            'ExtraData.Manager': vde_record.heademail
        },
    }
    return skillaz_record

from typing import Any, Optional, TypedDict

from pydantic import BaseModel, EmailStr, ValidationError

from pkg_types import WithError

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

def validate_vde_org_unit(record: dict[str, Any]) -> WithError[OrgUnitVde]:
    try:
        validated = OrgUnitVde(**record)
        return WithError(None, validated)
    except ValidationError:
        return WithError('record not valid', None)
    except Exception:
        return WithError('unhandled error', None)


def validate_vde_org_unit_db_meta(record: dict[str, Any]) -> WithError[OrgUnitVdeDbMeta]:
    try:
        validated = OrgUnitVdeDbMeta(**record)
        return WithError(None, validated)
    except ValidationError:
        return WithError('record not valid', None)
    except Exception:
        return WithError('unhandled error', None)

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

def transform_org_unit_vde_to_skillaz(record: dict[str, Any]) -> WithError[OrgUnitSkillaz]:
    err, vde_record = validate_vde_org_unit_db_meta(record)
    if err or vde_record is None:
        err = err if err else 'error empty record'
        return WithError(err, None)
    skillaz_record: OrgUnitSkillaz = {
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
    return WithError(None, skillaz_record)

def transform_ort_unit_insert(record: dict[str, Any]) -> WithError[OrgUnitVdeInsertReady]:
    err, validated = validate_vde_org_unit(record)    
    if err or validated is None:
        err = err if err else 'error empty record'
        return WithError(err, None)
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
    return WithError(None, insert_record)
    

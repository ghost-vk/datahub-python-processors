from datetime import datetime
from typing import Optional, TypeAlias, TypedDict, Any
from enum import Enum

from pydantic import BaseModel, EmailStr, ValidationError, field_validator, ConfigDict
import phonenumbers

from exceptions import TransformException
from utils import strip_dict_strings

class EmployeeStateEnum(str, Enum):
    active = 'Действующий'
    sick = 'На больничном'
    fired = 'Уволен'
    maternity = 'Декрет'

class EmployeeStateUUIDEnum(str, Enum):
    active = '0128e7b2-2248-4fed-bee5-2c48d57fa7c4'
    sick = '9c306aec-b4dc-4e26-9724-be024fe4d194'
    fired = '343cb325-7737-4ac4-8e52-fa2313558612'
    maternity = 'ff106fc3-384b-43c6-85da-05956b535ef8'

class EmployeeRolesEnum(str, Enum):
    user = 'user'
    manager = 'manager'
    mentor = 'mentor'
    external_partner = 'external_partner'

class EmployeeRolesUUIDEnum(str, Enum):
    user = 'a1f00ef8-b6a6-4766-91b9-4ec55cb4ab62'
    manager = 'd02a6ee1-b877-452d-8339-af1e9ff92fe9'
    mentor = '54201b65-eb88-48a4-81ff-6d3091c7f7b0'
    external_partner = 'c53ab918-bbb8-4d29-b51e-50d4991f0f8c'

def employee_role_uuid_to_name(uuid: EmployeeRolesUUIDEnum) -> EmployeeRolesEnum:
    return EmployeeRolesEnum[uuid.name]

class EmployeeGenderEnum(str, Enum):
    m = 'Мужской'
    f = 'Женский'

ValidatedPhoneNumber: TypeAlias = str

def validate_phone_number(
    phone: str, country_code: Optional[str] = 'RU'
) -> ValidatedPhoneNumber:
    maybe_phone = phonenumbers.parse(phone, country_code)
    if phonenumbers.is_possible_number(maybe_phone):
        return str(phonenumbers.format_number(
            maybe_phone,
            phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        )
    raise TransformException('Phone Number Invalid.')

class PEmployeeVde(BaseModel):
    """Представление сотрудника в исходных данных"""
    workplaceaddress: Optional[str] = None
    state: Optional[EmployeeStateEnum] = None
    gender: EmployeeGenderEnum
    workemail: EmailStr
    phone: Optional[str] = None
    workphone: Optional[str] = None
    surname: str 
    name: str
    patronymic: Optional[str] = None
    snils: Optional[str] = None
    personnelnumber: str
    jobid: Optional[str] = None
    jobname: Optional[str] = None
    workfunc: Optional[str] = None
    orgunitid: Optional[str] = None
    orgunitname: Optional[str] = None
    datejobassignment: Optional[datetime] = None
    dateorgentry: Optional[datetime] = None
    dateofbirth: Optional[datetime] = None
    flowuuid: Optional[str] = None

    model_config = ConfigDict(
        coerce_numbers_to_str=True
    )

    @field_validator('phone')
    def phone_validation(cls, v):
        if v is None:
            return v
        return validate_phone_number(v)

    @field_validator('workphone')
    def workphone_validation(cls, v):
        if v is None:
            return v
        return validate_phone_number(v)

class PEmployeeVdeMeta(BaseModel):
    """Представление сотрудника с метаданными из БД"""
    # новые поля
    id: str
    functionalmanager: Optional[str]
    functionalmanagereml: Optional[EmailStr]
    # uuid вместо названий
    state: Optional[str] = None
    isarchived: Optional[bool] = False
    roles: Optional[str]

    # дальше поля из PEmployeeVde
    workplaceaddress: Optional[str] = None
    gender: EmployeeGenderEnum
    workemail: EmailStr
    phone: Optional[str] = None
    workphone: Optional[str] = None
    surname: str 
    name: str
    patronymic: Optional[str] = None
    snils: Optional[str] = None
    personnelnumber: str
    jobid: Optional[str] = None
    jobname: Optional[str] = None
    workfunc: Optional[str] = None
    orgunitid: Optional[str] = None
    orgunitname: Optional[str] = None
    datejobassignment: Optional[datetime] = None
    dateorgentry: Optional[datetime] = None
    dateofbirth: Optional[datetime] = None
    flowuuid: Optional[str] = None

    model_config = ConfigDict(
        coerce_numbers_to_str=True
    )

    @field_validator('phone')
    def phone_validation(cls, v):
        if v is None:
            return v
        return validate_phone_number(v)

    @field_validator('workphone')
    def workphone_validation(cls, v):
        if v is None:
            return v
        return validate_phone_number(v)
    
class EmployeeVdeInsert(TypedDict):
    workplaceaddress: Optional[str]
    state: Optional[str]
    gender: str
    workemail: str
    phone: Optional[ValidatedPhoneNumber] 
    workphone: Optional[ValidatedPhoneNumber] 
    surname: str 
    name: str 
    patronymic: Optional[str] 
    snils: Optional[str] 
    personnelnumber: str
    jobid: Optional[str] 
    jobname: Optional[str] 
    workfunc: Optional[str] 
    orgunitid: Optional[str] 
    orgunitname: Optional[str] 
    datejobassignment: Optional[float] 
    dateorgentry: Optional[float] 
    dateofbirth: Optional[float] 
    flowuuid: Optional[str] 
    record_name: str

def _timestamp_or_none(t: datetime | None = None) -> float | None:
    return t.timestamp() if t else None

def transform_employee_vde_insert(record: dict[str, Any]) -> EmployeeVdeInsert:
    try: 
        strip_record = strip_dict_strings(record)
        employee = PEmployeeVde(**strip_record)
        insert_record: EmployeeVdeInsert = {
            'workplaceaddress': employee.workplaceaddress,
            'state': EmployeeStateUUIDEnum[employee.state.name].value 
                if employee.state else None,
            'gender': employee.gender.value,
            'workemail': employee.workemail,
            'phone':  employee.phone,
            'workphone':  employee.workphone,
            'surname': employee.surname,
            'name': employee.name,
            'patronymic':  employee.patronymic,
            'snils':  employee.snils,
            'personnelnumber':  employee.personnelnumber,
            'jobid':  employee.jobid,
            'jobname':  employee.jobname,
            'workfunc':  employee.workfunc,
            'orgunitid':  employee.orgunitid,
            'orgunitname':  employee.orgunitname,
            'datejobassignment':  _timestamp_or_none(employee.datejobassignment),
            'dateorgentry':  _timestamp_or_none(employee.dateorgentry),
            'dateofbirth':  _timestamp_or_none(employee.dateofbirth),
            'flowuuid':  employee.flowuuid,
            'record_name': employee.workemail,
        }
        return insert_record
    except ValidationError:
        raise TransformException

class EmployeeSkillazInternationalPhoneNumber(TypedDict):
    PhoneNumber: ValidatedPhoneNumber
    AreaCode: str
    CountryCode: str

EmployeeSkillazData = TypedDict('EmployeeSkillazData', {
    # 'м' | 'ж' | 'f' | 'm'
    'ExtraData.gender': str,
    'ExtraData.WorkPhoneNumber': Optional[ValidatedPhoneNumber],
    'ExtraData.SNILS': Optional[str],
    'ExtraData.PositionId': Optional[str],
    'ExtraData.FunctionalManager': Optional[str],
    'ExtraData.city': Optional[str], 
    'ExtraData.WorkFunction': Optional[str],
    'ExtraData.State': Optional[str],
    'ExtraData.department_external_ids': Optional[list[str]],
    # datetime in iso8601 format
    'ExtraData.date_of_hire_job_position': Optional[str],
    'ExtraData.date_of_hire': Optional[str],
    'ExtraData.date_of_birth': Optional[str],
})

class EmployeeSkillaz(TypedDict):
    UserName: str
    Email: str 
    LastName: str
    FirstName: str
    MiddleName: Optional[str]
    RoleIds: Optional[list[str]]
    InternationalPhoneNumber: Optional[EmployeeSkillazInternationalPhoneNumber]
    Position: Optional[str]
    EmployeeId: str
    IsArchived: Optional[bool]
    Data: EmployeeSkillazData

def _split_role_uuids(input: str) -> list[EmployeeRolesEnum]:
    try:
        if input == '' or input is None:
            return []
        return list(map(
            lambda uuid: EmployeeRolesEnum[EmployeeRolesUUIDEnum(uuid).name],
            input.split(',')))
    except ValueError:
        raise TransformException('bad role')

def _map_role_values(roles: list[EmployeeRolesEnum]) -> list[str]:
    if len(roles) == 0:
        return []
    return list(map(lambda r: r.value, roles))

def _transform_role_uuids_to_names(input: str | None) -> list[str] | None:
    if input is None:
        return None
    roles = _split_role_uuids(input)
    return _map_role_values(roles)

def _split_state_uuids(input: str) -> list[EmployeeStateEnum]:
    try:
        if input == '':
            return []
        return list(map(
            lambda uuid: EmployeeStateEnum[EmployeeStateUUIDEnum(uuid).name],
            input.split(',')))
    except ValueError:
        raise TransformException('bad state')

def _map_state_values(states: list[EmployeeStateEnum]) -> list[str]:
    if len(states) == 0:
        return []
    return list(map(lambda s: s.value, states))

def _transform_state_uuids_to_names(input: str | None) -> str | None:
    if input is None:
        return None
    states = _split_state_uuids(input)
    return _map_state_values(states)[0]

def _datetime_to_iso_or_none(_datetime: datetime | None=None) -> str | None:
    return _datetime.isoformat() if _datetime else None

def _format_phone_ru_international(phone: ValidatedPhoneNumber | None) -> EmployeeSkillazInternationalPhoneNumber | None:
        if phone is None:
            return None
        return {
            'PhoneNumber': phone,
            'AreaCode': '+7',
            'CountryCode': 'RU',
        }
        
def _extract_gender_first_char(gender: EmployeeGenderEnum) -> str:
    return gender.value[0].lower()

def transform_employee_skillaz(record: dict[str, Any]) -> EmployeeSkillaz:
    try:
        record = strip_dict_strings(record)
        validated = PEmployeeVdeMeta(**record)
        employee_skillaz: EmployeeSkillaz = {
            'UserName': validated.workemail, 
            'Email': validated.workemail, 
            'LastName': validated.surname,
            'FirstName': validated.name,
            'MiddleName': validated.patronymic,
            'RoleIds': _transform_role_uuids_to_names(validated.roles),
            'InternationalPhoneNumber': _format_phone_ru_international(
                validated.phone),
            'IsArchived': validated.isarchived,
            'Position': validated.jobname,
            'EmployeeId': validated.personnelnumber,
            'Data': {
                'ExtraData.gender': _extract_gender_first_char(validated.gender),
                'ExtraData.WorkPhoneNumber': validated.workphone,
                'ExtraData.SNILS': validated.snils,
                'ExtraData.PositionId': validated.jobid,
                'ExtraData.FunctionalManager': validated.functionalmanagereml,
                'ExtraData.city': validated.workplaceaddress, 
                'ExtraData.WorkFunction': validated.workfunc,
                'ExtraData.State': _transform_state_uuids_to_names(validated.state),
                'ExtraData.department_external_ids': [validated.orgunitid] 
                    if validated.orgunitid else None,
                'ExtraData.date_of_hire_job_position':
                    _datetime_to_iso_or_none(validated.datejobassignment),
                'ExtraData.date_of_hire': _datetime_to_iso_or_none(validated.dateorgentry),
                'ExtraData.date_of_birth': _datetime_to_iso_or_none(validated.dateofbirth),
            }
        }
        return employee_skillaz
    except ValidationError as verr:
        print(verr)
        raise TransformException
    

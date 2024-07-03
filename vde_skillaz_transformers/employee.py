from datetime import datetime
from typing import List, Optional, TypeAlias, TypedDict, Any
from enum import Enum

from pydantic import BaseModel, EmailStr, ValidationError, field_validator, ConfigDict
import phonenumbers

from exceptions import TransformException
from pkg_types import WithError
from utils import strip_dict

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
    workplaceaddress: Optional[str] = None
    state: Optional[EmployeeStateEnum] = None
    gender: Optional[EmployeeGenderEnum] = None
    workemail: EmailStr
    phone: Optional[str] = None
    workphone: Optional[str] = None
    surname: str 
    name: str
    patronymic: Optional[str] = None
    snils: Optional[str] = None
    personnelnumber: Optional[str] = None
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
    state: Optional[EmployeeStateUUIDEnum]
    gender: Optional[EmployeeGenderEnum]
    workemail: str
    phone: Optional[ValidatedPhoneNumber] 
    workphone: Optional[ValidatedPhoneNumber] 
    surname: str 
    name: str 
    patronymic: Optional[str] 
    snils: Optional[str] 
    personnelnumber: Optional[str] 
    jobid: Optional[str] 
    jobname: Optional[str] 
    workfunc: Optional[str] 
    orgunitid: Optional[str] 
    orgunitname: Optional[str] 
    datejobassignment: Optional[datetime] 
    dateorgentry: Optional[datetime] 
    dateofbirth: Optional[datetime] 
    flowuuid: Optional[str] 
    record_name: str

def transform_employee_vde_insert(record: dict[str, Any]) -> EmployeeVdeInsert:
    try: 
        strip_record = strip_dict(record)
        employee = PEmployeeVde(**strip_record)
        insert_record: EmployeeVdeInsert = {
            'workplaceaddress': employee.workplaceaddress,
            'state': EmployeeStateUUIDEnum[employee.state.name] if employee.state else None,
            'gender': employee.gender,
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
            'datejobassignment':  employee.datejobassignment,
            'dateorgentry':  employee.dateorgentry,
            'dateofbirth':  employee.dateofbirth,
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

class EmployeeSkillaz(TypedDict):
    UserName: str
    Email: str 
    LastName: str
    FirstName: str
    MiddleName: Optional[str]
    RoleIds: Optional[List[EmployeeRolesEnum]]
    InternationalPhoneNumber: Optional[EmployeeSkillazInternationalPhoneNumber]

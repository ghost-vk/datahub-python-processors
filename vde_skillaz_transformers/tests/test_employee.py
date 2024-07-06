import datetime 
import pprint

import pytest

import employee as e
from exceptions import TransformException

def test_transform_employee_vde_insert_valid_case():
    record = {
        'workplaceaddress': ' Москва  ',
        'state': '  На больничном',
        'gender': '  Мужской  ',
        'workemail': 'p.ivanov@digital.gov.ru',
        'phone':  '  79887776655  ',
        'workphone': '  79887776633  ',
        'surname': 'Иванов',
        'name': 'Петр',
        'patronymic': None,
        'snils': 1231231234,
        'personnelnumber': '123-123-123',
        'jobid': ' 070f2899-5933-4d56-bb22-02644cf47320 ',
        'jobname': ' Технический специалист 1С ',
        'workfunc': ' Администрирование \n1C системы ',
        'orgunitid': ' ff7cbb2b-3951-4329-a736-c4800ae62ceb ',
        'orgunitname': 'Управление 1С системами ',
        'datejobassignment': 1404299569,
        'dateorgentry': None,
        'dateofbirth': None,
        'flowuuid': '34f5aced-d03d-4fa3-8105-ec8fcb3ff8c1',
    }
    rec = e.transform_employee_vde_insert(record)
    assert rec == {
        'workplaceaddress': 'Москва',
        'state': '9c306aec-b4dc-4e26-9724-be024fe4d194',
        'gender': 'Мужской',
        'workemail': 'p.ivanov@digital.gov.ru',
        'phone': '+7 988 777-66-55',
        'workphone': '+7 988 777-66-33',
        'surname': 'Иванов',
        'name': 'Петр',
        'patronymic': None,
        'snils': '1231231234',
        'personnelnumber': '123-123-123',
        'jobid': '070f2899-5933-4d56-bb22-02644cf47320',
        'jobname': 'Технический специалист 1С',
        'workfunc': 'Администрирование \n1C системы',
        'orgunitid': 'ff7cbb2b-3951-4329-a736-c4800ae62ceb',
        'orgunitname': 'Управление 1С системами',
        'datejobassignment': datetime.datetime.fromtimestamp(1404299569, datetime.timezone.utc),
        'dateorgentry': None,
        'dateofbirth': None,
        'flowuuid': '34f5aced-d03d-4fa3-8105-ec8fcb3ff8c1',
        'record_name': 'p.ivanov@digital.gov.ru',
    }

def test_transform_employee_skillaz_valid_case():
    record = {
        'id': '8af42d5b-2a06-4fbd-8804-788c73e6790a',
        'functionalmanager': '52f03312-8676-4a5d-901a-3c6e06c192c3',
        'functionalmanagereml': 'f.manager@digital.gov.ru',
        'workplaceaddress': ' Москва  ',
        'roles': ' a1f00ef8-b6a6-4766-91b9-4ec55cb4ab62',
        'state': ' 9c306aec-b4dc-4e26-9724-be024fe4d194',
        'gender': '  Мужской  ',
        'workemail': 'p.ivanov@digital.gov.ru',
        'phone':  '  79887776655  ',
        'workphone': '  79887776633  ',
        'surname': 'Иванов',
        'name': 'Петр',
        'patronymic': None,
        'snils': 1231231234,
        'personnelnumber': '123-123-123',
        'jobid': ' 070f2899-5933-4d56-bb22-02644cf47320 ',
        'jobname': ' Технический специалист 1С ',
        'workfunc': ' Администрирование \n1C системы ',
        'orgunitid': ' ff7cbb2b-3951-4329-a736-c4800ae62ceb ',
        'orgunitname': 'Управление 1С системами ',
        'datejobassignment': 1404299569,
        'dateorgentry': None,
        'dateofbirth': None,
        'flowuuid': '34f5aced-d03d-4fa3-8105-ec8fcb3ff8c1',
    }
    rec = e.transform_employee_skillaz(record)
    assert rec == {
        'UserName': 'p.ivanov@digital.gov.ru',
        'Email': 'p.ivanov@digital.gov.ru',
        'LastName': 'Иванов',
        'FirstName': 'Петр',
        'MiddleName': None,
        'RoleIds': [e.EmployeeRolesEnum.user],
        'InternationalPhoneNumber': {
            'PhoneNumber': '+7 988 777-66-55',
            'AreaCode': '+7',
            'CountryCode': 'RU',
        },
        'IsArchived': False,
        'Position': 'Технический специалист 1С',
        'EmployeeId': '123-123-123',
        'Data': {
            'ExtraData.gender': 'м',
            'ExtraData.WorkPhoneNumber': '+7 988 777-66-33',
            'ExtraData.SNILS': '1231231234',
            'ExtraData.PositionId': '070f2899-5933-4d56-bb22-02644cf47320',
            'ExtraData.FunctionalManager': 'f.manager@digital.gov.ru',
            'ExtraData.city': 'Москва',
            'ExtraData.WorkFunction': 'Администрирование \n1C системы',
            'ExtraData.State': e.EmployeeStateEnum.sick.value,
            'ExtraData.department_external_ids': ['ff7cbb2b-3951-4329-a736-c4800ae62ceb'],
            'ExtraData.date_of_hire_job_position': '2014-07-02T11:12:49+00:00',
            'ExtraData.date_of_hire': None,
            'ExtraData.date_of_birth': None},
        }
    # pprint.pp(rec)

def test_transform_employee_skillaz_not_valid_case():
    with pytest.raises(TransformException) as e_info:
        bad_state_record = {
            'id': '8af42d5b-2a06-4fbd-8804-788c73e6790a',
            'functionalmanager': '52f03312-8676-4a5d-901a-3c6e06c192c3',
            'functionalmanagereml': 'f.manager@digital.gov.ru',
            'workplaceaddress': ' Москва  ',
            'roles': ' a1f00ef8-b6a6-4766-91b9-4ec55cb4ab62',
            'state': ' 9c306aec-b4dc-4e26-9724-be024fe4d195',
            'gender': '  Мужской  ',
            'workemail': 'p.ivanov@digital.gov.ru',
            'phone':  '  79887776655  ',
            'workphone': '  79887776633  ',
            'surname': 'Иванов',
            'name': 'Петр',
            'patronymic': None,
            'snils': 1231231234,
            'personnelnumber': '123-123-123',
            'jobid': ' 070f2899-5933-4d56-bb22-02644cf47320 ',
            'jobname': ' Технический специалист 1С ',
            'workfunc': ' Администрирование \n1C системы ',
            'orgunitid': ' ff7cbb2b-3951-4329-a736-c4800ae62ceb ',
            'orgunitname': 'Управление 1С системами ',
            'datejobassignment': 1404299569,
            'dateorgentry': None,
            'dateofbirth': None,
            'flowuuid': '34f5aced-d03d-4fa3-8105-ec8fcb3ff8c1',
        }
        e.transform_employee_skillaz(bad_state_record)
    assert e_info.value.args[0] == 'bad state'

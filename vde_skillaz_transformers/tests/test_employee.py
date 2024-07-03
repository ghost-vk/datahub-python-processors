import datetime 

import employee as e

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
        'personnelnumber': None,
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
        'personnelnumber': None,
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

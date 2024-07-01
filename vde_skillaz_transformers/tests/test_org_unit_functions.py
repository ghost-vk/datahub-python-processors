import org_unit as ou

def test_transform_org_unit_vde_to_skillaz():
    record = {
        'id': 'b8746764-c6e0-4886-9fcd-7093ee3cc56e',
        'record_name': ' Руководство ', 
        'default_order': '1',
        'orgunitid': '70054048-87c5-4c07-94eb-bbff34e8eb5b',
        'name': ' Руководство ',
        'headid': '64a2cfa0-5651-448c-9e05-2af1afee9deb',
        'heademail': '  head@digital.gov.ru  ',
        'address': 'Москва',
        'superiorname': 'Сверхруководство',
        'superiorid': '113587e5-e3ce-4302-948b-309df04951e2',
    }
    _, transformed = ou.transform_org_unit_vde_to_skillaz(record)
    if not transformed:
        raise ValueError('record not defined')
    assert transformed['Id'] == record['orgunitid'].strip()
    assert transformed['ExternalId'] == record['orgunitid'].strip()
    assert transformed['Name'] == record['name'].strip()
    assert transformed['ParentId'] == record['superiorid'].strip()
    assert transformed['Address'] == record['address'].strip()
    assert transformed['IsArchived'] == False
    assert transformed['Data']['ExtraData.Manager'] == record['heademail'].strip()

def test_validate_vde_org_unit():
    record = {
        'orgunitid': '70054048-87c5-4c07-94eb-bbff34e8eb5b',
        'name': ' Руководство ',
        'headid': '64a2cfa0-5651-448c-9e05-2af1afee9deb',
        'heademail': '  head@digital.gov.ru  ',
        'address': 'Москва',
        'superiorname': 'Сверхруководство',
        'superiorid': '113587e5-e3ce-4302-948b-309df04951e2',
    }
    _, transformed = ou.transform_ort_unit_insert(record)
    if not transformed:
        raise ValueError('record not defined')
    assert transformed['record_name'] == record['name'].strip()

def test_validate_vde_org_unit_fail_with_empty_dict():
    record = {}
    err, _ = ou.transform_ort_unit_insert(record)
    assert err == 'record not valid'

def test_validate_vde_org_unit_fail_with_not_valid_record():
    record = {
        'orgunitid': '70054048-87c5-4c07-94eb-bbff34e8eb5b',
        'name': ' Руководство ',
        'headid': '64a2cfa0-5651-448c-9e05-2af1afee9deb',
        'heademail': 'bad email value',
        'address': 'Москва',
        'superiorname': 'Сверхруководство',
        'superiorid': '113587e5-e3ce-4302-948b-309df04951e2',
    }
    err, _ = ou.transform_ort_unit_insert(record)
    assert err == 'record not valid'
    record = {
        'orgunitid': None,
        'name': ' Руководство ',
        'headid': '64a2cfa0-5651-448c-9e05-2af1afee9deb',
        'heademail': '  head@digital.gov.ru  ',
        'address': 'Москва',
        'superiorname': 'Сверхруководство',
        'superiorid': '113587e5-e3ce-4302-948b-309df04951e2',
    }
    err, _ = ou.transform_ort_unit_insert(record)
    assert err == 'record not valid'

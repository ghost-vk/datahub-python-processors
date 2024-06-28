import org_unit as ou

def test_transform_org_unit_vde_to_skillaz():
    record = {
        'orgunitid': '70054048-87c5-4c07-94eb-bbff34e8eb5b',
        'name': ' Руководство ',
        'headid': '64a2cfa0-5651-448c-9e05-2af1afee9deb',
        'heademail': '  head@digital.gov.ru  ',
        'address': 'Москва',
        'superiorname': 'Сверхруководство',
        'superiorid': '113587e5-e3ce-4302-948b-309df04951e2',
    }
    transformed = ou.transform_org_unit_vde_to_skillaz(record)
    assert transformed['Id'] == record['orgunitid'].strip()
    assert transformed['ExternalId'] == record['orgunitid'].strip()
    assert transformed['Name'] == record['name'].strip()
    assert transformed['ParentId'] == record['superiorid'].strip()
    assert transformed['Address'] == record['address'].strip()
    assert transformed['IsArchived'] == False
    assert transformed['Data']['ExtraData.Manager'] == record['heademail'].strip()


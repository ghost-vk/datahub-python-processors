from org_unit.validate_org_unit_record import validate_org_unit_record

def test_first():
  record = {
      "ID организационной единицы": "550e8400-e29b-41d4-a716-446655440000",
      "Название организационной единицы": "Sales",
      "ID Руководителя этой организационной единицы": "550e8400-e29b-41d4-a716-446655440001",
      "Название вышестоящей организационной единицы": "Corporate",
      "ID вышестоящей организационной единицы": "550e8400-e29b-41d4-a716-446655440002"
  }
  is_valid = validate_org_unit_record(record)
  assert is_valid != None
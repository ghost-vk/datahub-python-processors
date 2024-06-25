from typing import Dict, Any, Optional
from pydantic import ValidationError

from org_unit.org_unit_pydantic_model import OrgUnitPydanticModel

def validate_org_unit_record(record: Dict[str, Any]) -> Optional[OrgUnitPydanticModel]:
    try:
        # Create an instance of OrgUnitPydanticModel using the record
        org_unit_record = OrgUnitPydanticModel(**record)
        return org_unit_record
    except ValidationError as e:
        # Handle validation errors (e.g., print the errors)
        print("Validation error occurred:", e)
        return None

# record = {
#     "ID организационной единицы": "550e8400-e29b-41d4-a716-446655440000",
#     "Название организационной единицы": "Sales",
#     "ID Руководителя этой организационной единицы": "550e8400-e29b-41d4-a716-446655440001",
#     "Название вышестоящей организационной единицы": "Corporate",
#     "ID вышестоящей организационной единицы": "550e8400-e29b-41d4-a716-446655440002"
# }

# org_unit_record = validate_org_unit_record(record)
# if org_unit_record:
#     print("Validated record:", org_unit_record)
# else:
#     print("Record is invalid.")
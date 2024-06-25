from typing import Optional
from uuid import UUID

from nifiapi.recordtransform import RecordTransformResult, RecordTransform # type: ignore
from pydantic import ValidationError # type: ignore

from org_unit.org_unit_pydantic_model import OrgUnitPydanticModel

class TransformOrgUnit(RecordTransform):
    class Java:
        implements = ['org.apache.nifi.python.processor.RecordTransform']

    class ProcessorDetails:
        version = '2.0.0-M3'

    def __init__(self, **kwargs):
        super().__init__()

    def transform(self, context, record, schema, attributemap):
        try:
            org_unit_record = OrgUnitPydanticModel(**record)
        except ValidationError:
            return RecordTransformResult(record=record, relationship="failure")

        transformed_record = {
            'Id': str(org_unit_record.id_org_unit),
            'ExternalId': str(org_unit_record.id_org_unit),
            'Name': org_unit_record.name_org_unit,
            'ParentId': str(org_unit_record.parent_org_unit_id) if org_unit_record.parent_org_unit_id else None,
            'Address': None,
            'IsArchived': None,
            'Data': {
                'ExtraData.Manager': str(org_unit_record.manager_id) if org_unit_record.manager_id else None
            }
        }

        return RecordTransformResult(record=transformed_record, relationship="success")

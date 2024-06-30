from nifiapi.recordtransform import RecordTransformResult, RecordTransform

from org_unit import validate_vde_org_unit_db_meta

class OrgUnitSkillazRecordTransform(RecordTransform):
    class Java:
        implements = ['org.apache.nifi.python.processor.RecordTransform']

    class ProcessorDetails:
        version = '2.0.0-M3'
        tags = ['orgunit']

    def __init__(self, **kwargs):
        super().__init__()

    def transform(self, context, record, schema, attributemap):
        err, transformed_record = validate_vde_org_unit_db_meta(record)
        if err:
            return RecordTransformResult(record=record, relationship='failure')
        return RecordTransformResult(record=transformed_record)

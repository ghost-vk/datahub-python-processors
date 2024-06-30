from nifiapi.recordtransform import RecordTransformResult, RecordTransform

from org_unit import validate_vde_org_unit

class OrgUnitInsertValidation(RecordTransform):
    class Java:
        implements = ['org.apache.nifi.python.processor.RecordTransform']

    class ProcessorDetails:
        version = '2.0.0-M3'
        tags = ['orgunit']

    def __init__(self, **kwargs):
        super().__init__()

    def transform(self, context, record, schema, attributemap):
        err, validated = validate_vde_org_unit(record)
        if err:
            return RecordTransformResult(record=record, relationship='failure')
        return RecordTransformResult(record=validated, relationship='success')

from nifiapi.recordtransform import RecordTransformResult, RecordTransform

import test_fn

class OrgUnitSkillazRecordTransform(RecordTransform):
    class Java:
        implements = ['org.apache.nifi.python.processor.RecordTransform']

    class ProcessorDetails:
        version = '2.0.0-M3'
        tags = ['orgunit']

    def __init__(self, **kwargs):
        super().__init__()

    def transform(self, context, record, schema, attributemap):
        transformed_record = test_fn.test_fn()
        return RecordTransformResult(record=transformed_record)

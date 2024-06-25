from nifiapi.recordtransform import RecordTransformResult, RecordTransform

class OrgUnitVdeSkillazTransformer(RecordTransform):
    class Java:
        implements = ['org.apache.nifi.python.processor.RecordFileTransform'] 

    class ProcessorDetails:
        version: '2.0.0-M3'

    def __init__(self, **kwargs):
        super().__init__()

    def transform(self, context, record, schema, attributemap):
        transformed_record = { 'test': 'ok' }
        return RecordTransformResult(record=transformed_record,
                                     relationship="success")

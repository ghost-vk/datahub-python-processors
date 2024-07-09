from nifiapi.recordtransform import RecordTransformResult, RecordTransform

from org_unit import transform_ort_unit_insert
from exceptions import TransformException

class OrgUnitInsertTransform(RecordTransform):
    class Java:
        implements = ['org.apache.nifi.python.processor.RecordTransform']

    class ProcessorDetails:
        version = '2.0.0-M3'
        tags = ['orgunit']

    def __init__(self, **kwargs):
        super().__init__()

    def transform(self, context, record, schema, attributemap):
        try:
            transformed = transform_ort_unit_insert(record)
            return RecordTransformResult(record=transformed)
        except TransformException:
            return RecordTransformResult(record=record, relationship='failure')
        except Exception as e:
            self.logger.warn('Unhandled Error in OrgUnitInsertTransform. ' + repr(e))
            return RecordTransformResult(record=record, relationship='failure')

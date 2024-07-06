from nifiapi.recordtransform import RecordTransformResult, RecordTransform

from exceptions import TransformException
from employee import transform_employee_vde_insert 

class EmployeeInsertTransform(RecordTransform):
    class Java:
        implements = ['org.apache.nifi.python.processor.RecordTransform']

    class ProcessorDetails:
        version = '2.0.0-M3'
        tags = ['orgunit']

    def __init__(self, **kwargs):
        super().__init__()

    def transform(self, context, record, schema, attributemap):
        try:
            transformed = transform_employee_vde_insert(record)
            return RecordTransformResult(record=transformed)
        except TransformException:
            return RecordTransformResult(record=record, relationship='failure')
        except Exception as e:
            self.logger.warn('Unhandled Error in EmployeeInsertTransform. ' + repr(e))
            return RecordTransformResult(record=record, relationship='failure')
            

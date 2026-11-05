class ComplianceError(Exception):

    pass
class InvalidTransactionError(ComplianceError):
    pass
class DuplicateTransactionError(ComplianceError):
    pass
class DataFormatError(ComplianceError):
    pass
class EmptyQueueError(ComplianceError):
    pass
class EmptyStackError(ComplianceError):
    pass
class InvalidRuleConfigError(ComplianceError):
    pass
class InsufficientDataError(ComplianceError):
    pass

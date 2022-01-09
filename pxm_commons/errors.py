class PxmError(Exception):
    pass


class PxmServiceError(PxmError):
    pass


class PxmValueError(PxmServiceError):
    pass

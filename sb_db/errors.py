class Error(Exception):
    pass

class DuplicateKeyError(Error):
    pass

class PoolBusyError(Error):
    pass
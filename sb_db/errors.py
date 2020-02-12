class Error(Exception):
    pass

class UniqueViolation(Error):
    pass

class DatabaseError(Error):
    pass
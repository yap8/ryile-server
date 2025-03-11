class BaseDomainException(Exception):
    pass


class ValidationError(BaseDomainException):
    pass


class AuthenticationError(BaseDomainException):
    pass

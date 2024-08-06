from fastapi import HTTPException, status


class DefaultException(HTTPException):
    status_code = 500
    detail = ''

    def __init__(self):
        super().__init__(
            status_code=self.status_code,
            detail=self.detail
        )


class UserAlreadyExistsException(DefaultException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'User already exists'


class InvalidLoginDataException(DefaultException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Invalid email or password'


class AbsentTokenException(DefaultException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'No token'


class InvalidTokenFormatException(DefaultException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Invalid token format'


class ExpiredToeknException(DefaultException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Token expired'


class UserIsNotPresentException(DefaultException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Unable to find user'

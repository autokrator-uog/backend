from services.exceptions import ServiceException


class UserServiceException(ServiceException):
    pass


class UserNotFoundException(UserServiceException):
    pass

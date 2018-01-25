from services.exceptions import ServiceException


class AccountsServiceException(ServiceException):
    pass


class AccountNotFoundException(AccountsServiceException):
    pass

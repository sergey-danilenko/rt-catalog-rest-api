from .base import AppException


class GatewayError(AppException):
    notify = "Base gateway error"


class OrganizationAlreadyExists(GatewayError):
    notify = "Organization already exists"

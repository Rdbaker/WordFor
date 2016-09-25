# -*- coding: utf-8 -*-
"""API Errors."""


class APIError(Exception):
    message = "400: Bad Request"
    status_code = 400
    description = "The request to this resource is not acceptable."

    def __init__(self, message=None, description=None):
        Exception.__init__(self, message)
        if message is not None:
            self.message = message
        if description is not None:
            self.description = description

    @property
    def status(self):
        """The string version of the status_code integer.

        >>> from wordfor.api.errors import APIError
        >>> exc = APIError()
        >>> exc.status_code
        400
        >>> exc.status
        '400'
        >>> exc.status_code = 403
        >>> exc.status
        '403'

        """
        return str(self.status_code)


class UnauthorizedError(APIError):
    message = "401: Unauthorized"
    status_code = 401
    description = "You are not authenticated and therefore do not have " + \
        "access to this resource."


class ForbiddenError(APIError):
    message = "403: Forbidden"
    status_code = 403
    description = "You are not authroized to have access to this resource."


class NotFoundError(APIError):
    message = "404: Not Found"
    status_code = 404
    description = "The requested resource could not be found."


class UnprocessableEntityError(APIError):
    message = "422: Unprocessable Entity"
    status_code = 422
    description = "The request was well formed, but could not be" + \
        "interpreted as requested"

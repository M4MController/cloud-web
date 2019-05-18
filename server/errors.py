class BaseApiError(Exception):
    STATUS = 500
    TITLE = 'Unknown error'
    DETAIL = 'Unknown error'

    def __init__(self, source=None, **kwargs):
        self.source = source
        self.kwargs = kwargs

    def to_dict(self):
        return {
            'title': self.TITLE,
            'detail': self.DETAIL.format(**self.kwargs),
        }

    def __str__(self):
        return '{}: {}'.format(self.TITLE, self.DETAIL)


class BadRequestError(BaseApiError):
    STATUS = 400
    TITLE = 'Bad Request'


class ValidationFailedError(BadRequestError):
    DETAIL = 'Validation failed'

    def __init__(self, errors):
        super().__init__()
        self.source = errors


class UnsupportedMediaTypeError(BadRequestError):
    TITLE = 'Unsupported media type'
    DETAIL = 'Supported: {supported}'


class NotFoundError(BaseApiError):
    STATUS = 404
    TITLE = 'Not found'


class MethodNotAllowedError(BaseApiError):
    STATUS = 405
    TITLE = 'Method Not Allowed'


class ObjectNotFoundError(NotFoundError):
    DETAIL = '{object} not found'


class ConflictError(BaseApiError):
    STATUS = 409
    TITLE = 'Conflict'


class InternalServerError(BaseApiError):
    STATUS = 500
    TITLE = 'Internal server error'

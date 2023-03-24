from http import HTTPStatus


class AppError(Exception):
    def __init__(self, reason: str, status: int) -> None:
        super().__init__(f'[{status}] {reason}')
        self.reason = reason
        self.status = status


class ConflictError(AppError):
    def __init__(self, entity: str, method: str) -> None:
        super().__init__(f'Can not {method} {entity}', HTTPStatus.CONFLICT)


class NotfoundError(AppError):
    def __init__(self, entity: str, method: str) -> None:
        super().__init__(f' can not found {entity} in {method}', HTTPStatus.NOT_FOUND)

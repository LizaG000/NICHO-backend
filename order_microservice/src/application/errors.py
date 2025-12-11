from starlette import status
from src.infra.postgres.tables import BaseDBModel

from typing import Type, TypeVar

T = TypeVar('T', bound=BaseDBModel)

class BaseError(Exception):
    def __init__(
            self,
            message='Произошла неизвестная ошибка.',
            status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    ) -> None:
        self.status_code = status_code
        self.message = message
    
    def __str__(self) -> str:
        return self.message

class InvalidCredentialsError(BaseError):
    def __init__(self,
                 message: str='Неверный логин или пароль.',
                 status_code = status.HTTP_401_UNAUTHORIZED):
        super().__init__(message, status_code)

class UserAlreadyExistsError(BaseError):
    def __init__(
        self,
        message: str = "Пользователь с таким email или телефоном уже существует.",
        status_code: int = status.HTTP_409_CONFLICT,
    ):
        super().__init__(message, status_code)

class DatabaseCreateError(BaseError):
    def __init__(
        self,
        table: BaseDBModel,
        status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY,
    ):
        super().__init__(f"Ошибка при создании записи в модель: {table.__tablename__}", status_code)

class DatabaseUpdateError(BaseError):
    def __init__(
        self,
        table: Type[T],
        status_code: int = status.HTTP_409_CONFLICT,
    ):
        super().__init__(f"Ошибка при обновлении записи в моделе: {table.__tablename__}", status_code)

class DatabaseDeleteError(BaseError):
    def __init__(
        self,
        table: BaseDBModel,
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ):
        super().__init__(f"Ошибка при удалении записи в моделе: {table.__tablename__}", status_code)

class NotFoundError(BaseError):
    def __init__(
        self,
        table: str,
        status_code: int = status.HTTP_404_NOT_FOUND,
    ):
        super().__init__(f"В {table} запись не найдена", status_code)


class ForbiddenError(BaseError):
    def __init__(
        self,
        required_roles: list[str],
        user_role: str,
        status_code: int = status.HTTP_403_FORBIDDEN,
    ):
        message = (
            f"Недостаточно прав. Требуемые роли: {', '.join(required_roles)}. "
            f"Ваша роль: {user_role}"
        )
        super().__init__(message, status_code)

class UnauthorizedError(BaseError):
    def __init__(
        self,
        message: str = "Требуется авторизация",
        status_code: int = status.HTTP_401_UNAUTHORIZED,
    ):
        super().__init__(message, status_code)

from dishka import Provider, Scope, provide, FromDishka
from fastapi import HTTPException, Request
from src.application.services.auth.token import TokenProcessor
from src.application.schemas.auth import AuthSchema
from loguru import logger


class AuthProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def provide_token_processor(self) -> TokenProcessor:
        return TokenProcessor()

    @provide(provides=AuthSchema)
    def get_token_data(
            self,
            processor: FromDishka[TokenProcessor],
            request: FromDishka[Request],
    ) -> AuthSchema:
        logger.info("provider")
        auth_header = request.headers.get("Authorization")
        logger.info(auth_header)
        headers = {"Authorization": auth_header} if auth_header else {}

        try:
            return processor.extract_token_from_header(headers)
        except ValueError as e:
            raise HTTPException(status_code=401, detail=str(e))
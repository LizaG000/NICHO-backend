import http
import base64
import json
from typing import Dict, Any
from src.application.schemas.auth import AuthSchema
from loguru import logger


class TokenProcessor:
    @staticmethod
    def extract_token_from_header(headers: dict) -> AuthSchema:
        auth_header = headers.get("Authorization")

        if not auth_header:
            raise ValueError("Authorization header required")

        if not isinstance(auth_header, str):
            raise ValueError("Authorization header must be a string")

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise ValueError("Invalid Authorization format. Use: Bearer <token>")

        token = parts[1].strip()
        if not token:
            raise ValueError("Token cannot be empty")

        try:
            parts = token.split('.')
            if len(parts) != 3:
                raise ValueError("Invalid JWT structure")

            payload_b64 = parts[1]

            # Base64url decode
            padding = 4 - len(payload_b64) % 4
            if padding != 4:
                payload_b64 += '=' * padding

            decoded_bytes = base64.urlsafe_b64decode(payload_b64)
            payload_dict = json.loads(decoded_bytes)
            payload_dict["token"] = token
            logger.info(payload_dict)

            return AuthSchema.model_validate(payload_dict)

        except base64.binascii.Error:
            raise ValueError("Invalid base64 encoding in token")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON in token payload")
        except Exception as e:
            raise ValueError(f"Token decoding error: {str(e)}")

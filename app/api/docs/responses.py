from fastapi import status

UNAUTHORIZED_ERROR = {
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Пользователь не авторизован",
        "content": {
            "application/json": {
                "example": {"detail": "Invalid or missing API Key"}
            },
        },
    },
}

NOT_FOUND_ERROR = {
    status.HTTP_404_NOT_FOUND: {
        "description": "Организация не найдена",
        "content": {
            "application/json": {
                "example": {"detail": "Not found"}
            },
        },
    },
}

VALIDATION_ERROR = {
    status.HTTP_422_UNPROCESSABLE_ENTITY: {
        "description": "Ошибка валидации входных данных",
        "content": {
            "application/json": {
                "example": {
                    "detail": [
                        {
                            "loc": [
                                "string",
                                0
                            ],
                            "msg": "string",
                            "type": "string"
                        }
                    ]
                }
            }
        },
    }
}

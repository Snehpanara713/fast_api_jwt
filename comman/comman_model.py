from pydantic import BaseModel

from typing import Any


class SuccessResponse(BaseModel):
    """Success reponses Model"""

    hasError: bool = False
    result: Any
    statusCode: int = 200
    errorMsg: str = ""

    class Config:
        schema_extra = {
            "example": {
                "hasError": False,
                "statusCode": 200,
                "errorMsg": "",
                "result": "Data",
            }
        }

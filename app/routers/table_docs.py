from fastapi import status
from fastapi.responses import JSONResponse
from app.schemas.table import Table


def create_table_docs(router):
    @router.post(
        path="",
        status_code=status.HTTP_201_CREATED,
        response_model=Table,
        summary="Create a new restaurant table",
        description="Adds a new table to the restaurant's inventory",
        responses={
            status.HTTP_201_CREATED: {
                "description": "Table created successfully",
                "content": {
                    "application/json": {
                        "example": {
                            "id": 1,
                            "name": "Window View #5",
                            "location": "Near the fireplace",
                            "seats": 4,
                            "is_active": True,
                        }
                    }
                },
            },
        },
    )
    def decorator(func):
        func.__doc__ = """
        Create a new restaurant table with the following details:

        - **name**: Unique identifier for the table (2-50 characters)
        - **location**: Description of where the table is in the restaurant
        - **seats**: Number of seats (1-20)

        Returns the created table with system-generated ID and active status.
        """
        return func

    return decorator

"""Schemas."""
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginationFilterSchema(BaseModel):
    """Pagination filter schema."""

    page: int = Field(title="Page number", default=1)
    page_size: int = Field(title="Page size", default=10)


class OrderingFilterSchema(BaseModel):
    """Ordering filter schema."""

    ordering: str | None = Field(title="Ordering")


class PaginatedResponseSchema(BaseModel, Generic[T]):
    """Paginated response schema."""

    page: int = Field(title="Page number")
    page_size: int = Field(title="Page size")
    count: int = Field(title="Count")
    results: list[T] = Field(title="Results")


class SuccessResponseSchema(BaseModel):
    """Success response schema."""

    message: str = Field(title="Message")


class ErrorSchema(BaseModel):
    """Error schema."""

    reason: str = Field(title="Reason")


class ErrorResponseSchema(BaseModel):
    """Error response schema."""

    error: ErrorSchema = Field(title="Error")

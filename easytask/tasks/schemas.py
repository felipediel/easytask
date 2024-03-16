"""Schemas."""
from pydantic import BaseModel, ConfigDict, Field, RootModel


class TaskSchema(BaseModel):
    """Task schema."""

    id: int = Field(title="Id")
    userId: int = Field(title="User id")
    title: str = Field(title="Title")
    completed: bool = Field(title="Completed")
    model_config = ConfigDict(extra='ignore')


class TaskListSchema(RootModel):
    """Task list schema."""

    root: list[TaskSchema]


class TaskQueryParamSchema(BaseModel):
    """Task query param schema."""

    start: int = Field(
        title="Start",
        description="First index",
        default=0,
    )
    end: int | None = Field(
        title="End",
        description="Last index",
        default=None,
    )
    limit: int = Field(
        title="Limit",
        description="Maximum results",
        default=5,
    )

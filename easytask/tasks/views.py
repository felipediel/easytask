"""Views."""
from http import HTTPStatus

from flask_jwt_extended import jwt_required
from flask_pydantic import validate
from requests.exceptions import RequestException, Timeout

from flask import Blueprint, current_app

from easytask.core.response import error_response, success_response
from easytask.core.utils import map_gateway_http_status

from .client import TaskAPIClient
from .schemas import TaskListSchema, TaskQueryParamSchema

task_blueprint = Blueprint("tasks", __name__)


@task_blueprint.route("/", methods=["GET"])
@jwt_required()
@validate()
def get_task_list(query: TaskQueryParamSchema) -> tuple[list[dict], int]:
    """Get list of tasks."""
    api_url = current_app.config["TASK_SERVICE_URL"]
    api_client = TaskAPIClient(api_url)

    try:
        api_resp = api_client.get_task_list(
            params={
                "_start": query.start,
                "_end": query.end,
                "_limit": query.limit,
            }
        )
    except Timeout:
        return error_response(status=HTTPStatus.GATEWAY_TIMEOUT)
    except RequestException:
        return error_response(status=HTTPStatus.BAD_GATEWAY)

    if not api_resp.ok:
        status = map_gateway_http_status(api_resp.status_code)
        return error_response(status=status)

    try:
        task_list = TaskListSchema.model_validate_json(
            api_resp.content
        )
    except ValueError as err:
        current_app.logger.error(
            "Failed to deserialize service response: %s", err
        )
        return error_response(status=HTTPStatus.BAD_GATEWAY)

    limit = (
        query.limit
        if query.end is None
        else min(query.end - query.start, query.limit)
    )

    resp_data = [
        task.model_dump(include={"id", "title"})
        for task in task_list.root
    ][:limit]

    return success_response(resp_data)

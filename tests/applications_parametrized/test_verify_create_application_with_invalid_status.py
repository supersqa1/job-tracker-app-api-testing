import pytest

from clients.api_client import APIClient
from helpers.application_helper import build_create_application_payload
from helpers.application_helper import create_application
from helpers.error_helper import verify_error_respsone


INVALID_STATUS_VALUES = [
    pytest.param("interviewing", id="unsupported_string"),
    pytest.param("", id="empty_string"),
    pytest.param("   ", id="whitespace_string"),
    pytest.param("APPLIED", id="uppercase_status"),
    pytest.param(123, id="numeric_value"),
    pytest.param(True, id="boolean_value"),
    pytest.param(None, id="null_value"),
    pytest.param([], id="array_value"),
    pytest.param({}, id="object_value")
    ]


@pytest.mark.parametrize("invalid_status", INVALID_STATUS_VALUES)
def test_verify_create_application_rejects_invalid_status_parametrize(invalid_status):
    print(f"Running invalid status test for value: {invalid_status!r}")

    # create api client
    api_client = APIClient()

    # build a payload with the invalid status value
    payload = build_create_application_payload(status=invalid_status)

    # make the call expecting a validation error
    response_json = create_application(
        api_client,
        payload=payload,
        expected_status_code=422
        )

    # verify the error response
    verify_error_respsone(
        response_json,
        "VALIDATION_ERROR",
        "Request validation failed"
        )

    # verify the validation error is for the status field
    assert response_json["error"]["details"][0]["loc"][1] == "status"

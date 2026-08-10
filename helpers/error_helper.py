

def verify_error_respsone(response_json, expected_code, expected_message):
    assert response_json["error"], f"Create application expecteing failure response did not have error. Actual: {response_json}"
    assert response_json["error"]["code"] == expected_code
    assert response_json["error"]["message"] == expected_message
    assert isinstance(response_json["error"]["details"], list), f"Error response expected to have a list in 'details' but it did not. Actual: {response_json}"
    
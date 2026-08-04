"""
HTTP client for the Job Tracker API test framework.
"""

import logging

import requests
from configs.settings import BASE_URL, DEFAULT_USER_EMAIL, DEFAULT_USER_PASSWORD

logger = logging.getLogger(__name__)


class APIClient:
    """
    Wraps HTTP calls to the Job Tracker API with optional auth and status checks.
    """

    def __init__(self, authenticated=True, email=DEFAULT_USER_EMAIL, password=DEFAULT_USER_PASSWORD):
        """
        Create a client, logging in when authentication is enabled.

        Args:
            authenticated: When True, obtain a Bearer token at startup.
            email: Credentials used for login.
            password: Credentials used for login.
        """
        self.headers = {}
        self.authenticated = authenticated
        if authenticated:
            logger.info("Initializing authenticated API client for %s", email)
            access_token = self.login(email, password)
            self.headers["Authorization"] = f"Bearer {access_token}"
        else:
            logger.info("Initializing unauthenticated API client")

    def login(self, email, password):
        """
        Authenticate and return an access token.

        Args:
            email: User email.
            password: User password.

        Returns:
            Access token from the login response.
        """
        logger.debug("Attempting login at /api/v1/auth/login as %s", email)
        payload = {
            "email": email,
            "password": password
            }

        response_body = self.post_json("/api/v1/auth/login", data=payload)

        logger.info("Login successful for %s", email)
        return response_body["access_token"]

    def get(self, endpoint, headers=None, expected_status_code=200):
        """
        Send a GET request and assert the response status.

        Args:
            endpoint: API path appended to the base URL.
            headers: Optional headers merged with the client's defaults.
            expected_status_code: Status code the response must match.

        Returns:
            The raw ``requests`` response object.
        """
        headers = self.build_headers(headers)
        url = self.build_url(endpoint)
        logger.debug("GET %s (expecting %s)", url, expected_status_code)
        response = requests.get(url, headers=headers)
        logger.info("GET %s -> %s", url, response.status_code)
        self.verify_status_code(response, expected_status_code, url)
        return response

    def get_json(self, endpoint, headers=None, expected_status_code=200):
        """
        Send a GET request and return the parsed JSON body.

        Args:
            endpoint: API path appended to the base URL.
            headers: Optional headers merged with the client's defaults.
            expected_status_code: Status code the response must match.

        Returns:
            Parsed JSON from the response body.
        """
        headers = self.build_headers(headers)
        response = self.get(endpoint, headers, expected_status_code)
        return response.json()

    def post(self, endpoint, data, headers=None, expected_status_code=200):
        """
        Send a POST request with a JSON body and assert the response status.

        Args:
            endpoint: API path appended to the base URL.
            data: JSON-serializable payload.
            headers: Optional headers merged with the client's defaults.
            expected_status_code: Status code the response must match.

        Returns:
            The raw ``requests`` response object.
        """
        headers = self.build_headers(headers)
        url = self.build_url(endpoint)
        logger.debug("POST %s (expecting %s)", url, expected_status_code)
        response = requests.post(url, json=data, headers=headers)
        logger.info("POST %s -> %s", url, response.status_code)
        self.verify_status_code(response, expected_status_code, url)
        return response

    def post_json(self, endpoint, data, headers=None, expected_status_code=200):
        """
        Send a POST request and return the parsed JSON body.

        Args:
            endpoint: API path appended to the base URL.
            data: JSON-serializable payload.
            headers: Optional headers merged with the client's defaults.
            expected_status_code: Status code the response must match.

        Returns:
            Parsed JSON from the response body.
        """
        headers = self.build_headers(headers)
        response = self.post(endpoint, data, headers, expected_status_code)
        return response.json()

    def build_headers(self, headers=None):
        """
        Merge caller headers with auth headers when the client is authenticated.

        Args:
            headers: Optional headers to add or override.

        Returns:
            Combined headers dict, or ``None`` when unauthenticated and no headers are given.
        """
        if self.authenticated:
            return {**self.headers, **(headers or {})} # combining two dictionaries

        return headers

    def verify_status_code(self, response, expected_status_code, url):
        """
        Assert that the response status matches the expected value.

        Args:
            response: HTTP response to validate.
            expected_status_code: Status code the response must match.
            url: Request URL included in the assertion message on failure.
        """
        if response.status_code != expected_status_code:
            logger.warning(
                "Unexpected status for %s: expected %s, got %s",
                url, expected_status_code, response.status_code,
            )
        else:
            logger.debug("Status verified for %s: %s", url, expected_status_code)
        assert response.status_code == expected_status_code, \
            f"Status code. Expected: {expected_status_code}, \
            Actual: {response.status_code}, URL: {url}"


    def build_url(self, endpoint):
        """
        Combine the configured base URL with an API path.

        Args:
            endpoint: API path to append.

        Returns:
            Full request URL.
        """
        return f"{BASE_URL}{endpoint}"

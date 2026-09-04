# Application Fixture Tests

These tests are grouped in this folder because this section is focused on learning PyTest fixtures.

In a real test framework, many of these tests could also live in the feature-specific folders for the behavior being tested.

For example:

- authentication-related tests could live with other auth or negative tests
- application list tests could live with other application endpoint tests
- application update tests could live with other update workflow tests

We are keeping them here on purpose so it is easy to see the fixture examples together:

- `api_client` fixture
- `unauthenticated_api_client` fixture
- `created_application` fixture with cleanup
- fixtures combined with parametrization

The goal of this folder is teaching fixture usage, not creating the only possible folder structure.

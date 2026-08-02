import os

# BASE_URL -> the url that does not include the endpoint
# which will change per environment
# https://dev.jobtracking.com
# https://staging.jobtracking.com
# http://localhost:3050

BASE_URL = os.getenv("BASE_URL", "http://localhost:3050")
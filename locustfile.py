from locust import HttpUser, task, between, events, tag
import config
import data
import utils
import logging

logger = logging.getLogger(__name__)

class ETADeflectionUser(HttpUser):
    wait_time = between(1, 4) # Realistic think time
    host = config.BASE_URL 

    def on_start(self):
        # Pre-load data once per user instance to ensure readiness
        data.DataLoader.load_data()

    @task(config.WEIGHT_VALID)
    @tag('valid')
    def submit_valid_request(self):
        """
        Scenario 1: Valid Business Request (80%)
        - Picks a valid number from CSV.
        - Validates complex ETA business logic (Time/Tense).
        """
        record = data.DataLoader.get_valid_record()
        phone = record['telephoneNumber']
        scenario = record['scenario']
        
        request_name = f"POST /eta [Valid - {scenario.capitalize()}]"
        
        payload = {"telephoneNumber": phone}
        headers = utils.get_headers()
        
        with self.client.post(
            config.ETA_ENDPOINT,
            json=payload,
            headers=headers,
            timeout=config.REQUEST_TIMEOUT,
            catch_response=True,
            name=request_name
        ) as response:
            if response.status_code != 200 and response.status_code != 201:
                logger.error(f"Request {request_name} Failed: {response.status_code} - {response.text}")
            utils.validate_eta_logic(response, scenario)

    @task(config.WEIGHT_INVALID)
    @tag('invalid')
    def submit_invalid_input(self):
        """
        Scenario 2: Validation Failure (10%)
        - Generates dynamic garbage input (+44, non-numeric).
        - Expects 400 Bad Request / 422 Unprocessable Entity.
        """
        payload, failure_type = data.DataLoader.generate_invalid_payload()
        request_name = f"POST /eta [Invalid - {failure_type}]"
        headers = utils.get_headers()
        
        with self.client.post(
            config.ETA_ENDPOINT,
            json=payload,
            headers=headers,
            timeout=config.REQUEST_TIMEOUT,
            catch_response=True,
            name=request_name
        ) as response:
            # We expect a 4xx error here. If we get 4xx, it's a "Success" for the test logic.
            if response.status_code >= 400 and response.status_code < 500:
                response.success()
            else:
                 failure_msg = f"Expected 4xx for invalid input, got {response.status_code} - {response.text}"
                 logger.error(failure_msg)
                 response.failure(failure_msg)

    @task(config.WEIGHT_AUTH_FAIL)
    @tag('auth_fail')
    def submit_auth_failure(self):
        """
        Scenario 3: Auth Failure (10%)
        - sends invalid token.
        - Expects 401 Unauthorized or 403 Forbidden.
        """
        payload = data.DataLoader.get_valid_record() # Payload doesn't matter much
        request_name = "POST /eta [Auth Failure]"
        headers = utils.get_headers(invalid_auth=True)
        
        with self.client.post(
            config.ETA_ENDPOINT,
            json={"telephoneNumber": payload['telephoneNumber']},
            headers=headers,
            timeout=config.REQUEST_TIMEOUT,
            catch_response=True,
            name=request_name
        ) as response:
            if response.status_code in [401, 403]:
                response.success()
            else:
                response.failure(f"Expected 401/403, got {response.status_code}")

# --- REPORTING ---

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    logging.info("Test finished. Check artifacts for detailed CSV/HTML reports.")

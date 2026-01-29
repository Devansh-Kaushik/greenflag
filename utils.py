import uuid
import logging
import datetime
import config
from auth import TokenManager

logger = logging.getLogger(__name__)

def get_headers(invalid_auth=False):
    """
    Constructs standard headers. 
    If invalid_auth is True, injects a garbage token or removes it.
    """
    if invalid_auth:
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer invalid_token_123",
            "X-Correlation-Id": str(uuid.uuid4())
        }
    else:
        token = TokenManager.get_token()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
            "X-Correlation-Id": str(uuid.uuid4())
        }
    return headers

def parse_eta_time(eta_time_str):
    try:
        now = datetime.datetime.now()
        t = datetime.datetime.strptime(eta_time_str, "%H:%M").time()
        eta_dt = datetime.datetime.combine(now.date(), t)
        return eta_dt
    except ValueError:
        return None

def validate_eta_logic(response, scenario):
    """
    Strict validation of ETA business rules.
    """
    try:
        data = response.json()
    except ValueError:
        response.failure("Response was not JSON")
        return

    # Status check
    if response.status_code != 200:
        response.failure(f"Expected 200 OK, got {response.status_code}")
        return

    eta_time_str = data.get("etaTime")
    eta_tense = data.get("etaTense")

    # Rule: If no ETA data -> etaTime="00:00" and etaTense=false (bool)
    # How do we know "no ETA data"? Usually inferred from response or input specific scenario.
    if eta_time_str == "00:00":
        if eta_tense is not False: # Check explicitly for boolean False
             response.failure(f"Logic Fail: etaTime is 00:00 but etaTense is {eta_tense} (expected False)")
        return

    if not eta_time_str or eta_tense is None:
        response.failure("Missing 'etaTime' or 'etaTense' in response")
        return

    # Parse and Calculate
    eta_dt = parse_eta_time(eta_time_str)
    if not eta_dt:
        response.failure(f"Unparseable etaTime: {eta_time_str}")
        return

    now = datetime.datetime.now()
    delta_seconds = (eta_dt - now).total_seconds()
    
    # Validation Logic
    expected_tense = "present"
    if delta_seconds > 300:
        expected_tense = "future"
    elif delta_seconds < -300:
        expected_tense = "past"
        
    # Convert API response to string lower for comparison if it's a string, 
    # but spec says "future | present | past" OR "false". We handled false above.
    
    if str(eta_tense).lower() != expected_tense:
         response.failure(f"Logic Mismatch: Calc={expected_tense} (delta={delta_seconds:.0f}s) vs Resp={eta_tense}")
         return

    response.success()

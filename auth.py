import logging
import threading
import config

logger = logging.getLogger(__name__)

class TokenManager:
    """
    Simple thread-safe provider for the static Bearer token.
    """
    _instance = None
    _lock = threading.Lock()
    
    def __init__(self):
        self.token = config.BEARER_TOKEN

    @classmethod
    def get_token(cls):
        return config.BEARER_TOKEN

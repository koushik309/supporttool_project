import logging
import requests
import urllib3
import attr
from labgrid.proxy import proxymanager
from labgrid.target_factory import target_factory

#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@target_factory.reg_driver
@attr.s(eq=False)
class SupportToolDriver:
    # Required for attr.s to generate __init__ with these parameters
    target = attr.ib()
    name = attr.ib(default=None)

    # Static bindings
    bindings = {"supt": "SupportTool"}

    # Instance vars
    _support_tool_url = attr.ib(default="", init=False)
    logger = attr.ib(factory=lambda: logging.getLogger("SupportToolDriver"), init=False)

    def __attrs_post_init__(self):
        self.logger = logging.getLogger(f"{self.__class__.__name__}")

    def _rest_get(self, url: str, expected_result: bool = True, params: dict = None):
        try:
            if params:
                url += '?' + '&'.join([f"{k}={v}" for k, v in params.items()])
            response = requests.get(url, timeout=5, verify=False)

            if not response.ok and expected_result:
                return False, f"HTTP error {response.status_code}: {response.reason}", None

            content_type = response.headers.get("Content-Type", "").lower()
            if "application/json" in content_type:
                return True, "", response.json()
            else:
                return True, "", response.text
        except Exception as exc:
            return False, str(exc), N
   def check_supporttool_activated(self):
    """
    First ensure the server is running.
    Then check if the SupportTool is activated by:
    1. Trying `/api/status` for a known activation response.
    2. Falling back to `/swagger` and checking content.
    """
    try:
        # Step 1: Check if server is running
        if not self.check_rest_api_running():
            self.logger.error("Cannot check activation: SupportTool API is not running.")
            return False

        # Step 2: Try /api/status for known activation response
        status_url = f"{self._support_tool_url}/api/status"
        okay, error_msg, content = self._rest_get(status_url, expected_result=False)
        if okay and content and isinstance(content, dict) and content.get("status") == "active":
            self.logger.info("SupportTool is activated (via /api/status).")
            return True

        # Step 3: Fallback to /swagger endpoint
        swagger_url = f"{self._support_tool_url}/swagger"
        okay, error_msg, content = self._rest_get(swagger_url, expected_result=False)
        if okay and isinstance(content, str):
            if "Swagger UI" in content or "<title>Swagger UI" in content:
                self.logger.info("SupportTool is activated (via Swagger UI detection).")
                return True
            else:
                self.logger.warning("Swagger responded, but activation markers not found.")
        elif not okay:
            self.logger.warning(f"Swagger endpoint error: {error_msg}")

        return False

    except Exception as exc:
        self.logger.error(f"Activation check failed: {exc}")
        return False
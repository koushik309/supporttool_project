import logging
import requests
import urllib3
import attr
from labgrid.proxy import proxymanager
from labgrid.target_factory import target_factory

# Optional: disable warnings for unverified HTTPS requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@target_factory.reg_driver
@attr.s(eq=False)
class SupportToolDriver:
    target = attr.ib()
    name = attr.ib(default=None)

    bindings = {"supt": "SupportTool"}

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
            return False, str(exc), None

    def check_rest_api_running(self):
        """Check if the SupportTool server is reachable over HTTPS."""
        try:
            host, port = proxymanager.get_host_and_port(self.supt, default_port=self.supt.port)
            self._support_tool_url = f"https://{host}:{port}"
            okay, error_msg, content = self._rest_get(self._support_tool_url, expected_result=True)

            if not okay or not content:
                raise Exception(f"SupportToolDriver error: {error_msg}")
            
            self.logger.info(f"Support Tool API is running at {self._support_tool_url}")
            return True

        except requests.RequestException as exc:
            self.logger.error(f"Request error checking SupportTool API: {exc}")
            return False
        except Exception as exc:
            self.logger.error(f"Unexpected error checking API: {exc}")
            return False

    def check_supporttool_activated(self):
        """
        Confirm the SupportTool server is running, then check if it's activated
        via `/api/status` or fallback to detecting Swagger UI.
        """
        try:
            # Step 1: Ensure the server is up
            if not self.check_rest_api_running():
                self.logger.error("Cannot verify activation — server not reachable.")
                return False

            # Step 2: Try /api/status for known activation state
            status_url = f"{self._support_tool_url}/api/status"
            okay, error_msg, content = self._rest_get(status_url, expected_result=False)
            if okay and isinstance(content, dict) and content.get("status") == "active":
                self.logger.info("SupportTool is activated (via /api/status).")
                return True

            # Step 3: Fallback to Swagger UI check
            swagger_url = f"{self._support_tool_url}/swagger"
            okay, error_msg, content = self._rest_get(swagger_url, expected_result=False)
            if okay and isinstance(content, str):
                if "Swagger UI" in content or "<title>Swagger UI" in content:
                    self.logger.info("SupportTool is activated (via Swagger UI detection).")
                    return True
                else:
                    self.logger.warning("Swagger responded but no activation markers found.")
            elif not okay:
                self.logger.warning(f"Swagger endpoint error: {error_msg}")

            return False

        except Exception as exc:
            self.logger.error(f"Activation check failed: {exc}")
            return False
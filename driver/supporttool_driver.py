import logging
import requests
import attr
from labgrid.driver import Driver
from util.proxy import proxymanager
from factory.target_factory import target_factory

@target_factory.reg_driver
@attr.s(eq=False)
class SupportToolDriver(Driver):
    bindings = {"supt": "SupportTool"}
    _support_tool_url = ""

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        self.logger = logging.getLogger(f"{self.__class__.__name__}")

    def check_rest_api_running(self):
        try:
            host, port = proxymanager.get_host_and_port(self.supt, default_port=self.supt.port)
            self._support_tool_url = f"http://{host}:{port}"
            okay, error_msg, content = self._rest_get(self._support_tool_url, expected_result=True)
            if not okay or not content:
                raise Exception(f"SupportToolDriver error: {error_msg}")
            return True
        except requests.RequestException as exc:
            self.logger.error(f"Error checking support tool API: {exc}")
            return False

    def _rest_get(self, url: str, expected_result: bool = True, params: dict = None):
        try:
            if params:
                url += '?' + '&'.join([f"{k}={v}" for k, v in params.items()])
            response = requests.get(url, timeout=5)
            if not response.ok and expected_result:
                return False, f"HTTP error {response.status_code}: {response.reason}", None
            return True, "", response.json()
        except Exception as exc:
            return False, str(exc), None

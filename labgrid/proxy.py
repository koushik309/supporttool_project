def get_host_and_port(resource, default_port=60000):
    # The IP address of the mock-server in the Docker network
    return "192.168.40.3", default_port


proxymanager = type("ProxyManager", (), {"get_host_and_port": staticmethod(get_host_and_port)})

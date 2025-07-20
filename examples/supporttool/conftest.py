def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="local",
        help="Specify test environment: local or remote"
    )

def pytest_configure(config):
    config.env = config.getoption("--env")
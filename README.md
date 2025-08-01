# Support Tool Driver
# 🛠️ Support Tool Driver Test Framework

This repository provides a Labgrid-compatible Python driver (`SupportToolDriver`) to automate interaction with a medical device support tool via REST API. The tool facilitates upgrading and managing devices in a headless fashion, replacing the manual UI interaction.

The setup includes:
- A **mock FastAPI server** to simulate the real Support Tool backend
- A **Labgrid driver** for integration into embedded test workflows
- **Docker Compose** for isolated, reproducible test environments
- **Pytest** for automated test execution

---

## 📁 Project Structure

supporttool_project/
├── driver/
│ └── supporttool_driver.py # Main Labgrid-compatible driver
├── mock_server/
│ └── mock_supporttool.py # FastAPI mock server implementation
├── tests/
│ ├── test_supporttool_driver.py # Pytest tests for the driver
│ ├── docker-compose.yaml # Docker setup for running tests
│ ├── local.yaml # Environment config (local)
│ ├── remote.yml # Optional remote config
│ └── pytest.ini # Pytest configuration
├── Dockerfile # Base Dockerfile for test services
├── requirements.txt # Python dependencies
└── README.md # Project documentation (this file)



---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Git

### Steps

```bash
# Clone the repo
git clone https://github.com/koushik309/supporttool_project.git
cd supporttool_project/tests

# Build and run the services
docker-compose up --build

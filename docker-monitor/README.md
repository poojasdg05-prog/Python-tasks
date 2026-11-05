# Docker Container Monitoring and Management Tool Using Python

## 1. Project Overview

This project is a Python-based Docker Container Monitoring and Management Tool that helps DevOps engineers monitor Docker containers running on a local machine.

The tool connects to the Docker Engine using the Python Docker SDK, collects container details, monitors container status, identifies long-running containers, and generates monitoring reports in CSV format.

It also provides an option to start stopped containers through user confirmation.

**Key objective:** Automate basic Docker container monitoring and management using Python.

## 2. Project Objectives

- Monitor all Docker containers, including running and stopped containers.
- Retrieve container ID, name, image, status, and running duration.
- Identify long-running containers based on a configurable threshold.
- Identify stopped containers.
- Start a stopped container after user confirmation.
- Generate CSV reports for monitoring results.
- Maintain application logs for troubleshooting.
- Handle Docker connection errors and invalid user inputs.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python 3 | Automation scripting |
| Docker | Container platform |
| Docker Desktop / Docker Engine | Runs containers locally |
| Docker SDK for Python | Connects Python with Docker |
| CSV | Stores monitoring reports |
| Logging | Tracks application execution and errors |
| Exception Handling | Handles Docker and runtime errors |

## 4. Project Architecture

```text
docker-container-monitor/
│
├── docker_monitor.py
│
├── reports/
│   └── container_report.csv
│
├── logs/
│   └── docker_monitor.log
│
├── requirements.txt
│
└── README.md
```

**File descriptions:**

- `docker_monitor.py` – Main Python script for monitoring and managing containers.
- `reports/` – Stores generated container monitoring reports.
- `logs/` – Stores application execution logs.
- `requirements.txt` – Contains required Python dependencies.
- `README.md` – Project documentation.

## 5. Prerequisites

Install the following before running the project:

1. Python 3.9 or above.
2. Docker Desktop (Windows) or Docker Engine (Linux).
3. Docker daemon must be running.
4. VS Code or any Python

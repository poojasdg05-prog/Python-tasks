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
4. VS Code or any Python-supported IDE.

Verify installations:

```bash
python --version
docker --version
docker ps -a
```

## 6. Installation and Setup

### Step 1: Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd docker-container-monitor
```

### Step 2: Create a virtual environment

```bash
python -m venv venv
```

### Step 3: Activate the virtual environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\venv\Scripts\Activate.ps1
```

For Linux:

```bash
source venv/bin/activate
```

### Step 4: Install dependencies

```bash
pip install -r requirements.txt
```

The `requirements.txt` file should contain:

```text
docker
```

### Step 5: Run the application

```bash
python docker_monitor.py
```

## 7. Sample Docker Containers for Testing

Create one running container:

```bash
docker run -d --name demo-running alpine:latest sh -c "sleep 3600"
```

Create a container that will be stopped initially but can run when started:

```bash
docker create --name demo-stopped alpine:latest sleep 3600
```

Stop the second container:

```bash
docker start demo-stopped
docker stop demo-stopped
```

Verify both containers:

```bash
docker ps -a
```

Now execute the Python monitoring script.

## 8. Key Features

### Feature 1: Docker Connection

- Uses the Docker SDK to connect to the Docker daemon.
- Checks whether Docker is accessible.
- Handles connection failures using exception handling.

### Feature 2: Container Monitoring

Collects the following details:

- Container ID
- Container name
- Docker image
- Container status
- Container start time
- Running duration

### Feature 3: Long-Running Container Detection

- Calculates how long a container has been running.
- Compares the duration against a configurable threshold.
- Identifies containers that exceed the threshold.
- Helps engineers investigate containers that may require attention.

### Feature 4: Stopped Container Detection

- Identifies containers in the stopped or exited state.
- Displays the container name and status.
- Helps engineers identify unavailable application containers.

### Feature 5: Container Management

- Provides an option to start a stopped container.
- Requests user confirmation before starting it.
- Validates the container status before performing the action.

### Feature 6: Report Generation

Generates a CSV report containing container details and monitoring status.

Example:

| Container Name | Image | Status | Monitoring Result |
|---|---|---|---|
| demo-running | alpine | running | LONG_RUNNING / RUNNING |
| demo-stopped | alpine | exited | STOPPED |

The actual monitoring result depends on the configured threshold and container status.

### Feature 7: Logging and Exception Handling

- Maintains application logs.
- Captures Docker connection errors.
- Handles invalid container selections.
- Records monitoring and management activities.

## 9. Sample Output

```text
========================================
    DOCKER CONTAINER MONITORING TOOL
========================================

Checking Docker connection...

Docker connection successful!

Fetching container details...

Container Name : demo-running
Container ID   : xxxxxxxxxxxx
Image          : alpine:latest
Status         : running
Result         : RUNNING

----------------------------------------

Container Name : demo-stopped
Container ID   : xxxxxxxxxxxx
Image          : alpine:latest
Status         : exited
Result         : STOPPED

----------------------------------------

1. Monitor Containers
2. Start a Stopped Container
3. Exit

Enter your choice:
```

*Output is illustrative; the exact display depends on the implementation and running containers.*

## 10. Important Python Concepts Used

| Python Concept | Where It Is Used |
|---|---|
| Modules | Importing Docker, CSV, logging and system libraries |
| Functions | Separating monitoring and management operations |
| Conditional Statements | Checking container status |
| Loops | Iterating through containers |
| Lists and Dictionaries | Storing container information |
| Exception Handling | Handling Docker errors |
| File Handling | Writing CSV reports and log files |
| DateTime | Calculating container running duration |
| External Libraries | Connecting Python with Docker SDK |

## 11. Real-Time DevOps Use Case

In a real-time DevOps environment, multiple Docker containers may run application services such as:

- Frontend
- Backend
- Database
- Payment service
- API Gateway

A DevOps engineer needs to regularly monitor container health and identify stopped or abnormal containers.

This automation tool helps by collecting container information, identifying stopped and long-running containers, and generating reports.

It can be extended further to send email or Slack alerts and integrate with scheduled monitoring jobs.

**Note:** Running duration alone does not prove that a container is unhealthy. Production monitoring should also include health checks, resource utilization, application logs, and service availability.

## 12. Troubleshooting

| Issue | Possible Solution |
|---|---|
| Docker daemon connection failed | Start Docker Desktop or Docker Engine |
| `ModuleNotFoundError: No module named 'docker'` | Run `pip install docker` |
| Permission denied | Check Docker permissions and user access |
| No containers found | Run `docker ps -a` |
| CSV report not generated | Check report directory permissions |
| Container fails to start | Check container logs using `docker logs <container_name>` |

Useful Docker commands:

```bash
docker ps
docker ps -a
docker inspect <container_name>
docker logs <container_name>
docker stats
docker start <container_name>
docker stop <container_name>
```

## 13. Future Enhancements

- Monitor CPU and memory utilization using Docker stats.
- Add container health-check monitoring.
- Send email and Slack notifications.
- Schedule monitoring using cron or Windows Task Scheduler.
- Integrate with Prometheus and Grafana.
- Add a web dashboard using Flask or FastAPI.
- Integrate container monitoring into Jenkins or GitHub Actions.

## 14. Security Considerations

- Do not expose the Docker daemon over an unsecured network.
- Restrict Docker socket access to authorised users.
- Validate container names and user inputs.
- Avoid automatically restarting or deleting production containers without approval.
- Store credentials securely.

## 15. Conclusion

This project demonstrates how Python can be used to automate Docker container monitoring and basic container management.

It provides practical exposure to Docker SDK integration, Python automation, exception handling, logging, CSV report generation, and container troubleshooting.

The project is designed to run locally using Docker Desktop or Docker Engine and does not require AWS or any cloud infrastructure.

---

**Project Type:** DevOps Automation  
**Language:** Python  
**Platform:** Docker  
**Execution:** Local Machine  
**Author:** Your Name

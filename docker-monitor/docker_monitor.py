
import docker
import csv
import logging
import sys

from pathlib import Path
from datetime import datetime, timezone
from docker.errors import DockerException, APIError, NotFound


# -----------------------------------------
# 1. Configuration
# -----------------------------------------

REPORT_DIR = Path("reports")


# -----------------------------------------
# 2. Logging configuration
# -----------------------------------------

def setup_logging():

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    log_file = REPORT_DIR / f"docker_monitor_{timestamp}.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(sys.stdout)
        ],
        force=True
    )

    return log_file


# -----------------------------------------
# 3. Connect to local Docker Engine
# -----------------------------------------

def connect_docker():

    try:

        client = docker.from_env()

        client.ping()

        logging.info("Connected to local Docker Engine")

        return client

    except DockerException as error:

        raise RuntimeError(
            "Docker Engine is not running. "
            "Start Docker Desktop and try again."
        ) from error


# -----------------------------------------
# 4. Calculate container running duration
# -----------------------------------------

def get_running_duration(container):

    if container.status != "running":
        return None

    try:

        container.reload()

        start_time = container.attrs["State"]["StartedAt"]

        if not start_time or start_time.startswith("0001-"):
            return None

        start_time = datetime.fromisoformat(
            start_time.replace("Z", "+00:00")
        )

        current_time = datetime.now(timezone.utc)

        duration = current_time - start_time

        return max(0, int(duration.total_seconds()))

    except (KeyError, ValueError, TypeError):

        return None


# -----------------------------------------
# 5. Convert seconds into readable format
# -----------------------------------------

def format_duration(seconds):

    if seconds is None:
        return "N/A"

    hours, remainder = divmod(seconds, 3600)

    minutes, secs = divmod(remainder, 60)

    return f"{hours}h {minutes}m {secs}s"


# -----------------------------------------
# 6. Identify stopped and long-running containers
# -----------------------------------------

def monitor_containers(client, threshold_hours):

    all_containers = client.containers.list(all=True)

    stopped_containers = []

    report_data = []

    long_running_count = 0

    for container in all_containers:

        try:

            container.reload()

            status = container.status

            duration_seconds = get_running_duration(container)

            if status == "exited":

                category = "STOPPED"

                stopped_containers.append(container)

            elif status == "running":

                if (
                    duration_seconds is not None
                    and duration_seconds > threshold_hours * 3600
                ):

                    category = "LONG_RUNNING"

                    long_running_count += 1

                else:

                    category = "RUNNING"

            else:

                category = status.upper()

            record = {

                "Name": container.name,

                "Container_ID": container.short_id,

                "Image": container.attrs.get(
                    "Config", {}
                ).get("Image", "Unknown"),

                "Status": status,

                "Running_Duration": format_duration(
                    duration_seconds
                ),

                "Category": category

            }

            report_data.append(record)

            print(
                f"{record['Name']} | "
                f"{record['Container_ID']} | "
                f"{record['Image']} | "
                f"{record['Status']} | "
                f"{record['Running_Duration']} | "
                f"{record['Category']}"
            )

        except (APIError, NotFound) as error:

            logging.warning(
                "Could not inspect container: %s",
                error
            )

    return stopped_containers, report_data, long_running_count


# -----------------------------------------
# 7. Generate CSV report
# -----------------------------------------

def generate_report(report_data):

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    report_file = REPORT_DIR / f"container_report_{timestamp}.csv"

    fields = [
        "Name",
        "Container_ID",
        "Image",
        "Status",
        "Running_Duration",
        "Category"
    ]

    with report_file.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fields
        )

        writer.writeheader()

        writer.writerows(report_data)

    logging.info("CSV report generated: %s", report_file.resolve())

    return report_file


# -----------------------------------------
# 8. Optional restart of stopped container
# -----------------------------------------

def restart_stopped_container(stopped_containers):

    if not stopped_containers:

        print("\nNo stopped containers available.")

        return

    print("\nStopped containers:")

    for index, container in enumerate(stopped_containers, start=1):

        print(f"{index}. {container.name} ({container.short_id})")

    choice = input(
        "\nEnter container number to start, or press Enter to skip: "
    ).strip()

    if not choice:

        print("Skipping restart.")

        return

    if not choice.isdigit():

        print("Invalid selection.")

        return

    index = int(choice)

    if index < 1 or index > len(stopped_containers):

        print("Invalid container number.")

        return

    selected_container = stopped_containers[index - 1]

    confirmation = input(
        f"Type START to start {selected_container.name}: "
    ).strip()

    if confirmation != "START":

        print("Restart cancelled.")

        return

    try:

        selected_container.reload()

        if selected_container.status != "exited":

            print("Container is no longer stopped. Operation cancelled.")

            return

        # Start a stopped container
        selected_container.start()

        selected_container.reload()

        print(
            f"Container {selected_container.name} "
            f"current status: {selected_container.status}"
        )

        logging.info(
            "Started container: %s",
            selected_container.name
        )

    except (DockerException, APIError, NotFound) as error:

        logging.error("Unable to start container: %s", error)

        print("Container start failed:", error)


# -----------------------------------------
# 9. Main function
# -----------------------------------------

def main():

    log_file = setup_logging()

    print("\n===== DOCKER CONTAINER MONITOR =====")

    print("Log file:", log_file)

    try:

        threshold = float(
            input(
                "\nEnter long-running threshold in hours [2]: "
            ).strip() or "2"
        )

        if threshold < 0:

            raise ValueError("Threshold cannot be negative.")

    except ValueError as error:

        print("Invalid threshold:", error)

        return

    client = None

    try:

        client = connect_docker()

        print("\nContainer Name | ID | Image | Status | Duration | Category")

        stopped, report_data, long_running = monitor_containers(
            client,
            threshold
        )

        if not report_data:

            print("No containers found.")

        report_file = generate_report(report_data)

        print("\n========== SUMMARY ==========")

        print("Total containers:", len(report_data))

        print("Stopped containers:", len(stopped))

        print("Long-running containers:", long_running)

        print("Report:", report_file.resolve())

        # Optional recovery
        restart_stopped_container(stopped)

        print("\nMonitoring completed successfully.")

    except (RuntimeError, OSError, DockerException) as error:

        logging.error("%s", error)

        print("\nERROR:", error)

    finally:

        if client is not None:

            client.close()


if __name__ == "__main__":

    main()

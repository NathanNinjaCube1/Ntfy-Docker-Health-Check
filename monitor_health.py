import subprocess
import json
import time

def get_container_health_status(container_name):
    result = subprocess.run(
        ["docker", "inspect", container_name], capture_output=True, text=True
    )
    container_info = json.loads(result.stdout)
    health_status = container_info[0]["State"]["Health"]["Status"]
    return health_status

def send_notification(status, topic):
    message = f"The health status of the container has changed to: {status}"
    curl_command = f"curl -d '{message}' {topic}"
    subprocess.run(curl_command, shell=True)

def monitor_health(container_name, topic):
    previous_status = None
    while True:
        current_status = get_container_health_status(container_name)
       # print(f"Current status: {current_status}")
        if current_status != previous_status:
            send_notification(current_status, topic)
            previous_status = current_status
        time.sleep(10)  # Adjust the interval as needed

if __name__ == "__main__":
    container_name = "DOCKER-CONTAINER-NAME" # Replace with your docker container name
    curl_topic = "NTFY-TOPIC"  # Replace with your ntfy topic
   # print(f"Starting health monitor for container: {container_name}")
    monitor_health(container_name, curl_topic)

#!/bin/bash

# Configuration
SLEEP_INTERVAL=30  # Sleep duration in seconds between containers

# Function to log messages with timestamp
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Function to check if container exists
check_container() {
    local name="$1"
    if ! docker ps -a --format '{{.Names}}' | grep -q "^${name}$"; then
        log_message "Error: Container $name does not exist!"
        return 1
    fi
    return 0
}

# Function to run container with logging
run_container() {
    local name="$1"

    # Check if container exists
    if ! check_container "$name"; then
        exit 1
    fi

    log_message "Starting $name..."
    if ! docker start "$name"; then
        log_message "Error starting $name"
        exit 1
    fi
    log_message "$name started successfully"
}

# First container
run_container "deluge"
log_message "Sleeping for 5 seconds..."
sleep 5

# Second container
run_container "jackett"
log_message "Sleeping for $SLEEP_INTERVAL seconds..."
sleep $SLEEP_INTERVAL

# Third container
run_container "sonarr"
log_message "Sleeping for $SLEEP_INTERVAL seconds..."
sleep $SLEEP_INTERVAL

# Fourth container
run_container "radarr"

log_message "All containers have been started!"

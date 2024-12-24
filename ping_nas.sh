#!/bin/bash

# Configuration
NAS_IP="192.168.31.32"  # Replace with your NAS IP address
MAX_RETRIES=30        # Maximum number of retries
RETRY_INTERVAL=10     # Seconds between retries
SCRIPT_TO_RUN="/home/pi/Applications/pi-scripts/mount_nas.sh"  # Replace with your script path

# Function to check if NAS is available
check_nas() {
    ping -c 1 $NAS_IP >/dev/null 2>&1
    return $?
}

# Wait for NAS to be available
retries=0
echo "Waiting for NAS ($NAS_IP) to be available..."

while ! check_nas; do
    retries=$((retries + 1))
    if [ $retries -ge $MAX_RETRIES ]; then
        echo "Error: NAS not available after $MAX_RETRIES retries. Exiting."
        exit 1
    fi
    echo "NAS not available, retry $retries/$MAX_RETRIES. Waiting $RETRY_INTERVAL seconds..."
    sleep $RETRY_INTERVAL
done

echo "NAS is available! Running script..."
exec "$SCRIPT_TO_RUN"

import logging
import subprocess
from flask import Flask, jsonify

# Create a Flask application
app = Flask(__name__)

# Set up logging. Log to both a file and the console.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),  # Logs to a file named "app.log".
        logging.StreamHandler()         # Outputs logs to console for debugging.
    ]
)

# Define the route `/region` to return region and AZ information.
@app.route('/region', methods=['GET'])
def region_info():
    """
    Fetches the AWS region and availability zone information
    using the EC2 instance metadata service.
    """

    try:
        # Call AWS metadata endpoint to get region and availability zone.
        # Fetch the availability zone first.
        az_command = ['curl', '-s', 'http://169.254.169.254/latest/meta-data/placement/availability-zone']
        az = subprocess.check_output(az_command, text=True).strip()

        # Derive the region by slicing the last character from the AZ.
        region = az[:-1]

        # Log the region/az being returned.
        logging.info(f"Region: {region}, Availability Zone: {az}")

        # Return the values as a JSON response.
        return jsonify({"region": region, "availability_zone": az}), 200

    except subprocess.CalledProcessError as e:
        # If there is an issue with the `curl` command, log it and return an error.
        logging.error("Failed to fetch region/AZ", exc_info=True)
        return jsonify({"error": "Failed to fetch region/AZ"}), 500


if __name__ == "__main__":
    # Run the Flask server on all interfaces (0.0.0.0) and port 8080.
    # This is important because AWS Elastic Load Balancer interacts via public IPs.
    app.run(host="0.0.0.0", port=5000)
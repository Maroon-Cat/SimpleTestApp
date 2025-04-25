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

def fetch_metadata(path):
    try:
        # Get IMDSv2 token first
        token = subprocess.check_output(
            ['curl', '-sX', 'PUT', '-H', 'X-aws-ec2-metadata-token-ttl-seconds: 21600',
             'http://169.254.169.254/latest/api/token'], text=True
        ).strip()

        # Use the token to fetch metadata
        value = subprocess.check_output(
            ['curl', '-sH', f'X-aws-ec2-metadata-token: {token}',
             f'http://169.254.169.254/latest/meta-data/{path}'],
            text=True
        ).strip()

        return value
    except subprocess.CalledProcessError:
        logging.error(f"Failed to fetch metadata for {path}", exc_info=True)
        return ""

# Define the route `/region` to return region and AZ information.
@app.route('/region', methods=['GET'])
def region_info():
    az = fetch_metadata('placement/availability-zone')
    region = az[:-1] if az else ""
    logging.info(f"Region: {region}, Availability Zone: {az}")

    if az:
        return jsonify({"region": region, "availability_zone": az}), 200
    else:
        return jsonify({"error": "Failed to fetch region/AZ"}), 500


if __name__ == "__main__":
    # Run the Flask server on all interfaces (0.0.0.0) and port 8080.
    # This is important because AWS Elastic Load Balancer interacts via public IPs.
    app.run(host="0.0.0.0", port=5000)
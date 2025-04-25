import logging
from flask import Flask
import requests

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Change to logging.INFO for less verbose output
    format="%(asctime)s [%(levelname)s] %(message)s",
)

app = Flask(__name__)

@app.route("/region", methods=["GET"])
def get_region_and_az():
    """
    REST API endpoint to return the AWS region and availability zone (AZ)
    the instance is running in. Supports IMDSv2 (tokens required).
    """
    metadata_url = "http://169.254.169.254/latest/meta-data/"
    try:
        # Log the request for the metadata token (IMDSv2)
        logging.debug("Requesting IMDSv2 token...")
        token_response = requests.put(
            metadata_url + "api/token",
            headers={"X-aws-ec2-metadata-token-ttl-seconds": "360"}
        )

        if token_response.status_code != 200:
            logging.error(f"Token request failed: {token_response.status_code}, {token_response.text}")
            return {"error": "Failed to fetch IMDSv2 token"}, 500

        token = token_response.text
        logging.debug(f"IMDSv2 token: {token}")

        # Log the request for availability zone metadata
        logging.debug("Requesting availability zone from metadata...")
        az_response = requests.get(
            metadata_url + "placement/availability-zone",
            headers={"X-aws-ec2-metadata-token": token}
        )

        if az_response.status_code != 200:
            logging.error(f"AZ request failed: {az_response.status_code}, {az_response.text}")
            return {"error": "Failed to fetch availability zone"}, 500

        az = az_response.text
        logging.debug(f"Availability zone: {az}")

        # Derive AWS region from availability zone
        region = az[:-1]  # Strip off the last character (AZ letter)
        logging.debug(f"Region derived from AZ: {region}")

        # Return final response
        return {"region": region, "az": az}, 200

    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {e}")
        return {"error": str(e)}, 500


if __name__ == "__main__":
    # Configure Flask's built-in server to serve on 0.0.0.0:5000
    logging.info("Starting Flask app...")
    app.run(host="0.0.0.0", port=5000)
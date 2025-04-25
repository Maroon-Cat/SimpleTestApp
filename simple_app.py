import logging
from flask import Flask
import boto3
from botocore.exceptions import NoCredentialsError, EndpointConnectionError

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
    the instance is running in. Uses Boto3 to access EC2 metadata.
    """
    try:
        # Log the initialization of EC2 client
        logging.debug("Initializing EC2 Boto3 client...")

        # Use Boto3 to initialize the EC2 metadata client
        session = boto3.session.Session()
        ec2_metadata = session.client("ec2-metadata")

        # Fetch the availability zone
        logging.debug("Fetching availability zone using Boto3...")
        az = ec2_metadata.placement["availabilityZone"]

        # Derive the region from the availability zone
        region = az[:-1]  # Strip off the last character (AZ letter)
        logging.debug(f"Region derived from AZ: {region}")

        return {"region": region, "az": az}, 200

    except NoCredentialsError as e:
        logging.error("No AWS credentials found. Are you running on an EC2 instance with IAM role access?")
        return {"error": "No AWS credentials found"}, 500

    except EndpointConnectionError as e:
        logging.error("Unable to connect to EC2 metadata service. Is this running on an AWS EC2 instance?")
        return {"error": "Failed to connect to EC2 metadata service"}, 500

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return {"error": str(e)}, 500


if __name__ == "__main__":
    # Configure Flask's built-in server to serve on 0.0.0.0:5000
    logging.info("Starting Flask app...")
    app.run(host="0.0.0.0", port=5000)
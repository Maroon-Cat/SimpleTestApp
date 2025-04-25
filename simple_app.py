from flask import Flask
import requests

app = Flask(__name__)

@app.route("/region", methods=["GET"])
def get_region_and_az():
    """
    REST API endpoint to return the AWS region and availability zone (AZ)
    the instance is running in. Supports IMDSv2 (tokens required).
    """
    metadata_url = "http://169.254.169.254/latest/meta-data/"
    try:
        token = requests.put(
            metadata_url + "api/token",
            headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"}
        ).text
        print(token)
        az = requests.get(
            metadata_url + "placement/availability-zone",
            headers={"X-aws-ec2-metadata-token": token}
        ).text  # e.g., "eu-central-1a"
        print(az)
        region = az[:-1]  # Strip the last character (AZ letter) to get the region

        return {"region": region, "az": az}, 200
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
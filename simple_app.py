from flask import Flask
import requests

app = Flask(__name__)

@app.route("/region", methods=["GET"])
def get_region_and_az():
    """
    REST API endpoint to return the AWS region and availability zone (AZ)
    the instance is running in. Utilizes AWS metadata.
    """
    metadata_url = "http://169.254.169.254/latest/meta-data/"
    try:
        # Fetch the region and availability zone (AZ) from instance metadata
        az = requests.get(metadata_url + "placement/availability-zone").text
        region = az[:-1]  # Region is the AZ without the last character
        return {"region": region, "az": az}, 200
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
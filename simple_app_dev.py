import requests

def test_metadata_directly():
    """
    Manual test function to verify connection to the metadata service.
    """
    metadata_url = "http://169.254.169.254/latest/meta-data/"
    try:
        # Request an IMDSv2 token
        response = requests.put(
            metadata_url + "api/token",
            headers={
                "X-aws-ec2-metadata-token-ttl-seconds": "21600",
                "User-Agent": ""  # Match curl-like behavior
            }
        )
        if response.status_code == 200:
            print(f"IMDSv2 token request succeeded: {response.text}")
        else:
            print(f"IMDSv2 token request failed: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Exception occurred: {e}")

test_metadata_directly()
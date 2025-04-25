import os
import zipfile

def create_artifact():
    """
    Package the application into a deployable ZIP file.
    """
    artifact_name = "../artifacts/web_app.zip"
    with zipfile.ZipFile(artifact_name, "w") as zipf:
        for root, _, files in os.walk("."):
            # Add only .py files to the artifact
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, "."))

    print(f"Artifact '{artifact_name}' created successfully!")

if __name__ == "__main__":
    create_artifact()
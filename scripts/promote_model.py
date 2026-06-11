# promote model

import os
import mlflow
import yaml
from dotenv import load_dotenv
from utils.setup_mlflow import setup_mlflow_tracking
load_dotenv()

def load_params(file_path: str = "params.yaml") -> dict:
    with open(file_path, "r") as file:
        return yaml.safe_load(file)
print('parms.yaml_loaded for registrationmodel')


def promote_model():
    
    setup_mlflow_tracking()

    client = mlflow.MlflowClient()
    
    params = load_params()
    model_name = params["scripts"]["name"]

    
    # Get the latest version in staging
    latest_version_staging = client.get_latest_versions(model_name, stages=["Staging"])[0].version

    # Archive the current production model
    prod_versions = client.get_latest_versions(model_name, stages=["Production"])
    for version in prod_versions:
        client.transition_model_version_stage(
            name=model_name,
            version=version.version,
            stage="Archived"
        )

    # Promote the new model to production
    client.transition_model_version_stage(
        name=model_name,
        version=latest_version_staging,
        stage="Production"
    )
    print(f"Model version {latest_version_staging} promoted to Production")

if __name__ == "__main__":
    promote_model()
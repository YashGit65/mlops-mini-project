import os
import mlflow
from utils.logger import get_logger

logger = get_logger("setup-mlflow-tracking")


def setup_mlflow_tracking() -> None:
    """Set up DagsHub credentials for MLflow tracking."""
    try:
        dagshub_token = os.getenv("DAGSHUB_PAT")

        if not dagshub_token:
            raise EnvironmentError(
                "DAGSHUB_PAT environment variable is not set"
            )

        os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
        os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token

        dagshub_url = "https://dagshub.com"
        repo_owner = "YashGit65"
        repo_name = "mlops-mini-project"

        mlflow.set_tracking_uri(
            f"{dagshub_url}/{repo_owner}/{repo_name}.mlflow"
        )

        logger.info("MLflow tracking configured successfully.")

    except Exception as e:
        logger.error(
            "Failed to initialize DagsHub MLflow tracking: %s",
            e
        )
        raise
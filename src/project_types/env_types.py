import os

from dotenv import load_dotenv
from langchain_core.utils.pydantic import PydanticBaseModel


class EnvSetupException(Exception):
    def __init__(self, errors: list[str]):
        super().__init__("Failed due to lack of envs setup.")
        self.errors = errors

    def __str__(self):
        return f"EnvSetupException: {len(self.errors)} errors - {self.errors}"


class TypedEnvs(PydanticBaseModel):
    db_user: str
    db_passwd: str
    db_name: str
    db_host: str

    @staticmethod
    def load_envs() -> "TypedEnvs":
        """
        The step that processes the sentiment.
        It fetches all messages sent from the user so far and classifies the user as:
        "hot", "warm", or "cold". Al of those in regards to buying intent

        :returns: A new TypedEnvs object.
        :raise EnvSetupException: Some required env is not setup

        """
        load_dotenv()
        # to add a new env to the project you have to:
        # 1. Add the new variable to the class
        # 2. Add a new entry in this list as: (<variable name in the class>, <name of the env>)
        needed_env: list[tuple[str, str]] = [
            ("db_user", "POSTGRES_USER"),
            ("db_passwd", "POSTGRES_PASSWORD"),
            ("db_name", "POSTGRES_DB"),
            ("db_host", "DB_HOST"),
        ]
        validated_envs_obj = {}
        validation_errors: list[str] = []

        for obj_key, env in needed_env:
            found_env = os.getenv(env)
            if found_env is None:
                validation_errors.append(f"{env} env variable is not set")
            else:
                validated_envs_obj[obj_key] = found_env
        if len(validation_errors) != 0:
            raise EnvSetupException(validation_errors)

        result_obj = TypedEnvs(**validated_envs_obj)
        return result_obj

"""Fetch secrets: prefer env var, fall back to Key Vault via managed identity."""

import os
from typing import Any

from dotenv import load_dotenv

load_dotenv()


def get_secret(name: str, env_fallback: str | Any) -> str | None:
    """Return the secret from the env var if set, else fetch from Key Vault.

    Local dev sets env vars (used directly). Deployed containers leave secret
    env vars unset and have KEY_VAULT_NAME, so the Key Vault path is used.
    """
    env_value = os.getenv(env_fallback)
    if env_value:
        return env_value

    vault_name = os.getenv("KEY_VAULT_NAME")
    if not vault_name:
        return None

    from azure.identity import DefaultAzureCredential
    from azure.keyvault.secrets import SecretClient

    client_id = os.getenv("AZURE_CLIENT_ID")
    credential = DefaultAzureCredential(managed_identity_client_id=client_id)
    client = SecretClient(
        vault_url=f"https://{vault_name}.vault.azure.net",
        credential=credential,
    )
    return str(client.get_secret(name).value)

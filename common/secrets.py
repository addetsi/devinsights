"""Fetch secrets from Azure Key Vault via managed identity, or fall back to env vars locally."""

import os
from typing import Any


def get_secret(name: str, env_fallback: str) -> Any | None:
    """Fetch a secret from key vault if KEY_VAULT_NAME is set, else from an env var"""
    vault_name = os.getenv("KEY_VAULT_NAME")
    if vault_name:
        from azure.identity import DefaultAzureCredential
        from azure.keyvault.secrets import SecretClient

        client_id = os.getenv("AZURE_CLIENT_ID")
        credential = DefaultAzureCredential(managed_identity_client_id=client_id)

        client = SecretClient(
            vault_url=f"https://{vault_name}.vault.azure.net",
            credential=credential,
        )
        return client.get_secret(name).value
    return os.getenv(env_fallback)

import os

import keyring


SERVICE_NAME = "katago-ai-teacher"
NVIDIA_API_KEY_USERNAME = "nvidia_api_key"
GITHUB_TOKEN_USERNAME = "github_token"


def normalize_api_key(api_key):
    """Trim whitespace and common quote wrappers from API key values."""
    return (api_key or "").strip().strip("\"'")


def get_nvidia_api_key():
    """Read NVIDIA API key from keyring first, then environment variables."""
    try:
        keyring_value = normalize_api_key(keyring.get_password(SERVICE_NAME, NVIDIA_API_KEY_USERNAME))
        if keyring_value:
            return keyring_value
    except keyring.errors.KeyringError:
        pass

    return normalize_api_key(
        os.getenv("NVIDIA_API_KEY")
        or os.getenv("KATAGO_NVIDIA_API_KEY")
    )


def set_nvidia_api_key(api_key):
    """Store NVIDIA API key in the OS keyring. Does not write to .env."""
    keyring.set_password(SERVICE_NAME, NVIDIA_API_KEY_USERNAME, normalize_api_key(api_key))


def get_github_token():
    """Read GitHub Models token from keyring first, then environment variables."""
    try:
        keyring_value = normalize_api_key(keyring.get_password(SERVICE_NAME, GITHUB_TOKEN_USERNAME))
        if keyring_value:
            return keyring_value
    except keyring.errors.KeyringError:
        pass

    return normalize_api_key(
        os.getenv("GITHUB_TOKEN")
        or os.getenv("KATAGO_GITHUB_TOKEN")
    )


def set_github_token(token):
    """Store GitHub Models token in the OS keyring. Does not write to .env."""
    keyring.set_password(SERVICE_NAME, GITHUB_TOKEN_USERNAME, normalize_api_key(token))

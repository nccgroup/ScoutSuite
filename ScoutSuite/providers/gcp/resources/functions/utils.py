from ScoutSuite.providers.utils import is_secret


def get_environment_secrets(environment_variables):
    secrets = []
    for k, v in environment_variables.items():
        secrets.append(is_secret(k))
        secrets.append(is_secret(v))
    # return None values
    return [secret for secret in secrets if secret]

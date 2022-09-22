from re import sub


def format_resource_kind(kind: str):
    return (kind[0] + sub('([A-Z])', '_\\1', kind[1:])).lower()

def format_api_version(api_version: str):
    parts = api_version.split('/')
    if len(parts) < 2:
        return api_version
    formatted_version = f'''{parts[1]}-{parts[0]}'''.replace('.', '-')
    return formatted_version

def format_resource_name(name: str):
    if not name: return ''
    return sub('[^a-zA-Z0-9]', '-', name)

def format_resource_id(name: str, namespace: str = ''):
    formatted_id = format_resource_name(name)
    if namespace:
        formatted_ns = format_resource_name(namespace)
        formatted_id = f'--{formatted_ns}--{formatted_id}'
    return formatted_id
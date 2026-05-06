import re
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


def camelize_key(key: str) -> str:
    # snake_case → camelCase
    parts = key.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])


def camelize(data):
    if isinstance(data, dict):
        return {camelize_key(k): camelize(v) for k, v in data.items()}
    if isinstance(data, list):
        return [camelize(i) for i in data]
    return data


class CamelCaseJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        data = camelize(data)
        return super().render(data, accepted_media_type, renderer_context)


def decamelize_key(key: str) -> str:
    # camelCase → snake_case
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", key)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def decamelize(data):
    if isinstance(data, dict):
        return {decamelize_key(k): decamelize(v) for k, v in data.items()}
    if isinstance(data, list):
        return [decamelize(i) for i in data]
    return data


class CamelCaseJSONParser(JSONParser):
    def parse(self, stream, media_type=None, parser_context=None):
        data = super().parse(stream, media_type, parser_context)
        return decamelize(data)

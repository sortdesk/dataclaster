from dataclasses import field as fieldtype, dataclass
from typing import Union, Any

import json
import jsonpath_rw

from common import Config, BaseMixin
from exceptions import TooManyMatchesError, NoMatchesError


class JSONConfig(Config):
    def __init__(self, path: str) -> None:
        self.path = path


class JSONMixin(BaseMixin):

    @classmethod
    def _process_field(cls, field: fieldtype, json_dict: dict) -> Any:

        cls.raise_for_types_not_supported(field.type)

        if hasattr(field, "config"):
            if not isinstance(field.config, JSONConfig):
                raise ValueError(
                    f"You must pass a valid instance of JSONConfig to the `config` parameter on {field.name}"
                )
            return cls._process_field_with_config(field, json_dict)
        else:
            return cls._process_field_without_config(field, json_dict)

    @classmethod
    def _process_field_with_config(cls, field: fieldtype, json_dict: dict) -> Any:
        expr = jsonpath_rw.parse(field.config.path)
        value = [match.value for match in expr.find(json_dict)]

        if not value:
            raise NoMatchesError(
                f"Couldn't find any matches for the path '{field.config.path}' of field {field.name}"
            )

        is_list = cls.get_base_type(field.type) == list
        has_several_matches = len(value) > 1

        if not is_list:
            if has_several_matches:
                raise TooManyMatchesError(
                    f"{field.name} or type {field.type} has too many matches for the path '{field.config.path}'"
                )
            value = value[0]

        return cls.cast_value_to_type(value, field.type)

    @classmethod
    def _process_field_without_config(cls, field: fieldtype, json_dict: dict) -> Any:
        value = json_dict[field.name]
        return cls.cast_value_to_type(value, field.type)

    @classmethod
    def from_json(cls, json_dict: Union[str, dict], deserialize: bool = False) -> dataclass:
        if deserialize:
            json_dict = json.loads(json_dict)

        dc = cls.to_dataclass(json_dict)
        return dc

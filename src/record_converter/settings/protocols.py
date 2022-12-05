"""_summary_
"""
from typing import Protocol, Optional, Any, Dict


class DataClass(Protocol):
    __dataclass_fields__: dict[str, Any]


class DateConvertor(Protocol):
    """Protocol class to define minimum interface of a DateConvertor."""

    def __init__(
            self,
            rules: Dict,
            record: Dict):
        ...

    def convert_date(self) -> Dict:
        ...


class Convertor(Protocol):
    """Protocol class to define minimum interface of a Convertor."""

    def __init__(
            self,
            rules: Dict,
            record: Dict,
            data_classes: Dict[str, DataClass],
            command_class=None,
            date_coverter_class=None,
            convertor_class=None,
            skip_response=None):
        ...
    
    def convert(self) -> Dict:
        ...

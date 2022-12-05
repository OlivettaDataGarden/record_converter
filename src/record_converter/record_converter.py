"""
Module to define record conversion functionality.

Classes:
    - RecordConverter: Public class to be used to convert records based upon
                       conversion definition in YAML file

"""
from typing import Any, Dict, Optional

from helper.dict_helper import keys_in_lower_case
from helper.read_yaml import ConvertYamlToDict

from record_converter.converter import ConvertRecord
from record_converter.settings import DataClass

class RecordConverter():
    """
    Class that coverts a input record to a format as defined by a yaml file
    provided when creating the class instance.

    args:
        yaml_file (str)
            YAML file including directory to be processed int
            self.conversion_rules by __init__()
        keys_in_lower_case (bool)
            if set to true ensures that all keys in record to be converted will
            be in lower case

    public methods:
        - convert: converts record according to rules

    The yaml file is converted into a dict which is used to call the
    ConvertRecord class.
    """

    def __init__(
            self,
            yaml_file: str,
            keys_in_lower_case: bool=True,
            data_classes: Optional[Dict[str, DataClass]]=None,
            command_class: Optional[Any]=None,
            skip_response: Optional[Any]=None):
        conversion_dict = ConvertYamlToDict(yaml_file)
        self.data_classes = data_classes
        self.command_class = command_class
        if conversion_dict.is_valid():
            self.conversion_rules = conversion_dict.provide_dict()
        self.keys_in_lower_case = keys_in_lower_case
        self.skip_response = skip_response

    def convert(self, record: Dict) -> Dict:
        """
        returns conversion of record according to rules in
        self.conversion_rules

        args:
            record (dict): record to be coverted

        returns:
            dict: coverted record
        """
        if self.keys_in_lower_case:
            record = keys_in_lower_case(record)
        return ConvertRecord(
            rules=self.conversion_rules,
            record=record,
            command_class=self.command_class,
            data_classes=self.data_classes or {},
            skip_response=self.skip_response
        ).convert()

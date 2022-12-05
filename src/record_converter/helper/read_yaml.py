"""
Module to provide a yaml reader including validation.

readers:
    ConvertYamlToDict: returns a dict from a valid YAML
"""
import yaml
from typing import Dict, Optional


class ConvertYamlToDict():
    """
    Class to create a dict from a YAML file

    paramaters:
        - filename: filename including path of yaml file

    public methods:
        - provide_dict
    """

    def __init__(self, filename: str):
        self.filename: str = filename
        self._dict: Optional[Dict] = None
        self._error: bool = False

    def provide_dict(self):
        """
        Get dict form form YAML file.
        """
        if self._error:
            raise ValueError(
                ''.join([
                    'Calling provide_dict() while yaml file has been ',
                    'invalidated.'
                ])
            )

        if not self._dict:
            raise ValueError(
                ''.join([
                    'Calling provide_dict() yaml file hase not yet been ',
                    'processed. First call `is_valid()` method to process '
                    'YAML file.'
                ])
            )

        return self._dict

    def _to_dict(self) -> None:
        """
        Method to create dict from the yaml file. If yaml file can not be
        converted to dict self._error is set to True.
        """
        # if _to_dict() has already been called return.
        if self._error or self._dict:
            return

        try:
            self._dict = yaml.load(
                open(self.filename, 'r'), Loader=yaml.FullLoader)
        except yaml.scanner.ScannerError as e:
            print(e)
            self._error = True

    def is_valid(self) -> bool:
        """
        Method to indicate if a yaml file could be converted succesfully into a
        dict. If conversion has not yet been done it will be initiated by this
        method.

        args:
            - None

        returns:
            Boolean: True if dict can be created, False if not
        """
        if not self._dict and not self._error:
            self._to_dict()

        return not self._error

    def error(self) -> bool:
        """Returns error status """
        return self._error

"""Module to define Conditions class.

Classes:
    - Conditions
"""
from datetime import datetime

from typing import Optional

from record_converter.settings import ConditionsDict, ConditionValue


class Conditions():
    """
    Class to evaluate conditions for a given value.j

    args:
        provided_condions (dict):
            dict in form of
                {condition: value for condition / None}
            multiple conditions can be added to a single dict (as
            long as they are different conditions)

        value (str, int, float): 
            the value that is used to evaluate the condition.

    available conditions:
        is_a_string:
            Checks if value is of type string, No specific argument needed
        is_not_a_string:
            Checks if value is not of type string, No specific argument needed
        is_null:
            takes true ot false as argument and checks if fieldname is None
            or is not None depending on the argument
        date_not_today:
            takes a date in string format (YYYY-MM-DD) and check that this date is not today. Input date is not checked if it has the right format.
        str_length:
            takes an int as condition input and checks if given value has
            exactly that length.
        field_does_not_exist:
            checks if given field exists and returns False if it exists
        field_does_exist:
            checks if given field exists and returns True if it exists
        is_null:
            takes a boolean as argument and check the field value accordingly
            for a None value

    """

    def __init__(
        self,
        provided_conditions: Optional[ConditionsDict] = None,
        value: Optional[ConditionValue] = None
    ):
        self.provided_conditions: ConditionsDict = \
            provided_conditions or ConditionsDict({})
        self.value = value

    def evaluate(self) -> bool:
        """Evaluetes the given conditions with the given value

        Returns:
            Boolean: Returns true if all conditions are met for given
                     value. If not all conditions are met False is returned

        """
        # be default evaluate method returns True unless one of the given
        # conditions is no met
        all_conditions = True

        for condition in self.provided_conditions:
            if condition in dir(self):
                all_conditions = all_conditions and getattr(self, condition)()
            else:
                raise NotImplementedError(f'Condition {condition}')

        return all_conditions

    def date_not_today(self) -> bool:
        return not (datetime.today().strftime("%Y-%m-%d") == self.value)

    def is_not_a_string(self) -> bool:
        return (not isinstance(self.value, str))

    def is_a_string(self) -> bool:
        return isinstance(self.value, str)

    def str_length(self) -> bool:
        try:
            return len(str(self.value)) == \
                self.provided_conditions['str_length']
        except (TypeError):
            raise

    def field_does_not_exist(self) -> bool:
        return self.value is None

    def field_does_exist(self) -> bool:
        return self.value is not None

    def is_null(self) -> bool:
        """
        check if value is None or not None depending on value of condition field
        'is_null'
        """
        return (self.value is None) == self.provided_conditions['is_null']

    def equals(self) -> bool:
        return self.value == self.provided_conditions['equals']

    def in_list(self) -> bool:
        return self.value in self.provided_conditions['in_list']

    def does_not_equal(self) -> bool:
        return self.value != self.provided_conditions['does_not_equal']

    def contains(self) -> bool:
        return self.provided_conditions['contains'] in self.value

    def does_not_contain(self) -> bool:
        return not (self.provided_conditions['does_not_contain'] in self.value)

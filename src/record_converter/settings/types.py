from typing import NewType, Dict, Optional, Union, List

ConditionsDict = NewType(
    'ConditionsDict', Dict[str, Optional[Union[bool, str, int, List]]])

ConditionValue = Union[str, int, float]


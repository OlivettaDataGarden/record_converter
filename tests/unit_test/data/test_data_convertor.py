"""Module to define test data for converter class tests
"""
from dataclasses import dataclass, field
from typing import List


@dataclass
class PhoneNumber:
    phone_nr: str
    phone_type: str = None


@dataclass
class DataClassTester:
    field1: str = None


@dataclass
class DataClassWithMethodTester:
    field1: str = None
    phones: List[PhoneNumber] = field(default_factory=list)

    def add_phone(self, phone_nr, phone_type=None):
        self.phones.append(
            PhoneNumber(
                phone_nr=phone_nr,
                phone_type=phone_type
            )
        )


DATA_CLASSES = {
    'test_data': DataClassTester,
    'data_class_with_method': DataClassWithMethodTester
}

BASE_PARAMS = {
    'record': {'field1': 'a'},
    'rules': {
        'new_field': 'field1'
    },
    'expected_results': {
        'new_field': 'a'
    },
    'data_classes': {}
}

PARAMS_NESTED_FIELD = {
    'record': {'field1': {
        'field2': {
            'field3': 'a'}}},
    'rules': {
        'new_field': 'field1.field2.field3'
    },
    'expected_results': {
        'new_field': 'a'
    },
    'data_classes': {}
}

PARAMS_NESTED_FIELD_WITH_SPECIAL_CHAR = {
    'record': {'field1!': {
        'field#2': {
            'field-3': 'a'}}},
    'rules': {
        'new_field': 'field1!.field#2.field-3'
    },
    'expected_results': {
        'new_field': 'a'
    },
    'data_classes': {}
}

PARAMS_ALLOW_NONE_VALUE_NONE = {
    'record': {'input': 'existing value'},
    'rules': {'output': {
        '$allow_none_value': {
            'field_name': 'other_input'
        }}},
    'expected_results': {'output': None},
    'data_classes': {}
}

PARAMS_ALLOW_NONE_VALUE_WITH_VALUE = {
    'record': {'input': 'existing value'},
    'rules': {'output': {
        '$allow_none_value': {
            'field_name': 'input'
        }}},
    'expected_results': {'output': 'existing value'},
    'data_classes': {}
}

PARAMS_RETURN_EXPLICIT_NONE_VALUE_SET_TO_NON = {
    'record': {},
    'rules': {'output': {
        '$set_to_none_value': 'test'}},
    'expected_results': {'output': None},
    'data_classes': {}
}

PARAMS_RETURN_NONE_FROM_COMMAND = {
    'record': {'field1': 'a'},
    'rules': {
        'test': {
            '$to_int': {
                'fieldname': 'field2'
            }
        }
    },
    'expected_results': {},
    'data_classes': {}
}


PARAMS_COMMAND_IN_ROOT = {
    'record': {'field1': '1', 'key': 'keyname'},
    'rules': {
        'test': {'$fixed_value': 'test'},
        '$join_key_value': {
            'key': 'key',
            'value': 'field1'
        }

    },
    'expected_results': {
        'test': 'test',
        'keyname': '1'
    },
    'data_classes': {}
}

PARAMS_SKIP_TRUE = {
    'record': {'field1': 'a'},
    'rules': {
        '$skip': {
            'fieldname': 'field1',
            'condition': {
                'equals': 'a'}
        },
        'new_field': 'field1'
    },
    'expected_results': None,
    'data_classes': {}
}

PARAMS_SKIP_FALSE = {
    'record': {'field1': 'a'},
    'rules': {
        '$skip': {
            'fieldname': 'field1',
            'condition': {
                'does_not_equal': 'a'}
        },
        'new_field': 'field1'
    },
    'expected_results': {
        'new_field': 'a'
    },
    'data_classes': {}
}

PARAMS_SKIP_INVALID = {
    'record': {'field1': 'a'},
    'rules': {
        '$skip': {
            'fieldname': 'field1',
        },
        'new_field': 'field1'
    },
    'expected_results': {
        'new_field': 'a'
    },
    'data_classes': {}
}

PARAMS_CONVERT = {
    'record': {'field1': 'a'},
    'rules': {
        '$convert1': {
            'fieldname': 'field1',
            'actions': [{"add_postfix": 'bcd'}]
        },
        'new_field': 'field1'
    },
    'expected_results': {
        'new_field': 'abcd'
    },
    'data_classes': {}
}

PARAMS_DATE_CONVERT = {
    'record': {'field1': '01-02-2021'},
    'rules': {
        '$format_date1': {
            'date_field': 'field1',
            'format': 'DD-MM-YYYY'
        },
        'new_field': 'field1'
    },
    'expected_results': {
        'new_field': '2021-02-01'
    },
    'data_classes': {}
}

PARAMS_PROCESS_COMMAND = {
    'record': {'field1': 'A', 'field2': 'B'},
    'rules': {
        'new_field': {
            '$join': ['$seperator_', 'field1', 'field2']
        }},
    'expected_results': {
        'new_field': 'A_B'
    },
    'data_classes': {}
}

PARAMS_DICT_RULE = {
    'record': {'field1': 'abcd'},
    'rules': {
        'new_field': {
            'nested_field': 'field1'
        }
    },
    'expected_results': {
        'new_field': {'nested_field': 'abcd'}
    },
    'data_classes': {}
}


PARAMS_DATA_CLASS_NOT_DEFINED = {
    'record': {'field1': 'abcd'},
    'rules': {
        'new_field': {
            '$data_class': {
                'data_class_name': 'not_defined_name',
                'params': {
                    'new_field': {
                        'nested_field': 'field1'
                    }}}}},
    'expected_results': {
        'new_field': {'nested_field': 'abcd'}
    },
    'data_classes': {}
}

PARAMS_DATA_CLASS = {
    'record': {'field1': 'abcd'},
    'data_classes': DATA_CLASSES,
    'rules': {
        'new_field': {
            '$data_class': {
                'data_class_name': 'test_data',
                'params': {
                    'field1': {
                        'nested_field': 'field1'
                    }}}}},
    'expected_results': {
        'new_field': {'field1': {'nested_field': 'abcd'}}
    }
}

PARAMS_DATA_CLASS_WITH_METHOD = {
    'record': {
        'field1': 'abcd',
        'contact': {
            "phones": [
                {
                    "type": "PHONE1",
                    "number": "+49 (0)30 54860523",
                    "uri": "tel:+493054860523"
                },
                {
                    "type": "MOBILE",
                    "number": "+49 (0)177 4564790",
                    "uri": "tel:+491774564790"
                },
                {
                    "type": "FAX",
                    "number": "+49 (0)30 54860528"
                }
            ]
        }
    },
    'data_classes': DATA_CLASSES,
    'rules': {
        'new_field': {
            '$data_class': {
                'data_class_name': 'data_class_with_method',
                'params': {
                    'field1': {'nested_field': 'field1'},
                },
                'methods': [
                    {'add_phone': {
                        '$from_list': {
                            'list_field_name': 'contact.phones',
                            'phone_nr': 'number',
                            'phone_type': 'type'}
                    }}
                ]
            }
        }
    },
    'expected_results':
        {
        'new_field':
            {
                'field1': {'nested_field': 'abcd'},
                'phones': [
                    {'phone_nr': '+49 (0)30 54860523', 'phone_type': 'PHONE1'},
                    {'phone_nr': '+49 (0)177 4564790', 'phone_type': 'MOBILE'},
                    {'phone_nr': '+49 (0)30 54860528', 'phone_type': 'FAX'}
                ]
            }
    }
}

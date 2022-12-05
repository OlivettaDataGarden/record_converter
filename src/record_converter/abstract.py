import jmespath


class AbstractCommand():

    def __init__(self, record, rules):
        self.rules = rules
        self.record = record

    def convert(self):
        raise NotImplementedError

    def _get_field(self, key, rec=None):
        record = rec or self.record
        if key:
            try:
                return jmespath.search(key, record)
            except jmespath.exceptions.ParseError:
                pass

        return None

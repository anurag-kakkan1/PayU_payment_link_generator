from .constants import CommonConstants

class DataValidator():

    def validate(self, data):
        """
        :param data:
        :return:
        """
        self.check_if_fields_are_present(data)

    def check_if_fields_are_present(self, data):
        """
        Checks if the data contains the required keys.
        :param data: [{"key1": "value1", "key2": "value2"}, {"key1": "value3", "key2": "value4"}]
        :return:
        """
        if data:
            keys = list(data[0].keys())
            for required in CommonConstants.REQUIRED_HEADER_FIELDS:
                if required not in keys:
                    raise Exception('File is missing required field: {} '.format(required)) 
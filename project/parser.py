import re
from datetime import datetime

class Parser:
    """
    This class has a set of methods to handle with events sended by the energy sensor.
    """

    REGEX_GROUP = r"([a-z]|[A-Z])+( |[a-z]|[A-Z])*\:( |\w|\=|\;|\.|\-|\,|(\d+\:\d+\:\d+))*(?!( |[a-z]|[A-Z])*\:)"
    REGEX_SUBGROUP = r'^(?P<head>\w+)\:(?P<tail>.*)'

    @staticmethod
    def parse(event_string):
        """
        This method is a dictionary factory, which transform a event string into a dictionary with the respective values.
        :param event_string: a event_string sended by the energy sensor.
        :return: a dictionary with the event values or None if error in the format of event_string
        """
        result_dict = dict(
            device_id = None,
            device_fw = None,
            evt = None,
            alarms = dict(),
            power = dict(
                active = None,
                reactive = None,
                appearent = None
            )
        )

        info_groups = [value.group() for value in re.finditer(Parser.REGEX_GROUP, event_string)]
        info_groups = map(lambda value: value.replace(' ','').lower(), info_groups)
        print("info_groups -> ", info_groups)

        splitted_groups = []
        for group in info_groups:
            re_result = re.match(Parser.REGEX_SUBGROUP, group)
            head = re_result.group('head')
            tail = re_result.group('tail')
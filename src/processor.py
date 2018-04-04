from collections import defaultdict
import math


class User:
    def __init__(self):
        # times are in datatime.
        self.session_start = 0  # datatime of the first request
        self.session_write = 0  # time slot to write to file if no more request
        self.session_last = 0   # will be eliminated in final version

        def session_length(inactivity_period):
            last_request = self.session_write - inactivity_period
            deltat = last_request - self.session_start + 1
            deltat_seconds = math.ceil(deltat.total_seconds())
            return deltat_seconds


class Processor:
    pass

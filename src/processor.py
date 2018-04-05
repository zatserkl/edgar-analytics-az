from filestream import DataStream
from collections import defaultdict
import math
import datetime


class User:
    def __init__(self):
        # times are in datatime.
        self.session_start = 0  # datatime of the first request
        self.session_write = 0  # time slot to write to file if no more request
        self.session_last = 0   # will be eliminated in final version

    def setup(self, ip, date_time):
        self.ip = ip
        self.date_time = date_time

    def session_length(self, inactivity_period):
        last_request = self.session_write - inactivity_period
        deltat = last_request - self.session_start + 1
        deltat_seconds = math.ceil(deltat.total_seconds())
        return deltat_seconds


class Processor:
    def __init__(self, fname_input, inactivity_period, fname_output):
        self.inactivity_period = inactivity_period

        print("fname_input:", fname_input)
        print("inactivity_period =", inactivity_period)

        self.dataStream = DataStream(fname_input)
        self.outfile = open(fname_output, "w")

        self.userDict = defaultdict(User)
        self.timeDict = defaultdict(datetime.datetime)

    def flush(self):
        print("EOF: flush the output file")

    def process_request(self, fields):
        """ Processes the request
        """
        print(fields)

        user = User()
        if user.session_start > 0:
            print("user:", user)

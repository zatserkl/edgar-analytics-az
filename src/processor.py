# Andriy Zatserklyaniy <zatserkl@gmail.com> Apr 4, 2018

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

    def session_length(self, inactivity_period):
        last_request = self.session_write - inactivity_period
        deltat = last_request - self.session_start + 1
        deltat_seconds = math.ceil(deltat.total_seconds())
        return deltat_seconds


class Processor:
    def __init__(self, fname_input, inactivity_period, fname_output):
        self.inactivity_period = inactivity_period

        self.dataStream = DataStream(fname_input)
        self.outfile = open(fname_output, "w")

        self.userDict = defaultdict(User)
        self.timeDict = defaultdict(datetime.datetime)

    def flush(self):
        print("EOF: flush the rest into the output file")

    def process_request(self, ip, date_time):
        """ Processes the request from ip at datetime date_time
        """
        self.userDict[ip].date_time = date_time
        print(ip, self.userDict[ip].date_time)

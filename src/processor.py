# Andriy Zatserklyaniy <zatserkl@gmail.com> Apr 4, 2018

from filestream import DataStream
from collections import defaultdict
import math
import datetime


class User:
    """ Keeps the number and times of requests.
    Attributes:
        inactivity_period (timedelta): class variable common for all instances
        session_start (datetime): Time of the first request
        session_write (datetime): Time to write to file if no more requests
    """
    inactivity_period = datetime.timedelta()  # class variable, common for all

    def __init__(self):
        # times are in datatime.
        self.session_start = 0  # datatime of the first request
        self.session_write = 0  # time slot to write to file if no more request
        # self.session_last = 0   # will be eliminated in final version
        self.nrequests = 0

    def __str__(self):
        return "session_start: {} session_write: {} nrequests = {}".format(
            self.session_start, self.session_write, self.nrequests)

    def session_length(self):
        last_request = self.session_write - User.inactivity_period
        deltat = last_request - self.session_start + 1
        deltat_seconds = math.ceil(deltat.total_seconds())
        return deltat_seconds

    def process_request(self, date_time):
        if self.nrequests == 0:
            self.session_start = date_time

        self.session_write = date_time + User.inactivity_period
        self.nrequests += 1


class Processor:
    def __init__(self, fname_input, inactivity_period, fname_output):
        # set User class variable
        User.inactivity_period = datetime.timedelta(seconds=inactivity_period)

        self.dataStream = DataStream(fname_input)
        self.outfile = open(fname_output, "w")

        self.userDict = defaultdict(User)   # key: ip
        self.timeDict = defaultdict(list)   # key: time to write to output file

    def flush(self):
        print("EOF: flush the rest into the output file")

    def process_request(self, ip, date_time):
        """ Processes the request from ip at datetime date_time
        """
        # add user to ip dictionary
        self.userDict[ip].process_request(date_time)
        print(ip, self.userDict[ip])

        # add user to time dictionary
        self.timeDict[self.userDict[ip].session_write].append(ip)
        # print(self.timeDict[self.userDict[ip].session_write])

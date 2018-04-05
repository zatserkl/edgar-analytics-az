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

        self.time_min = None

    def flush(self):
        print("EOF: flush the rest into the output file")

    def write_time_slot(self, time_slot):
        print("*** write slot time_min", str(time_slot))
        print("    timeDict[time_min]:", self.timeDict[time_slot])
        for ip in self.timeDict[time_slot]:
            print("   ** candidate", self.userDict[ip])
            if self.userDict[ip].session_write == time_slot:
                print("   **--> write to file", ip)

    def process_request(self, ip, date_time):
        """ Processes the request from ip at datetime date_time
        """
        if self.time_min is None:
            self.time_min = date_time

        print("-->", str(date_time), "   time_min =", str(self.time_min))

        if date_time - self.time_min > User.inactivity_period:
            # print(".. write slot", str(self.time_min))
            self.write_time_slot(self.time_min + User.inactivity_period)

        # add user to ip dictionary
        self.userDict[ip].process_request(date_time)
        print("{:16} {}".format(ip, self.userDict[ip]))

        # add user to time slot session_write
        time_slot = self.userDict[ip].session_write
        print("append ip", ip, "to time_slot", time_slot)
        self.timeDict[self.userDict[ip].session_write].append(ip)
        print("  timeDict", self.timeDict[self.userDict[ip].session_write])

    def bottom(self):
        pass

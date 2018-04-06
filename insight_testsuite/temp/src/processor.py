# Andriy Zatserklyaniy <zatserkl@gmail.com> Apr 4, 2018

from filestream import DataStream
from collections import defaultdict, OrderedDict
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
    second1 = datetime.timedelta(seconds=1)   # constant: 1 second

    def __init__(self):
        # times are in datatime.
        self.session_start = 0  # datatime of the first request
        self.session_write = 0  # time slot to write to file
        self.nrequests = 0

    def __str__(self):
        return "session_start: {} session_write: {} nrequests = {}".format(
            self.session_start, self.session_write, self.nrequests)

    def session_length(self):
        last_request = self.session_write - User.inactivity_period
        deltat = last_request - self.session_start + User.second1
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

        self.userDict = OrderedDict()      # key: ip, keep input order
        self.timeDict = defaultdict(list)  # key: time to write to output file

        self.time_min = None               # current time slot to write

    def flush(self):
        # print("\nEOF: flush the rest into the output file")
        # for ip, user in self.userDict.items():
        #     print("{:16} start: {} write: {}".format(ip,
        #           user.session_start, user.session_write))
        # print()

        # dump the userDict into the output file in the input order

        for ip, user in self.userDict.items():
            session_length = user.session_length()
            nrequests = user.nrequests
            # print("      ==> write to file", ip,
            #       "length:", session_length, "nrequests:", nrequests)
            session_end = user.session_write - User.inactivity_period
            s = (str(ip) + "," +
                 str(user.session_start) + "," +
                 str(session_end) + "," +
                 str(session_length) + "," +
                 str(nrequests) + "\n")
            self.outfile.write(s)

    def write_time_slot(self, date_time):
        """ Writes slot self.time_min into output file.
        """
        # print("  *** write slot time_min", self.time_min)
        # print("    timeDict[time_min]:", self.timeDict[self.time_min])
        #
        # print("self.userDict:")
        # for key, value in self.userDict.items():
        #     print("key:", key, "   value:", value)
        # print()

        for ip in self.timeDict[self.time_min]:
            try:
                user = self.userDict[ip]
            except KeyError as e:
                print("KeyError e =", e)
                print("ip =", ip)
                exit()
            # print("      candidate ip =", ip, user)
            if user.session_write == self.time_min:
                session_length = user.session_length()
                nrequests = user.nrequests
                # print("      ==> write to file", ip,
                #       "length:", session_length, "nrequests:", nrequests)
                session_end = user.session_write - User.inactivity_period
                s = (str(ip) + "," +
                     str(user.session_start) + "," +
                     str(session_end) + "," +
                     str(session_length) + "," +
                     str(nrequests) + "\n")
                self.outfile.write(s)
                # delete this ip from userDict
                del(self.userDict[ip])

        # delete this time slot
        # print("    bef del: timeDict[time_min]:", self.timeDict[self.time_min])
        # for ip in self.timeDict[self.time_min]:
        #     if ip in self.userDict:
        #         del(self.userDict[ip])
        del(self.timeDict[self.time_min])

        # update time_min
        time_last = date_time + User.inactivity_period
        self.time_min += User.second1
        while self.time_min not in self.timeDict.keys():
            if self.time_min >= time_last:
                break
            self.time_min += User.second1
        # print("  new time_min:", self.time_min)

    def process_request(self, ip, date_time):
        """ Processes the request from ip at datetime date_time
        """
        if self.time_min is None:
            self.time_min = date_time + User.inactivity_period

        # last slot to write
        self.time_last = date_time + User.inactivity_period

        # print("-->", date_time, "   time_min =", self.time_min)

        while self.time_min < date_time:
            self.write_time_slot(date_time)

        # add user to ip dictionary
        if ip not in self.userDict:
            self.userDict[ip] = User()
        self.userDict[ip].process_request(date_time)
        # print("{:16} {}".format(ip, self.userDict[ip]))

        # add user to time slot session_write
        time_slot = self.userDict[ip].session_write
        # print("append ip", ip, "to time_slot", time_slot)
        # --KeyError- self.timeDict[time_slot].append(ip)
        if ip not in self.timeDict[time_slot]:
            # print("append ip", ip, "to time_slot", time_slot)
            self.timeDict[time_slot].append(ip)

        # print("  timeDict", self.timeDict[self.userDict[ip].session_write])

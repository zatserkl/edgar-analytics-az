# Andriy Zatserklyaniy <zatserkl@gmail.com> Apr 4, 2018

# current command line:
# python src/sessionization.py input/log.csv

from filestream import DataStream
from processor import User
import sys


def main(fname, inactivity_period):
    print("fname:", fname)
    print("inactivity_period =", inactivity_period)

    dataStream = DataStream(fname)

    while True:
        try:
            fields = dataStream.next_fields()
        except StopIteration:
            print("EOF reached")
            return
        print(fields)

        user = User()
        if user.session_start > 0:
            print("user:", user)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:", __file__, "logfile inactivity-file")
        exit()

    fname = sys.argv[1]
    fname_inactivity = sys.argv[2]

    # read the inactivity_period
    inactivity_period = 0
    with open(fname_inactivity) as file_inactivity:
        inactivity_period = int(file_inactivity.readline())

    main(fname, inactivity_period)

# Andriy Zatserklyaniy <zatserkl@gmail.com> Apr 4, 2018

from filestream import DataStream
from processor import Processor
import sys


def wait(debug):
    if debug:
        c = input("<CR>=Continue, q=Quit ")
        if c.upper() == 'Q':
            return True
    return False


def main(fname_input, inactivity_period, fname_output, debug=False):

    dataStream = DataStream(fname_input)
    processor = Processor(fname_input, inactivity_period, fname_output)

    line_number = 0
    while True:
        line_number += 1
        if debug:
            print("line", line_number)
        try:
            ip, date_time = dataStream.next_fields()
            processor.process_request(ip, date_time)
        except StopIteration:
            processor.flush()
            break

        if wait(debug):
            break


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage:", __file__,
              "input-file inactivity-file output-file [debug=False/True]")
        exit()

    fname_input = sys.argv[1]
    fname_inactivity = sys.argv[2]
    fname_output = sys.argv[3]

    debug = False
    if len(sys.argv) > 4:
        debug = sys.argv[4].lower() == "true"

    inactivity_period = 0
    with open(fname_inactivity) as file_inactivity:
        inactivity_period_str = file_inactivity.readline()
        try:
            inactivity_period = int(inactivity_period_str)
        except ValueError as e:
            print(e)
            exit()

    main(fname_input, inactivity_period, fname_output, debug)

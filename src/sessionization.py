# Andriy Zatserklyaniy <zatserkl@gmail.com> Apr 4, 2018

from filestream import DataStream
from processor import Processor
import sys


def main(fname_input, inactivity_period, fname_output):
    # print("fname_input:", fname_input)
    # print("inactivity_period =", inactivity_period)
    # print("fname_output:", fname_output)

    dataStream = DataStream(fname_input)
    processor = Processor(fname_input, inactivity_period, fname_output)

    line_number = 0
    while True:
        line_number += 1
        print("line", line_number)
        try:
            ip, date_time = dataStream.next_fields()
            processor.process_request(ip, date_time)
        except StopIteration:
            processor.flush()
            break

        # debug
        c = input("<CR>=Continue, q=Quit ")
        if c.upper() == 'Q':
            break


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage:", __file__, "input-file inactivity-file output-file")
        exit()

    fname_input = sys.argv[1]
    fname_inactivity = sys.argv[2]
    fname_output = sys.argv[3]

    inactivity_period = 0
    with open(fname_inactivity) as file_inactivity:
        inactivity_period = int(file_inactivity.readline())

    main(fname_input, inactivity_period, fname_output)

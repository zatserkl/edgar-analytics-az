from filestream import DataStream
import sys


def main(fname):
    print("fname:", fname)
    dataStream = DataStream(fname)
    try:
        fields = dataStream.next_fields()
    except StopIteration:
        print("EOF")
    print(fields)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:", __file__, "filename")
        exit()

    fname = sys.argv[1]
    main(fname)

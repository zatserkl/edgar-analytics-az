class FileStream(object):
    """ Creates generator for the file content.
    The method next_line returns the next line from the generator.
    Calling rountine should catch StopIteration in case of EOF.
    """
    def __init__(self, fname):
        self.fname = fname
        self.gen_stream = self.__stream(self.fname)

    def __stream(self, fname):
        """ Create generator for lines
        """
        with open(fname) as filestream:
            line = filestream.readline()
            while line:
                yield line
                line = filestream.readline()

    def next_line(self):
        """ Returns the next line from the generator.
        Raises StopIteration at EOF. Catch it in the calling routine.
        """
        return next(self.gen_stream).strip('\n')  # raises StopIteration at EOF


class DataStream(FileStream):
    def __init__(self, fname):
        super().__init__(fname)
        # read the header line
        names = []
        try:
            names = list(self.next_line().split(','))
        except StopIteration:
            print("Terminated: no header line")
            raise StopIteration
        print("names:\n", names)

    def next_fields(self):
        list_str = list(next(self.gen_stream).split(','))
        print("list_str", list_str)
        ip = list_str[0]
        date = list_str[1]
        time = list_str[2]
        clk = list_str[3]
        accession = list_str[4]
        extention = list_str[5]
        return ip, date, time, clk, accession, extention

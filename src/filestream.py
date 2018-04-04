# Andriy Zatserklyaniy <zatserkl@gmail.com> Apr 4, 2018


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

        # From the description:
        #
        # "Your program should only use this header to determine the order
        # in which the fields will appear in the rest of the other lines
        # in the same file."
        #
        # Find indices of the data fields.

        name_index = {}
        for iname, name in enumerate(names):
            name_index[name] = iname
        print(name_index)
        try:
            self.ip = name_index["ip"]
            self.date = name_index["date"]
            self.time = name_index["time"]
            self.cik = name_index["cik"]
            self.accession = name_index["accession"]
            self.extention = name_index["extention"]
        except KeyError as e:
            print("No such key in the header:", e)
            exit()

    def next_fields(self):
        list_str = list(next(self.gen_stream).split(','))
        # print("list_str", list_str)
        ip = list_str[self.ip]
        date = list_str[self.date]
        time = list_str[self.time]
        cik = list_str[self.cik]
        accession = list_str[self.accession]
        extention = list_str[self.extention]
        return ip, date, time, cik, accession, extention

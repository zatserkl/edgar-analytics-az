# Table of Contents
1. [Programming remarks](README.md#Programming-remarks)

11. [Understanding the challenge](README.md#understanding-the-challenge)
12. [Introduction](README.md#introduction)
13. [Challenge summary](README.md#challenge-summary)
14. [Details of challenge](README.md#details-of-challenge)
15. [Implementation details](README.md#implementation-details)
16. [Input files](README.md#input-files)
17. [Output file](README.md#output-file)
18. [Example](README.md#example)
19. [Writing clean, scalable and well-tested code](README.md#writing-clean-scalable-and-well-tested-code)
20. [Repo directory structure](README.md#repo-directory-structure)
21. [Testing your directory structure and output format](README.md#testing-your-directory-structure-and-output-format)
22. [Instructions to submit your solution](README.md#instructions-to-submit-your-solution)
23. [FAQ](README.md#faq)

# Introduction

The goal of this challenge is to collect analytics of visiting of the Securities and Exchange Commission's Electronic Data Gathering, Analysis and Retrieval (EDGAR) system: get the number of requests per session as well as start time, end time, and duration of the session for each visitor IP. The detailed description of the code challenge can be found at (https://github.com/InsightDataScience/edgar-analytics).

# Environment and Dependencies

* Python 3.6.3

* Imported standard modules

import datetime

from collections import defaultdict, OrderedDict

import sys

import math

# Algorithm and code structure

The code uses two cross-linked dictionary:

timeDict {time slot to write the output file: list of IPs}

userDict {IP: User}

The class User includes main attributes:

session start time

session write time

To process current request I calculate time slot to write for the request, fill userDict and register the IP in the timeDict.

The Python's dictionaries provides about O(1) time complexity.

The code clears entries after streaming the visitor info into the output file, providing very low value of memory usage.

# Programming remarks

The code is written in Python 3.6. The code uses feature of dictionary in the Python 3 to keep the input order of the elements.

The dictionary userDict is of type of OrderedDict to dump the value to the output file after the end of file was detected in the input order.

File stream: I avoid reading the whole file into memory and return generators for each line.
To lower the memory usage (important for the possible large input files), the code does not read the whole file into memory. The class hierarchy FileStream and DataStream provide generators for the input fields of interest.

Field indices: I select the field of interest following the order in the header of the csv-file.

Note that in fact to provide the required result we don't need the requested document attributes at all, so the documents attributes are omitted from the processing.

# Memory usage

The dictionary entries in userDict and timeDict are removed after streaming into the output file.

That measure together with usage of input data provide that the memory usage stays the same during the execution of the code, independent on the input file size; it is about 10.2 MB.

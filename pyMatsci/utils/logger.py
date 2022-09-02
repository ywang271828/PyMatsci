from sys import stderr
from datetime import datetime
class Logger:
    ERROR=0
    QUIET=0
    BASIC=1
    WARNING=2
    DETAIL=3
    DEBUG=4

    io_level = 1

    @classmethod
    def set_io_level(cls, lev):
        cls.io_level = lev

    @classmethod
    def basic(cls, message):
        if cls.io_level >= cls.BASIC:
            print("{:s}: {:s}".format(str(datetime.now()), message))

    @classmethod
    def warning(cls, message):
        if cls.io_level >= cls.WARNING:
            print("{:s}: Warning! {:s}".format(str(datetime.now()), message))

    @classmethod
    def error(cls, message):
        print("{:s}: Error! {:s}".format(str(datetime.now()), message))

    @classmethod
    def detail(cls, message):
        if cls.io_level >= cls.DETAIL:
            print("{:s} DETAIL: {:s}".format(str(datetime.now()), message))

    @classmethod
    def debug(cls, message):
        if cls.io_level >= cls.DEBUG:
            print("{:s} DEBUG: {:s}".format(str(datetime.now()), message))
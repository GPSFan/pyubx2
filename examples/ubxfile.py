"""
ubxfile.py

This example illustrates a simple example implementation of a 
UBXMessage and/or NMEAMessage binary logfile reader using the
UBXReader iterator functions and an external error handler.

Created on 25 Oct 2020

@author: semuadmin
"""

from pyubx2.ubxreader import UBXReader


def errhandler(err):
    """
    Handles errors output by iterator.
    """

    print(f"\nERROR: {err}\n")


def read(stream, errorhandler, protfilter, quitonerror, validate, msgmode):
    """
    Reads and parses UBX message data from stream.
    """

    msgcount = 0

    ubr = UBXReader(
        stream,
        protfilter=protfilter,
        quitonerror=quitonerror,
        validate=validate,
        msgmode=msgmode,
        parsebitfield=True,
        errorhandler=errorhandler,
    )
    for _, parsed_data in ubr:
        print(parsed_data)
        msgcount += 1

    print(f"\n{msgcount} messages read.\n")


if __name__ == "__main__":
    YES = ("Y", "y", "YES,", "yes", "True")
    NO = ("N", "n", "NO,", "no", "False")

    print("Enter fully qualified name of file containing binary UBX data: ", end="")
    filename = input().strip('"')
    print(
        "Which protocol(s) do you want to handle? (1 = NMEA, 2 = UBX, 4 = RTCM3 (3) ",
        end="",
    )
    val = input() or "3"
    iprotfilter = int(val)
    print(
        "How do you want to handle protocol errors? (0 = ignore, 1 = log and continue, 3 = raise and stop) (1) ",
        end="",
    )
    val = input() or "1"
    iquitonerror = int(val)
    print("Do you want to validate the message checksums (y/n)? (y) ", end="")
    val = input() or "y"
    ivalidate = val in YES
    print("Message mode (0=GET (output), 1=SET (input), 2=POLL (poll)? (0) ", end="")
    mode = input() or "0"
    imsgmode = int(mode)

    print(f"Opening file {filename}...")
    with open(filename, "rb") as fstream:
        read(fstream, errhandler, iprotfilter, iquitonerror, ivalidate, imsgmode)
    print("Test Complete")

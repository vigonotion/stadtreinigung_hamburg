import argparse

from .StadtreinigungHamburg import StadtreinigungHamburg
from .GarbageCollection import GarbageCollection


def main():
    parser = argparse.ArgumentParser(description='Get garbage collection dates for Stadtreinigung Hamburg.')

    parser.add_argument('street')
    parser.add_argument('number')

    parser.add_argument("--asid", help="use asid instead of street", action="store_true")
    parser.add_argument("--hnid", help="use hnid instead of street number", action="store_true")

    args = parser.parse_args()

    srh = StadtreinigungHamburg()
    collections = srh.get_garbage_collections(args.street, args.number, args.asid, args.hnid)

    if(len(collections) > 0):
        print("Next garbage collections:")
        for c in collections:
            print(c.container + " on " + c.date.strftime("%Y/%m/%d"))
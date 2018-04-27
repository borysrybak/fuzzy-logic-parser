import os
import re
import time
from collections import defaultdict
from difflib import get_close_matches
import json

import yaml

from objectview import ObjectView

THIS_FOLDER = os.getcwd()
STATS_OUTPUT_FORMAT = "{0:10.0f},{1:d},{2:d},{3:d},{4:d},\n"
VERBOSE_OUTPUT_FORMAT = "Date, Sum"


class Receipt(object):
    """ Market receipt to be parsed """

    def __init__(self, config, raw):
        """
        :param config: ObjectView
            Config object 
        :param raw: [] of str
            Lines in file
        """
        
        self.config = config
        self.market = self.date = self.sum = None
        self.lines = raw
        #self.normalize()
        self.parse()

    def normalize(self):
        """
        :return: void
            1) strip empty lines
            2) convert to lowercase
            3) encoding?

        """

        self.lines = [
            line.lower() for line in self.lines if line.strip()
        ]

    def parse(self):
        """
        :return: void
            Parses obj data
        """
        
        self.date = self.parse_date()
        self.sum = self.parse_sum()

    def fuzzy_find(self, keyword, accuracy=0.6):
        """
        :param keyword: str
            The keyword string to look for
        :param accuracy: float
            Required accuracy for a match of a string with the keyword
        :return: str
            Returns the first line in lines that contains a keyword.
            It runs a fuzzy match if 0 < accuracy < 1.0
        """
        result = []
        #if keyword == 'E':
        for line in self.lines:
              words = line.split()
                    # Get the single best match in line
              matches = get_close_matches(keyword, words, 1, accuracy)
              if matches:
                 result = line
        return result

    def parse_date(self):
        """
        :return: date
            Parses data
        """
        #print(self.config.date_format)
        for line in self.lines:
            m = re.match(self.config.date_format, line)
            if m:  # We"re happy with the first match for now
                return m.group(1)

    def parse_sum(self):
        """
        :return: str
            Parses sum data
        """
        
        for sum_key in self.config.sum_keys:
            sum_line = self.fuzzy_find(sum_key) #sum_key.lower())
            if sum_line:
                # Replace all commas with a dot to make
                # finding and parsing the sum easier
                   
                sum_line = sum_line.replace(",", ".")
                sum_words = sum_line.split()
                # Parse the sum
                for words in sum_words:
                    sum_float = re.search(self.config.sum_format, words)
                    if sum_float:
                        return sum_float.group(0)


def read_config(file="config.yml"):
    """
    :param file: str
        Name of file to read
    :return: ObjectView
        Parsed config file
    """

    stream = open(os.path.join(THIS_FOLDER, file), "r")
    docs = yaml.safe_load(stream)
    return ObjectView(docs)


def read_json_from_file(file="json1.json"):
    """
    :param folder: str
        Path to folder to list
    :param include_hidden: bool
        True iff you want also hidden files
    :return: [] of str
        List of full path of files in folder
    """

    stream = open(file, "r")
    json_result = json.load(stream)
    return json_result


def percent(numerator, denominator):
    """
    :param numerator: float
        Numerator of fraction
    :param denominator: float
        Denominator of fraction
    :return: str
        Fraction as percentage
    """

    if denominator == 0:
        out = "0"
    else:
        out = str(int(numerator / float(denominator) * 100))

    return out + "%"


def ocr_receipts(config, receipt_lines):
    """
    :param config: ObjectView
        Parsed config file
    :param receipt_files: [] of str
        List of files to parse
    :return: {}
        Stats about files
    """

    print(VERBOSE_OUTPUT_FORMAT)
    receipt = Receipt(config, receipt_lines)
    print(receipt.date, receipt.sum)

    return

def get_files_in_folder(folder, include_hidden=False):
    """
    :param folder: str
        Path to folder to list
    :param include_hidden: bool
        True iff you want also hidden files
    :return: [] of str
        List of full path of files in folder
    """

    files = []
    for file in os.listdir(folder):
        if file.endswith(".json"):        
            files.append(os.path.join(folder, file) )
    return files


def main():
    """
    :return:
    """

    config = read_config()
    
    files = get_files_in_folder("json_result")
    for file in files:
        print(file + ":")
        result = read_json_from_file(file)
        lines = []
        for line in result['recognitionResult']['lines']:  #OCR version 1
        #for line in result['content']['lines']: # OCR version 2
            lines.append(line['text'])
        ocr_receipts(config, lines)


if __name__ == "__main__":
    main()

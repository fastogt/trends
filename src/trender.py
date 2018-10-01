#!/usr/bin/env python3

import sys
import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import argparse

CSV_HEADER = ['date', 'key', 'clicks', 'impressions', 'ctr', 'position', 'property', 'country']


def trend(data: list):
    """ Determine trend """
    if len(data) < 3:
        return None
    y = np.array(data)
    x = np.array(range(len(data)))
    A = np.vstack([x, np.ones(len(x))]).T
    m, c = np.linalg.lstsq(A, y)[0]
    trend = 'constant'
    if m > 0:
        trend = 'rising'
    if m < 0:
        trend = 'falling'
    mean = np.mean(y)
    return {'trend_rate': m,
            'trend_offset': c,
            'trend': trend,
            'mean': mean}


def read_keys_from_file(page_filters_file):
    keys = []
    with open(page_filters_file, "r") as file_handle:
        for line in file_handle.readlines():
            keys.append(line.strip("\n"))
    return keys


def parse_command_line_options():
    """
    Parses arguments from the command line and returns them in the form of an ArgParser object.
    """
    parser = argparse.ArgumentParser(description="Trending plot.")
    parser.add_argument('csv_file_path', type=str, help='CSV path for trending data.')
    parser.add_argument('--keywords_file', type=str, help='File path of a key for scaning', default="")
    parser.add_argument('--plot_field', type=str, help='Field fo plots',
                        choices=['clicks', 'impressions', 'ctr', 'position'], default='ctr')
    return parser.parse_args()


def main():
    """
        Fetch and parse all command line options.
        """
    args = parse_command_line_options()
    if args.keywords_file:
        try:
            keys = read_keys_from_file(args.keywords_file)
        except IOError as err:
            logging.error("%s is not a valid file path", args.page_filters_file)
            sys.exit(err)
    else:
        keys = []

    csv = pd.read_csv(args.csv_file_path)
    data = csv[CSV_HEADER]

    data_rows_count_start = len(data)
    if not keys:
        all_keys = data['key'].tolist()
        counted = defaultdict(int)
        max_count = 0
        for i, v in enumerate(all_keys):
            counted[v] += 1
            if counted[v] > max_count:
                max_count = counted[v]

        keys = []
        ls2_sum = 0
        for key, value in counted.items():
            if value > max_count / 2:
                keys.append(key)
                ls2_sum += value

        data = data.loc[data['key'].isin(keys)]

    data = data.loc[data['key'].isin(keys)]

    x = data['date']
    y = data[args.plot_field]
    data_rows_count_filtered = len(data)
    plt.figure('{0} ({1}) {2}/{3}'.format(args.csv_file_path, args.plot_field, data_rows_count_filtered,
                                          data_rows_count_start))
    plt.scatter(x, y)

    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plt.plot(x, p(x), "r--")

    plt.show()


if __name__ == '__main__':
    main()

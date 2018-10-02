#!/usr/bin/env python3

import sys
import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from trend_info import TrendInfo
from collections import defaultdict

import argparse

CSV_HEADER = ['date', 'key', 'clicks', 'impressions', 'ctr', 'position', 'property', 'country']
PRECISION = 3


def round_value(value):
    return round(value, PRECISION)


def make_trend_info(key: str, x: np.array, y: np.array, valid_dots_percent):
    """ Determine trend """
    data_size = len(x)
    if data_size < 3:
        return None

    ones = np.ones(data_size)
    A = np.vstack([x, ones]).T
    m, c = np.linalg.lstsq(A, y, rcond=None)[0]
    mean = np.mean(y)
    return TrendInfo(key, m, round_value(c), round_value(mean), round_value(y.max()), round_value(y.min()),
                     round_value(valid_dots_percent))


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


def filter_keys(keys):
    counted = defaultdict(int)
    max_count = 0
    for i, v in enumerate(keys):
        counted[v] += 1
        if counted[v] > max_count:
            max_count = counted[v]

    filtered_keys = []
    for key, value in counted.items():
        if value >= max_count / 2:
            filtered_keys.append(key)
    return filtered_keys


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
    all_keys = data['key'].tolist()
    if not keys:
        keys = filter_keys(all_keys)

    data = data.loc[data['key'].isin(keys)]

    grouped_data_keys = data.groupby(data['key'].tolist(), as_index=False)
    dates = data['date'].unique()

    trends = []
    for key, row in grouped_data_keys:
        values = np.zeros(len(dates))

        sl_dates = row['date'].tolist()
        sl_values = row[args.plot_field].tolist()
        valid_dots_percent = len(sl_dates) / len(dates)
        for i, date in enumerate(sl_dates):
            val = sl_values[i]
            ind = np.where(dates == date)
            values[ind] = val

        tr = make_trend_info(key, dates, values, valid_dots_percent)
        if tr:
            trends.append(tr)

    trends.sort()
    for trend in trends:
        print(trend)

    x = data['date']
    y = data[args.plot_field]
    data_rows_count_filtered = len(data)
    # title
    plt.title('{0} {1}/{2}'.format(args.csv_file_path, data_rows_count_filtered, data_rows_count_start))
    plt.xlabel('Date')
    plt.ylabel(args.plot_field)

    plt.scatter(x, y)

    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plt.plot(x, p(x), "r--")

    plt.show()


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
import numpy as np

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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


def parse_command_line_options():
    """
    Parses arguments from the command line and returns them in the form of an ArgParser object.
    """
    parser = argparse.ArgumentParser(description="Trending plot.")
    parser.add_argument('csv_file_path', type=str, help='CSV path for trending data.')
    return parser.parse_args()


def main():
    """
        Fetch and parse all command line options.
        """
    args = parse_command_line_options()

    csv = pd.read_csv(args.csv_file_path)
    # 2018-01-01,some,18.0,50.0,0.36,2.2,gsc_property,worldwide
    data = csv[CSV_HEADER]
    x = data['date']
    y = data['ctr']
    plt.scatter(x, y)

    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plt.plot(x, p(x), "r--")

    plt.show()


if __name__ == '__main__':
    main()

#!/usr/bin/env python

# Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.

import argparse
from typing import List, Tuple

from sockeye.utils import smart_open

from .utils import read_benchmark_handler_output


def compute_percentiles(lengths: List[int], length_percentile: int,
                        times: List[float], time_percentile: int) -> Tuple[int, float]:
    # Length percentile
    lp_i = min(int((length_percentile / 100) * len(lengths)), len(lengths) - 1)
    lp = sorted(lengths)[lp_i]

    # Time percentile (of length percentile)
    percentile_points = sorted(zip(lengths, times))[:lp_i + 1]
    percentile_times = [point[1] for point in percentile_points]
    tp_i = min(int((time_percentile / 100) * len(percentile_times)), len(percentile_times) - 1)
    tp = sorted(percentile_times)[tp_i]
    return lp, tp


def percentiles_from_benchmark_output(input_stream, length_percentile: int, time_percentile: int) -> Tuple[int, float]:
    input_lengths = []
    translation_times = []
    for entry in read_benchmark_handler_output(input_stream):
        input_lengths.append(int(entry['input_tokens']))
        translation_times.append(float(entry['translation_time']))
    return compute_percentiles(input_lengths, length_percentile, translation_times, time_percentile)


def main():
    parser = argparse.ArgumentParser(description='Report length and time percentiles for benchmark output')
    parser.add_argument(
        '--input',
        '-i',
        required=True,
        help=
        'Input file (result of sockeye.translate with \'benchmark\' output)')
    parser.add_argument(
        '--length-percentile',
        '-lp',
        type=int,
        default=99,
        help='Percentile to report for input length. Default: %(default)s')
    parser.add_argument(
        '--time-percentile',
        '-tp',
        type=int,
        default=99,
        help='Percentile to report for translation time. Default: %(default)s')
    args = parser.parse_args()

    with smart_open(args.input) as inp:
        lp, tp = percentiles_from_benchmark_output(inp, args.length_percentile, args.time_percentile)
    print('P{}\t{:d}'.format(args.length_percentile, lp))
    print('P{}/{}\t{:0.3f}'.format(args.time_percentile, args.length_percentile, tp))


if __name__ == '__main__':
    main()

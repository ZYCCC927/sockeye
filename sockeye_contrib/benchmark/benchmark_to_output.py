#!/usr/bin/env python

# Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.

import sys
from typing import Iterator

from .utils import read_benchmark_handler_output


def get_output_from_benchmark_output(input_stream) -> Iterator[str]:
    for entry in read_benchmark_handler_output(input_stream):
        yield entry['output']


def main():
    for output in get_output_from_benchmark_output(sys.stdin):
        print(output)


if __name__ == '__main__':
    main()

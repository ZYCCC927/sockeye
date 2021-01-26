# Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.

from typing import Dict, Iterator


def read_benchmark_handler_output(stream: str) -> Iterator[Dict[str, str]]:
    for line in stream:
        fields = line.strip().split('\t')
        entry = dict(field.split('=', 1) for field in fields)
        yield entry

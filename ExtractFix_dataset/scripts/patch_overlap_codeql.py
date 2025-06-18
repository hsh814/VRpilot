#!/usr/bin/env/python3

import csv
import sys
from pathlib import Path
from collections import defaultdict

# Check for overlap between two intervals X: [a,b) and Y: [c,d)
def check_overlap(X, Y):
    if X[0] <= Y[0] and Y[0] < X[1]:
        return True
    elif X[0] < Y[1] and Y[1] <= X[1]:
        return True
    elif X[0] <= Y[0] and Y[1] <= X[1]:
        return True
    elif Y[0] <= X[0] and X[1] <= Y[1]:
        return True
    else:
        return False

def test_check_overlap():
    # Overlap at the start of X
    assert check_overlap([1,3], [0,2]) == True
    # Overlap at the end of X
    assert check_overlap([1,3], [2,3]) == True
    # Overlap inside X
    assert check_overlap([1,4], [2,3]) == True
    # Overlap at the start of Y
    assert check_overlap([0,2], [1,3]) == True
    # Overlap at the end of Y
    assert check_overlap([2,3], [1,3]) == True
    # Overlap inside Y
    assert check_overlap([2,3], [1,4]) == True
    # No overlap
    assert check_overlap([1,3], [3,4]) == False
    assert check_overlap([1,3], [5,6]) == False
    assert check_overlap([1,3], [0,1]) == False

def print_dict(d):
    for k, v in d.items():
        print(f"{k:>10}: {v}")

patch_ranges = defaultdict(list)

current = None
for line in open(sys.argv[1]):
    line = line.rstrip()
    if line.startswith('---'):
        _, path = line.split(' ', 1)
        # strip first path component
        path = Path(path).parts[1:]
        path = '/'.join(path)
        current = str(path)
    elif line.startswith('@@'):
        parts = line.split(' ')
        start, size = parts[1].split(',')
        start = -int(start)
        size = int(size)
        patch_ranges[current].append((start,start+size))
patch_ranges = dict(patch_ranges)

header = ["name", "desc", "sev", "message", "path",
        "start_line", "start_col", "end_line", "end_col"]
for row in csv.DictReader(open(sys.argv[2]),fieldnames=header):
    path = str(Path(row["path"][1:]))

    if path not in patch_ranges:
        continue
    print(f"Found matching filename for {path}")
    for patch_range in patch_ranges[path]:
        if check_overlap(patch_range, (int(row["start_line"]), int(row["end_line"])+1)):
            print_dict(row)
            break

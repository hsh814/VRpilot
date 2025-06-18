#!/usr/bin/env python

import os
import re
import sys
import unidiff
from pprint import pprint

def parse_asan_report(report_filename, strip_prefix):
    asan_report = open(report_filename, encoding='latin1')
    # Skip forward until we find the line that starts the report.
    while True:
        line = asan_report.readline()
        if not line:
            print("Could not find report in asan report")
            sys.exit(1)
        if line.startswith('================================================================='):
            break
    report_marker = re.compile(r'^==(?P<num>\d+)==ERROR: AddressSanitizer:')
    stack_trace_nosym_re = re.compile(r'^ +#(?P<num>\d+) (?P<addr>0x[0-9a-fA-F]+) in (?P<func>\w+) \((?P<file>[^+]+)\+(?P<offset>0x[0-9a-fA-F]+)\)')
    stack_trace_sym_re = re.compile(r'^ +#(?P<num>\d+) (?P<addr>0x[0-9a-fA-F]+) in (?P<func>\w+) (?P<file>[^:]+):(?P<line>\d+)')
    report = {}
    while True:
        line = asan_report.readline()
        if not line: break
        
        match = report_marker.match(line)
        if match:
            break

    report['num'] = match.group('num')
    report['topline'] = line.strip()
    report['description'] = asan_report.readline().strip()
    stack_trace = []
    while True:
        line = asan_report.readline()
        if not line: break
        match = stack_trace_nosym_re.match(line)
        if match:
            d = match.groupdict()
            d['syms'] = False
            d['file'] = d['file'].replace(strip_prefix, '')
            stack_trace.append(d)
        else:
            match = stack_trace_sym_re.match(line)
            if match:
                d = match.groupdict()
                d['syms'] = True
                d['line'] = int(d['line'])
                d['file'] = d['file'].replace(strip_prefix, '')
                stack_trace.append(d)
            else:
                break
    report['stack_trace'] = stack_trace

    # For stack buffer overflow reports, we may have frame info.
    # It looks like:
    #   This frame has 2 object(s):
    #     [32, 200) 'jerr'
    #     [256, 888) 'cinfo' <== Memory access at offset 888 overflows this variable
    frames = []
    frame_re = re.compile(r'^\s+\[(?P<start>\d+), (?P<end>\d+)\) \'(?P<name>\w+)\'')
    pos = asan_report.tell() # So we can rewind if there's no frame info.
    while True:
        line = asan_report.readline()
        if not line: break
        if not line.startswith("  This frame has"):
            continue
        # We've found the frame info.
        while True:
            line = asan_report.readline()
            if not line: break
            match = frame_re.match(line)
            if not match:
                break
            d = match.groupdict()
            if '<==' in line:
                d['overflow'] = True
            else:
                d['overflow'] = False
            frames.append(d)
        break
    if frames:
        report['frames'] = frames

    # Rewind
    asan_report.seek(pos)

    # For heap buffer overflow reports, we may have a stack trace for the allocation site.
    # It looks like:
    # allocated by thread T0 here:
    #    #0 0x7f183c5a4602 in malloc (/usr/lib/x86_64-linux-gnu/libasan.so.2+0x98602)
    #    #1 0x7f183c2a5d78 in alloc_large /dataset/repos/libjpeg-turbo/jmemmgr.c:391
    #    #2 0x7f183c2a5d78 in alloc_sarray /dataset/repos/libjpeg-turbo/jmemmgr.c:475
    alloc_info = {}
    while True:
        line = asan_report.readline()
        if not line: break
        if not line.startswith("allocated by thread "):
            continue
        alloc_info['thread'] = line.strip().split()[-1]
        # We've found the allocation site.
        alloc_stack = []
        while True:
            line = asan_report.readline()
            if not line: break
            match = stack_trace_nosym_re.match(line)
            if match:
                d = match.groupdict()
                d['syms'] = False
                d['file'] = d['file'].replace(strip_prefix, '')
                alloc_stack.append(d)
            else:
                match = stack_trace_sym_re.match(line)
                if match:
                    d = match.groupdict()
                    d['syms'] = True
                    d['line'] = int(d['line'])
                    d['file'] = d['file'].replace(strip_prefix, '')
                    alloc_stack.append(d)
                else:
                    break
        alloc_info['stack_trace'] = alloc_stack
        report['alloc_info'] = alloc_info
        break

    # Rewind
    asan_report.seek(pos)

    # Find summary line.
    while True:
        line = asan_report.readline()
        if not line: break
        if line.startswith('SUMMARY:'):
            break
    report['summary'] = line.strip()
    report['sanitizer'] = 'ASAN'

    return [report]

# Parse UBSAN report. It looks like:
# /dataset/repos/libtiff/libtiff/tif_ojpeg.c:816:8: runtime error: division by zero
def parse_ubsan_report(report_filename, strip_prefix):
    reports = []
    ubsan_re = re.compile(r'^(?P<file>[^:]+):(?P<line>\d+):(?P<col>\d+): runtime error: (?P<description>.*)')
    ubsan_report = open(report_filename, encoding='latin1')
    for line in ubsan_report:
        match = ubsan_re.match(line)
        if match:
            d = match.groupdict()
            d['sanitizer'] = 'UBSAN'
            d['file'] = d['file'].replace(strip_prefix, '')
            d['line'] = int(d['line'])
            d['col'] = int(d['col'])
            d['summary'] = f'SUMMARY: runtime error: {d["description"]} in {d["file"]}:{d["line"]}'
            # Fake a stack trace for compatibility with asan reports.
            d['stack_trace'] = [{'file': d['file'], 'line': d['line'], 'syms': True}]
            reports.append(d)
    return reports

def is_asan(fname):
    return b'==ERROR: AddressSanitizer:' in open(fname,'rb').read()

def is_ubsan(fname):
    return b'runtime error:' in open(fname,'rb').read()

patchset = unidiff.PatchSet(open(sys.argv[1], encoding='latin1').read())
if is_asan(sys.argv[2]):
    reports = parse_asan_report(sys.argv[2], sys.argv[3])
elif is_ubsan(sys.argv[2]):
    reports = parse_ubsan_report(sys.argv[2], sys.argv[3])
else:
    raise ValueError("Not an ASAN or UBSAN report!")

# How large are the source changes in the patch?
source_patches = [p for p in patchset if p.source_file.endswith('.c') or
                                         p.source_file.endswith('.h') or
                                         p.source_file.endswith('.cpp')]
for report in reports:
    file_matches = set()
    hunk_matches = 0
    for p in source_patches:
        line_starts = []
        line_ends = []
        added = 0
        removed = 0
        # Strip first component of patch file path.
        source_file = '/'.join(p.source_file.split('/')[1:])
        
        ranges = []
        for hunk in p:
            added += hunk.added
            removed += hunk.removed
            line_starts.append(hunk.source_start)
            line_ends.append(hunk.source_start + hunk.added - 1)
            if hunk.added > 0:
                added_lines = [line.source_line_no for line in hunk if line.is_added]
                removed_lines = [line.source_line_no for line in hunk if line.is_removed]
                ranges.append((min(added_lines), max(added_lines)))
        patch_range = (min(line_starts), max(line_ends))
        
        matched = False
        # Check if two ranges a and b overlap
        def overlaps(a, b):
            return a[0] <= b[0] <= a[1] or b[0] <= a[0] <= b[1]
            
        # Check if the ASAN report is in the range of the patch. For each
        # stack frame entry, we check if the line number is in the range of
        # the patch, with up to 10 lines before the ASAN line.
        for r in report['stack_trace']:
            if not r['syms']: continue
            # HACK: UBSAN reports sometimes don't have paths, only filenames.
            if report['sanitizer'] == 'UBSAN' and '/' not in r['file']:
                source_file = os.path.basename(source_file)
            #print(f"Comparing {source_file} {patch_range} to {r['file']}:({r['line']-10},{r['line']})")
            if r['file'] == source_file:
                file_matches.add(source_file)
                matched = True
                if overlaps(patch_range, (r['line']-10, r['line'])):            
                    hunk_matches += 1
                    #print(f'  {r["file"]}:{r["line"]} in {r["func"]}')          
        if 'alloc_info' in report:
            for r in report['alloc_info']['stack_trace']:
                if not r['syms']: continue
                #print(f"Comparing {source_file} {patch_range} to {r['file']}:{r['line']}")
                if r['file'] == source_file:
                    file_matches.add(source_file)
                    matched = True
                    if overlaps(patch_range, (r['line']-10, r['line'])): 
                        hunk_matches += 1
                        #print(f'  {r["file"]}:{r["line"]} in {r["func"]}')                  

        match_marker = ' * ' if matched else '   '
        print(f'{match_marker} {source_file}: {added} lines added, {removed} lines removed, spans {patch_range[1]-patch_range[0]+1} lines (' +
              ', '.join(f'{st}-{ed}' for st,ed in ranges) + ')')
    total_hunks = sum(len(p) for p in source_patches)
    print(report['summary'])
    print(f'{report["sanitizer"]} report: {len(file_matches)}/{len(source_patches)} source files match, {hunk_matches}/{total_hunks} hunks match')
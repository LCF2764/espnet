#!/usr/bin/env python
import argparse
import io
import sys

PY2 = sys.version_info[0] == 2

if PY2:
    from itertools import izip_longest as zip_longest
else:
    from itertools import zip_longest


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Gather wav.scp for each channels into a wav.scp')
    parser.add_argument('scp', type=str, nargs='+', help='Give wav.scp')
    parser.add_argument('out', nargs='?', type=argparse.FileType('w'),
                        default=sys.stdout,
                        help='The output filename. '
                             'If omitted, then output to sys.stdout')
    args = parser.parse_args()

    fscps = [io.open(scp, 'r', encoding='utf-8') for scp in args.scp]

    for linenum, lines in enumerate(zip_longest(*fscps)):
        keys = []
        wavs = []

        for line, scp in zip(lines, args.scp):
            if line is None:
                raise RuntimeError('Numbers of line mismatch')

            sps = line.split(' ', 1)
            if len(sps) != 2:
                raise RuntimeError(
                    'Invalid line is found: {}, line {}: "{}" '
                    .format(scp, linenum, line))
            key, wav = sps
            keys.append(key)
            wavs.append(wav.strip())

        if not all(k == keys[0] for k in keys):
            raise RuntimeError('The ids mismatch: {}'.format(keys))

        # gather-wav.py can be found in "utils"
        args.out.write('{} gather-wav.py {} |\n'.format(
            keys[0], ' '.join('"{}"'.format(w) for w in wavs)))


if __name__ == '__main__':
    main()

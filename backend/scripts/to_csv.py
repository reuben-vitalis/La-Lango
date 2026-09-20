"""Convert a line-aligned parallel corpus (.src/.tgt) into the team CSV format.

Usage:
    python backend/scripts/to_csv.py \
        --src data/raw/english-kiswahili/all.src \
        --tgt data/raw/english-kiswahili/all.tgt \
        --output languages/english-kiswahili/english-kiswahili.csv
"""

import argparse
import csv
import sys

DEFAULT_HEADER = ("English sentence", "Swahili Translation")


def convert(src_path, tgt_path, out_path, header=DEFAULT_HEADER):
    with open(src_path, encoding="utf-8") as f:
        src_lines = f.read().splitlines()
    with open(tgt_path, encoding="utf-8") as f:
        tgt_lines = f.read().splitlines()

    if len(src_lines) != len(tgt_lines):
        sys.exit(
            f"Error: line count mismatch - {src_path} has {len(src_lines)} lines, "
            f"{tgt_path} has {len(tgt_lines)}"
        )

    written = skipped = 0
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(header)
        for src, tgt in zip(src_lines, tgt_lines):
            src, tgt = src.strip(), tgt.strip()
            if not src or not tgt:
                skipped += 1
                continue
            writer.writerow([src, tgt])
            written += 1

    print(f"Wrote {written} pairs to {out_path} (skipped {skipped} blank)")
    return written


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--src", required=True)
    parser.add_argument("--tgt", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    convert(args.src, args.tgt, args.output)


if __name__ == "__main__":
    main()

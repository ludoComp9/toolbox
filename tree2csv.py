#!/usr/bin/env python3
#
# Convert content of a file given in input generated from the Linux `tree` command
#
# 2025/10/06    0.01    Initial version
import re
import csv
import os
import sys
import argparse

### Global constant
__version__ = '0.01'
# Regex patterns for cleaning and parsing
ANSI_RE = re.compile(
	r'(\x1B\[[0-?]*[ -/]*[@-~])|'      # real ESC[
	r'(\\x1B\[[0-?]*[ -/]*[@-~])|'     # literal "\x1B["
	r'(\\033\[[0-9;]*m)|'              # literal "\033["
	r'(\\e\[[0-9;]*m)|'                # literal "\e["
	r'(ESC\[[0-9;]*m)',                # literal "ESC["
	flags=re.IGNORECASE
)
TREE_CHARS_RE = re.compile(r'^[\s│├└┌┐┤┴┬┼─>»·•-]+')
NAME_START_RE = re.compile(r'[A-Za-z0-9_.@\-]')
SUMMARY_RE = re.compile(r'^\s*\d+\s+(directories?|files?)', re.I)


def clean_raw(line):
	"""Remove ANSI escape codes and trailing newlines."""
	return ANSI_RE.sub('', line.rstrip('\n'))

def find_name_index(s):
	"""Find where the name starts in a 'tree' line (after indentation)."""
	m = NAME_START_RE.search(s)
	if m:
		return m.start()
	stripped = re.sub(r'^[\s│├└┌┐┤┴┬┼─>»·•-]+', '', s)
	if not stripped:
		return None
	ch = stripped[0]
	return s.find(ch)

def parse_items(path, debug=False, show_progress=False):
	"""Parse the tree-like file and return a list of (indent, name)."""
	items = []
	with open(path, 'r', encoding='utf-8', errors='replace') as f:
		raw_lines = f.readlines()

	total = len(raw_lines)
	for idx, raw in enumerate(raw_lines):
		if show_progress and idx % 1000 == 0:
			print(f"\r⏳ Reading lines: {idx + 1}/{total}", end='', flush=True)

		if not raw.strip():
			continue
		if SUMMARY_RE.match(raw):
			continue
		s = clean_raw(raw)
		if s.strip() == '.':
			items.append({'idx': idx, 'raw': raw.rstrip('\n'), 'name': '.', 'indent': -1})
			continue
		name_idx = find_name_index(s)
		if name_idx is None:
			continue
		name = s[name_idx:].strip()
		name = re.sub(r'^[\u2500-\u257F\s\-›»·•>]+', '', name).strip()
		if not name:
			continue
		indent = name_idx
		items.append({'idx': idx, 'raw': raw.rstrip('\n'), 'name': name, 'indent': indent})
		if debug and len(items) <= 50:
			print(f"DBG item[{len(items)-1}] idx={idx} indent={indent} name='{name}'")

	if show_progress:
		print(f"\r✅ Read complete ({len(items)} items).{' ' * 20}")
	return items

def build_rows(items, debug=False, show_progress=False):
	"""Convert parsed lines into (directory, file) CSV rows."""
	if not items:
		return []

	stack = [(-1, '.')]
	rows = []
	start = 0
	if items[0]['name'] == '.':
		start = 1

	total = len(items)
	for i in range(start, total):
		if show_progress and i % 1000 == 0:
			print(f"\r⚙️  Building CSV: {i + 1}/{total}", end='', flush=True)

		cur = items[i]
		indent = cur['indent']
		name = cur['name']

		next_indent = items[i + 1]['indent'] if i + 1 < total else -1
		is_dir = next_indent > indent

		while stack and stack[-1][0] >= indent:
			stack.pop()

		parent = stack[-1][1] if stack else '.'
		fullpath = f'{parent}/{name}' if parent != '.' else f'./{name}'

		if is_dir:
			rows.append((fullpath, ''))
			stack.append((indent, fullpath))
		else:
			if parent != '.' and not any(r == (parent, '') for r in rows):
				rows.append((parent, ''))
			rows.append((parent if parent != '.' else '.', name))

	# Ensure top-level directory is included
	data_items = [it for it in items if it['name'] != '.']
	if data_items:
		min_indent = min(it['indent'] for it in data_items)
		top_names = [it['name'] for it in data_items if it['indent'] == min_indent]
		for tn in reversed(top_names):
			d = f'./{tn}'
			if not any(r == (d, '') for r in rows):
				rows.insert(0, (d, ''))

	seen = set()
	final = []
	for d, f in rows:
		key = (d, f)
		if key not in seen:
			seen.add(key)
			final.append((d, f))

	if show_progress:
		print(f"\r✅ CSV build complete ({len(final)} rows).{' ' * 20}")
	return final

def write_csv(rows, outpath):
	"""Write directory/file pairs to a CSV file."""
	with open(outpath, 'w', newline='', encoding='utf-8') as f:
		writer = csv.writer(f, delimiter=';')
		writer.writerow(['directory', 'file'])
		writer.writerows(rows)

def main():
	parser = argparse.ArgumentParser(description=(
		f"--== Tree to CSV v{__version__} ==--\n"
		f"--== Convert a 'tree' command text output into a CSV file ==--"
		),
		formatter_class=argparse.RawTextHelpFormatter
	)
	parser.add_argument('-V', '--version', action='version', version='{} v{}'.format(os.path.basename(__file__), __version__))
	parser.add_argument('input', help="Input text file (from 'tree' command).")
	parser.add_argument('output', help="Output CSV file path.")
	parser.add_argument('--debug', action='store_true', help="Enable debug output for inspection.")
	parser.add_argument('--show-progress', action='store_true', help="Show progress during processing.")
	args = parser.parse_args()

	if not os.path.exists(args.input):
		print(f"❌ Error: input file not found: {args.input}", file=sys.stderr)
		sys.exit(2)

	items = parse_items(args.input, debug=args.debug, show_progress=args.show_progress)
	rows = build_rows(items, debug=args.debug, show_progress=args.show_progress)
	write_csv(rows, args.output)
	print(f"\n✅ Done! CSV written to: {os.path.abspath(args.output)} ({len(rows)} rows)")

### Main ###
if __name__ == '__main__':
	main()
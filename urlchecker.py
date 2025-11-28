#!/usr/bin/env python3

# -*- coding: utf-8 -*-

# URL Checker
# 28/11/2025	0.01	Initial script

import argparse
import requests
import csv
import json
import time
from datetime import datetime
from bs4 import BeautifulSoup
from bs4 import XMLParsedAsHTMLWarning
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import warnings
# Ignore warning message in case of XML content
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

__version__ = '0.01'

def get_options():
	""" Argument control """
	parser = argparse.ArgumentParser(description=f"--== URL Checker v{__version__} ==--")
	parser.add_argument('-V', '--version', action='version', version='{} v{}'.format(os.path.basename(__file__), __version__))
	parser.add_argument('-d', '--debug', dest='debug', help='enable debug mode', action="store_true")
	parser.add_argument('--url', dest='url', help='unique URL to check', metavar='<ip address>')
	parser.add_argument('-i', '--input', dest='input_file', help='Filename contains a list of URLs to check', metavar='<filename>', action='store')
	parser.add_argument('-f', '--format', dest='output_format', help='specify output format (default: csv)', choices=['json', 'csv'], default='csv', type=str.lower)
	parser.add_argument('-o', '--output', dest='output_file', help='specify the output filename', metavar='<filename>', action='store')
	parser.add_argument('-t', '--threads', dest='threads', help='specify threads number', metavar='<digit>', type=int, action='store')
	parser.add_argument('--proxy', dest='proxy', help='specify HTTP proxy with port. Example: "localhost:3128"', metavar='<proxy_host>:<proxy_port>', type=parse_proxy, action='store')
	parser.add_argument('--noproxy', dest='noproxy', help='Ignore system proxy (if defined)', action="store_true")
	return parser.parse_args()

def parse_proxy(value):
	try:
		host, port = value.split(":")
		return host, int(port)
	except ValueError:
		raise argparse.ArgumentTypeError("Proxy must be defined as <host>:<port>. (Example: localhost:3128)")

def format_duration(seconds):
	""" Format time """
	if seconds < 1:
		return f"{round(seconds * 1000, 2)} ms"
	return f"{round(seconds, 3)} s"

def get_title(html):
	""" Get HTML title page """
	try:
		soup = BeautifulSoup(html, "html.parser")
		title = soup.title.string if soup.title else ""
		return title.strip() if title else ""
	except Exception:
		return ""

def check_url(url):
	""" Check URL given in input """
	start = time.time()

	try:
		response = requests.get(url, timeout=8)
		status = response.status_code
		title = get_title(response.text)
		error = ""
	except requests.exceptions.RequestException as e:
		status = None
		title = ""
		error = str(e)

	duration = time.time() - start

	return {
		"url": url,
		"status_code": status,
		"title": title,
		"duration": format_duration(duration),
		"error": error,
		"control_date": datetime.fromtimestamp(start).strftime("%Y-%m-%d %H:%M:%S")
	}

def output_json(data, output_file=None):
	if output_file:
		with open(output_file, 'w', encoding='utf-8') as f:
			json.dump(data, f, indent=2)
	else:
		json.dump(data, sys.stdout, indent=2)
		print()  # newline for clean terminal output

def output_csv(data, output_file=None):
	if not data:
		logger.error("No data to write to CSV.")
		return False
	with open(output_file, 'w', newline='', encoding='utf-8') as f:
		writer = csv.DictWriter(f, fieldnames=data[0].keys())
		writer.writeheader()
		writer.writerows(data)

def main():
	# Initialization
	args = get_options()
	results = []
	# Configure maximum threads
	max_threads = args.threads if args.threads else os.cpu_count() * 5
	if not args.proxy and not args.noproxy and 'https_proxy' in os.environ:
		# Use default proxy
		logger.debug('Proxy system detected. Script will use it.')
		default_proxy = os.environ['https_proxy'].split('/')[-1].split('@')[-1]
		args.proxy = parse_proxy(default_proxy)
	else:
		# Ignore system proxy
		args.proxy = None
	
	if args.url:
		urls = [args.url]
	elif args.input_file:
		with open(args.input_file, "r", encoding="utf-8") as f:
			urls = [line.strip() for line in f if line.strip()]

	# Check URL(s) in multithreading mode
	with ThreadPoolExecutor(max_workers=max_threads) as executor:
		future_map = {executor.submit(check_url, url): url for url in urls}

		for future in as_completed(future_map):
			result = future.result()
			results.append(result)

	if results:
		if args.output_file:
			eval(f"output_{args.output_format}")(results, args.output_file)
		else:
			# Standard output
			for r in results:
				print(f"Date: {r['control_date']}")
				print(f"URL: {r['url']}")
				print(f"Status code: {r['status_code']}")
				print(f"Title: {r['title']}")
				print(f"Time duration: {r['duration']}")
				if r["error"]:
					print(f"Error : {r['error']}")
				print("-" * 40)

if __name__ == "__main__":
	main()
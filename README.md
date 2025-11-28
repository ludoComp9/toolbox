# Toolbox

Small tools

# Tools presentation

## tree2csv.py

Script to convert of a file given in input generated from the Linux `tree` command

### Help
```plaintext
usage: tree2csv.py [-h] [-V] [--debug] [--show-progress] input output

--== Tree to CSV v0.01 ==--
--== Convert a 'tree' command text output into a CSV file ==--

positional arguments:
  input            Input text file (from 'tree' command).
  output           Output CSV file path.

options:
  -h, --help       show this help message and exit
  -V, --version    show program's version number and exit
  --debug          Enable debug output for inspection.
  --show-progress  Show progress during processing.
```

### Example
```shell
python3 tree2csv.py --show_progress input_file.txt outputfile.csv
```

## urlchecker.py

Script to check status of URL(s) given in input (argument or from CSV file)

### Help
```plaintext
usage: urlchecker.py [-h] [-V] [-d] [--url <ip address>] [-i <filename>] [-f {json,csv}] [-o <filename>] [-t <digit>] [--proxy <proxy_host>:<proxy_port>] [--noproxy]

--== URL Checker v0.01 ==--

options:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  -d, --debug           enable debug mode
  --url <ip address>    unique URL to check
  -i <filename>, --input <filename>
                        Filename contains a list of URLs to check
  -f {json,csv}, --format {json,csv}
                        specify output format (default: csv)
  -o <filename>, --output <filename>
                        specify the output filename
  -t <digit>, --threads <digit>
                        specify threads number
  --proxy <proxy_host>:<proxy_port>
                        specify HTTP proxy with port. Example: "localhost:3128"
  --noproxy             Ignore system proxy (if defined)
````

### Example #1 - Check a specific URL and get results to standard output

```shell
python3 urlchecker.py --url https://www.amazon.com
```
```plaintext
Date: 2025-11-28 22:30:44
URL: https://www.amazon.com
Status code: 503
Title: Sorry! Something went wrong!
Time duration: 186.08 ms
----------------------------------------
```

### Example #2 -  Check URL defined in a CSV file and save results to an output file

With `url.txt` CSV file contains:
```plaintext
https://www.example.com
https://www.amazon.com
https://mapscaping.com/where-am-i/
https://en.wikipedia.org/wiki/Main_Page
https://www.w3schools.com/html/html_examples.asp
https://www.cisa.gov/news.xml
```

- Save to a CSV file
```shell
python3 urlchecker.py -i url.txt --format csv -o results.csv
```

```plaintext
url,status_code,title,duration,error,control_date
https://www.cisa.gov/news.xml,200,CISA News,88.33 ms,,2025-11-28 22:34:48
https://en.wikipedia.org/wiki/Main_Page,403,,107.66 ms,,2025-11-28 22:34:48
https://www.example.com,200,Example Domain,109.18 ms,,2025-11-28 22:34:48
https://www.w3schools.com/html/html_examples.asp,200,HTML Examples,155.08 ms,,2025-11-28 22:34:48
https://www.amazon.com,503,Amazon.com,172.99 ms,,2025-11-28 22:34:48
https://mapscaping.com/where-am-i/,200,"Where Am I - November 28, 2025",520.67 ms,,2025-11-28 22:34:48
```

- Save to a JSON file
```shell
python3 urlchecker.py -i url.txt --format json -o results.json
```

```plaintext
[
  {
    "url": "https://www.cisa.gov/news.xml",
    "status_code": 200,
    "title": "CISA News",
    "duration": "102.29 ms",
    "error": "",
    "control_date": "2025-11-28 22:32:44"
  },
  {
    "url": "https://www.example.com",
    "status_code": 200,
    "title": "Example Domain",
    "duration": "108.4 ms",
    "error": "",
    "control_date": "2025-11-28 22:32:44"
  },
  {
    "url": "https://en.wikipedia.org/wiki/Main_Page",
    "status_code": 403,
    "title": "",
    "duration": "117.91 ms",
    "error": "",
    "control_date": "2025-11-28 22:32:44"
  },
  {
    "url": "https://www.w3schools.com/html/html_examples.asp",
    "status_code": 200,
    "title": "HTML Examples",
    "duration": "173.4 ms",
    "error": "",
    "control_date": "2025-11-28 22:32:44"
  },
  {
    "url": "https://www.amazon.com",
    "status_code": 503,
    "title": "Sorry! Something went wrong!",
    "duration": "193.62 ms",
    "error": "",
    "control_date": "2025-11-28 22:32:44"
  },
  {
    "url": "https://mapscaping.com/where-am-i/",
    "status_code": 200,
    "title": "Where Am I - November 28, 2025",
    "duration": "500.99 ms",
    "error": "",
    "control_date": "2025-11-28 22:32:44"
  }
]
```
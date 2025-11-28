# Toolbox

Small tools

# Tools presentation

## tree2csv.py

Script to convert of a file given in input generated from the Linux `tree` command

** Usage **
```shell
python3 tree2csv.py --show_progress input_file.txt outputfile.csv
```

## urlchecker.py

Script to check status of URL(s) given in input (argument or from CSV file)

** Check a specific URL and get results to standard output **
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

** Check URL defined in a CSV file and save results to an output file **

`url.txt` CSV file contains:
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
output file:
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
output file:
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
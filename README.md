EmailHarvester
====
* A tool to retrieve Domain email addresses from Search Engines

This project was inspired by:
* theHarvester(https://github.com/laramies/theHarvester) from laramies.
* search_email_collector(https://github.com/rapid7/metasploit-framework/blob/master/modules/auxiliary/gather/search_email_collector.rb) from Carlos Perez.


Requirements
=====
* Python 3.x
* termcolor
* colorama
* requests


Features
=====
* Retrieve Domain email addresses from Search Engines (Google, Bing, Yahoo, ASK).
* Export results to txt and xml files.
* Limit search results.
* Define your own User-Agent string.
* Use proxy server.


Download/Installation
====
* git clone https://github.com/maldevel/EmailHarvester
* pip install -r requirements.txt --user


Usage
=====
```
usage: EmailHarvester.py [-h] [-d DOMAIN] [-s FILE] [-e ENGINE] [-l LIMIT]
                         [-u USER-AGENT] [-x PROXY]

 _____                   _  _   _   _                                _
|  ___|                 (_)| | | | | |                              | |
| |__  _ __ ___    __ _  _ | | | |_| |  __ _  _ __ __   __ ___  ___ | |_  ___  _ __
|  __|| '_ ` _ \  / _` || || | |  _  | / _` || '__|\ \ / // _ \/ __|| __|/ _ \| '__|
| |___| | | | | || (_| || || | | | | || (_| || |    \ V /|  __/\__ \| |_|  __/| |
\____/|_| |_| |_| \__,_||_||_| \_| |_/ \__,_||_|     \_/  \___||___/ \__|\___||_|

    A tool to retrieve Domain email addresses from Search Engines | @maldevel
                                Version: 1.1.5

optional arguments:
  -h, --help            show this help message and exit
  -d DOMAIN, --domain DOMAIN
                        Domain to search.
  -s FILE, --save FILE  Save the results into a TXT and XML file.
  -e ENGINE, --engine ENGINE
                        Select search engine(google, bing, yahoo, ask, all).
  -l LIMIT, --limit LIMIT
                        Limit the number of results.
  -u USER-AGENT, --user-agent USER-AGENT
                        Set the User-Agent request header.
  -x PROXY, --proxy PROXY
                        Setup proxy server (example: http://127.0.0.1:8080)
```


Examples
=====
**Search in Google**
* ./EmailHarvester.py -d example.com -e google

**Search in all engines**
* ./EmailHarvester.py -d example.com -e all

**Limit results**
* ./EmailHarvester.py -d example.com -e all -l 200

**Export emails**
* ./EmailHarvester.py -d example.com -e all -l 200 -s emails.txt

**Custom User-Agent string**
* ./EmailHarvester.py -d example.com -e all -u "MyUserAgentString 1.0"

**Proxy Server**
* ./EmailHarvester.py -d example.com -e all -x http://127.0.0.1:8080 

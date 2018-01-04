EmailHarvester
====
* A tool to retrieve Domain email addresses from Search Engines
* Check the [License](https://github.com/maldevel/EmailHarvester/blob/master/LICENSE)

This project was inspired by:
* theHarvester(https://github.com/laramies/theHarvester) from laramies.
* search_email_collector(https://github.com/rapid7/metasploit-framework/blob/master/modules/auxiliary/gather/search_email_collector.rb) from Carlos Perez.


Requirements
=====
* Python 3.x
* termcolor
* colorama
* requests
* validators


Features
=====
* Retrieve Domain email addresses from popular Search engines (Google, Bing, Yahoo, ASK, Baidu, Dogpile, Exalead).
* Export results to txt and xml files.
* Limit search results.
* Define your own User-Agent string.
* Use proxy server.
* Plugins system.
* Search in popular web sites using Search engines (Twitter, LinkedIn, Google+, Github, Instagram, Reddit, Youtube).


Download/Installation
====
* git clone https://github.com/maldevel/EmailHarvester
* pip install -r requirements.txt


Usage
=====
```
usage: EmailHarvester.py [-h] [-d DOMAIN] [-s FILE] [-e ENGINE] [-l LIMIT]
                         [-u USER-AGENT] [-x PROXY] [--noprint]

 _____                   _  _   _   _                                _
|  ___|                 (_)| | | | | |                              | |
| |__  _ __ ___    __ _  _ | | | |_| |  __ _  _ __ __   __ ___  ___ | |_  ___  _ __
|  __|| '_ ` _ \  / _` || || | |  _  | / _` || '__|\ \ / // _ \/ __|| __|/ _ \| '__|
| |___| | | | | || (_| || || | | | | || (_| || |    \ V /|  __/\__ \| |_|  __/| |
\____/|_| |_| |_| \__,_||_||_| \_| |_/ \__,_||_|     \_/  \___||___/ \__|\___||_|

    A tool to retrieve Domain email addresses from Search Engines | @maldevel
                                Version: 1.3.2

optional arguments:
  -h, --help            show this help message and exit
  -d DOMAIN, --domain DOMAIN
                        Domain to search.
  -s FILE, --save FILE  Save the results into a TXT and XML file (both).
  -e ENGINE, --engine ENGINE
                        Select search engine(google, bing, yahoo, ask, all).
  -l LIMIT, --limit LIMIT
                        Limit the number of results.
  -u USER-AGENT, --user-agent USER-AGENT
                        Set the User-Agent request header.
  -x PROXY, --proxy PROXY
                        Setup proxy server (example: http://127.0.0.1:8080)
  --noprint             EmailHarvester will print discovered emails to terminal. 
						It is possible to tell EmailHarvester not to print results to terminal with this option.
  -r EXCLUDED_PLUGINS, --exclude EXCLUDED_PLUGINS
                        Plugins to exclude when you choose 'all' for search engine (eg. '-r google,twitter')
  -p, --list-plugins    List all available plugins.
```


Examples
=====
**Search in Google**
* ./EmailHarvester.py -d example.com -e google

**Search in site using Search engines**
* ./EmailHarvester.py -d example.com -e linkedin
* ./EmailHarvester.py -d example.com -e twitter
* ./EmailHarvester.py -d example.com -e googleplus

**Search in all engines/sites**
* ./EmailHarvester.py -d example.com -e all

**Search in all engines/sites but exclude some**
* ./EmailHarvester.py -d example.com -e all -r twitter,ask

**Limit results**
* ./EmailHarvester.py -d example.com -e all -l 200

**Export emails**
* ./EmailHarvester.py -d example.com -e all -l 200 -s emails.txt

**Custom User-Agent string**
* ./EmailHarvester.py -d example.com -e all -u "MyUserAgentString 1.0"

**Proxy Server**
* ./EmailHarvester.py -d example.com -e all -x http://127.0.0.1:8080 

Docker
=====
Alpine based Dockerfile
```bash
git clone https://github.com/maldevel/EmailHarvester
cd EmailHarvester
docker build -t EmailHarvester .
docker run -it EmailHarvester -d example.com
```
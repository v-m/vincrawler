# VinCrawler

![](https://img.shields.io/github/license/v-m/vincrawler.svg)
![](https://img.shields.io/github/languages/top/v-m/vincrawler.svg)
![](https://img.shields.io/badge/python-3-yellowgreen.svg)

This is a really simple Python web crawler developed for fun.

This simple crawler get all `<a>` URLs found in a site. 
It comply with the site `robots.txt` file (if any) regarding 
the authorized urls as well as the rate limits (based on `Request-rate` and `Crawl-delay`).

If no limits are specified in the `robots.txt` file, then the user can specify these values.
If any, default values are considered (that is, 2 request per 1 second). 

## Installation

Virtual environment strongly encouraged.

```bash
pip install git+https://github.com/v-m/vincrawler.git
```

## Synopsis

```
$ vincrawler --help
usage: vincrawler [-h] [-a USERAGENT] [-R ROBOT] [-t TASKS] [-u UNIT] [-q]
                  [-v]
                  url

positional arguments:
  url                   base url to crawl

optional arguments:
  -h, --help            show this help message and exit
  -a USERAGENT, --useragent USERAGENT
                        user agent to use (default: vincrawler-bot/0.1a1)
  -R ROBOT, --robot ROBOT
                        robots file (default: robots.txt)
  -t TASKS, --tasks TASKS
                        number of tasks per unit of time (default: read from
                        robots.txt or 2)
  -u UNIT, --unit UNIT  the unit of time (default: read from robots.txt or 1
                        sec)
  -q, --ignorequeries   ignore queries part in url
  -v, --verbose         verbosity level
```

## Running

A simple running example is:

```
$ vincrawler http://www.vmusco.com
VinCrawler 0.1a1.
 * User-agent = vincrawler-bot/0.1a1
 * User URL = http://www.vmusco.com
 * Parsed URL = www.vmusco.com
 * Robot file = robots.txt
 * Ignore Queries = False
 * Rate: 2 task(s) per 1 sec(s)
http://www.vmusco.com/files/rapport_fr.pdf
http://www.vmusco.com
http://www.vmusco.com/academic.html
http://www.vmusco.com/files/abstract_fr.pdf
```

### Info printing

To totally silent infos, redirect `stderr` to `/dev/null`:

```
$ vincrawler http://www.vmusco.com 2> /dev/null
http://www.vmusco.com/files/abstract_fr.pdf
http://www.vmusco.com/academic.html
http://www.vmusco.com/files/rapport_fr.pdf
http://www.vmusco.com
```

Get more verbosity using the `-v[v+]` (max 3) option:

```
$ vincrawler http://www.vmusco.com -vvv
VinCrawler 0.1a1.
 * User-agent = vincrawler-bot/0.1a1
 * User URL = http://www.vmusco.com
 * Parsed URL = www.vmusco.com
 * Robot file = robots.txt
 * Ignore Queries = False
 * Rate: 2 task(s) per 1 sec(s)
1 url(s) in queue...
[1547083655.1479292] http://www.vmusco.com
        Skipping http://www.vmusco.com
        Skipping mailto://dhruk@redirect.vincenzomusco.com
        Skipping https://www.linkedin.com/in/vincenzo-musco
        Skipping http://www.github.com/v-m
        Skipping https://scholar.google.com/citations?user=y7P8mpIAAAAJ
        Skipping https://www.researchgate.net/profile/Vincenzo_Musco
        Skipping http://dblp.uni-trier.de/pers/hd/m/Musco:Vincenzo
        Adding http://www.vmusco.com/academic.html
        Skipping javascript://switchColor();
        Skipping http://www.vmusco.com/academic.html
        Skipping https://en.wikipedia.org/wiki/Mutation_testing
        Skipping https://www.wikiwand.com/en/Belgian_national_identity_card
1 url(s) in queue...
[1547083655.2678442] http://www.vmusco.com/academic.html
        Skipping http://www.vmusco.com
        Skipping mailto://dhruk@redirect.vincenzomusco.com
        Skipping https://www.linkedin.com/in/vincenzo-musco
        Skipping http://www.github.com/v-m
        Skipping https://scholar.google.com/citations?user=y7P8mpIAAAAJ
        Skipping https://www.researchgate.net/profile/Vincenzo_Musco
        Skipping http://dblp.uni-trier.de/pers/hd/m/Musco:Vincenzo
        Skipping http://www.vmusco.com/academic.html
        Skipping javascript://switchColor();
        Skipping http://dx.doi.org/10.1007/s11219-016-9332-8
        Skipping https://hal.inria.fr/hal-01346046/document
        Skipping https://github.com/v-m/PropagationAnalysis
        Skipping https://github.com/v-m/PropagationAnalysis-dataset
        Skipping https://tel.archives-ouvertes.fr/tel-01398903
        Skipping https://tel.archives-ouvertes.fr/tel-01398903/document
        Adding http://www.vmusco.com/files/abstract_fr.pdf
        Adding http://www.vmusco.com/files/rapport_fr.pdf
        Skipping https://doi.org/10.1109/SCAM.2016.24
        Skipping https://hal.inria.fr/hal-01350515/document
        Skipping https://github.com/v-m/PropagationAnalysis
        Skipping https://github.com/v-m/PropagationAnalysis-dataset
        Skipping http://dx.doi.org/10.1145/2896995.2896996
        Skipping https://hal.inria.fr/hal-01279620/document
        Skipping https://github.com/v-m/PropagationAnalysis
        Skipping https://github.com/v-m/PropagationAnalysis-dataset
        Skipping http://dx.doi.org/10.1109/AST.2015.20
        Skipping https://hal.inria.fr/hal-01120913/document
        Skipping https://github.com/v-m/PropagationAnalysis
        Skipping https://github.com/v-m/PropagationAnalysis-dataset
        Skipping http://arxiv.org/abs/1410.7921
        Skipping https://arxiv.org/pdf/1410.7921.pdf
        Skipping https://github.com/v-m/GDGNC
        Skipping https://zenodo.org/record/49665
2 url(s) in queue...
Waiting 0.7557551860809326 seconds
[1547083656.152234] http://www.vmusco.com/files/abstract_fr.pdf
1 url(s) in queue...
[1547083656.3658829] http://www.vmusco.com/files/rapport_fr.pdf
http://www.vmusco.com/files/abstract_fr.pdf
http://www.vmusco.com/academic.html
http://www.vmusco.com
http://www.vmusco.com/files/rapport_fr.pdf
```

### Specify the rate

If nothing is specified by the `robots.txt` file, 
the user is allowed to change the default rate by using the `--tasks` and `--unit` flags.
These flags specify how many tasks are allowed per unit of time (n seconds).
By default these are set to 2 request per 1 second. 
To change this behavior:

```
$ vincrawler http://www.vmusco.com --tasks 2 --unit 5 -vv
VinCrawler 0.1a1.
 * User-agent = vincrawler-bot/0.1a1
 * User URL = http://www.vmusco.com
 * Parsed URL = www.vmusco.com
 * Robot file = robots.txt
 * Ignore Queries = False
 * Rate: 2 task(s) per 5 sec(s)
1 url(s) in queue...
[1547067970.231126] http://www.vmusco.com
	Adding http://www.vmusco.com/academic.html
1 url(s) in queue...
[1547067970.351226] http://www.vmusco.com/academic.html
	Adding http://www.vmusco.com/files/abstract_fr.pdf
	Adding http://www.vmusco.com/files/rapport_fr.pdf
2 url(s) in queue...
Waiting 4.752922058105469 seconds
[1547067975.233991] http://www.vmusco.com/files/abstract_fr.pdf
1 url(s) in queue...
[1547067975.441032] http://www.vmusco.com/files/rapport_fr.pdf
http://www.vmusco.com/files/rapport_fr.pdf
http://www.vmusco.com
http://www.vmusco.com/academic.html
http://www.vmusco.com/files/abstract_fr.pdf
```

In this example, we specified that we want to execute 2 tasks maximum per 5 seconds.

## Tests

Simple test cases can be ran using:

```
python tests/test_crawler.py
```
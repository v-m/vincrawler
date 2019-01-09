"""
Base classes for the crawler
Author: Vincenzo Musco (http://www.vmusco.com)
Date: 9 January 2019
"""
from typing import List, Optional, Tuple

__author__ = "Vincenzo Musco (http://www.vmusco.com)"
__date__ = "9 January 2019"

import re
import sys
import bs4
from time import time, sleep
from urllib import robotparser
from urllib.parse import urljoin, urlparse
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from vmusco.logger import VerboseObject, VerboseLogger


class Crawler(VerboseObject):
    """
    Crawler object taking care of the crawling per se as well as the maximum # of queries per amount of time.
    """

    def __init__(self, starting_url: str, user_agent: str, robots_file: str = "robots.txt", tasks_per: int = 1,
                 per_unit: int = 1, ignore_queries: bool = False):
        """
        Constructor
        :param starting_url: the url to start from
        :param user_agent: the user agent to use
        :param robots_file: the robot file path to consider
        :param tasks_per: # of tasks to consider per amount of time defined in per_unit
        :param per_unit: # of seconds for a unit of time
        :param ignore_queries: define if the query part of the url should be considered or not
        """
        super().__init__()
        self._state = CrawlerState(starting_url, user_agent, robots_file, ignore_queries)
        self._last_task_issued_on: List[float] = []

        self._tasks_per = self._state.get_robots_tasks_per() or tasks_per
        self._per_unit = self._state.get_robots_per_unit() or per_unit

    def start(self) -> None:
        """
        Start the crawling process
        """
        self._logger.print_if_level(0, " * Rate: {} task(s) per {} sec(s)".format(self._tasks_per, self._per_unit))

        while self._state.has_more_to_visit():
            self._logger.print_if_level(2, "{} url(s) in queue...".format(self._state.nb_tasks_remaining()))
            url = self._state.visit_next()
            self._crawl(url)

    def set_logger(self, logger: VerboseLogger) -> None:
        """
        Change the logger. Ensure that all object using the logger uses the same one.
        :param logger: the new logger to use
        """
        super().set_logger(logger)
        self._state.set_logger(logger)

    def _crawl(self, an_url: Optional[str]) -> None:
        """
        One crawling operation (ie crawling one webpage url)
        :param an_url: the url of the web page to crawl
        """

        if an_url is not None:
            # We update the number of operation available in the remaining time slot
            self._update_available_slots()

            if not self._is_there_any_available_slots():
                # If there is not more slots available currently, let's wait until a new one is available
                wait_time = self._wait_time()
                self._logger.print_if_level(1, "Waiting {} seconds".format(wait_time))
                sleep(wait_time)
                self._crawl(an_url)
            else:
                # Recording the start time
                task_started_on = time()
                self._last_task_issued_on.append(task_started_on)
                self._logger.print_if_level(1, "[{}] {}".format(task_started_on, an_url))

                # Load the url
                req = Request(an_url, data=None, headers={'User-Agent': self._state.get_user_agent()})

                try:
                    with urlopen(req) as page:
                        soup = bs4.BeautifulSoup(page.read(), "html5lib")

                        # Mining links (<a> elements) on the page
                        for link in soup.select("a"):
                            if 'href' in link.attrs:
                                next_hop = urljoin(an_url, link['href'])
                                self._state.add_url_to_visit(next_hop)
                except HTTPError as e:
                    self._logger.print_if_level(1, "Error {} while crawling {}".format(e.code, an_url))

    def _update_available_slots(self) -> None:
        """
        Remove any slot which is now again available (according to per_unit)
        """
        while len(self._last_task_issued_on) > 0 and time() >= self._last_task_issued_on[0] + self._per_unit:
            self._last_task_issued_on.pop(0)

    def _is_there_any_available_slots(self) -> bool:
        """
        :return: true if there is any available time slot
        """
        return len(self._last_task_issued_on) < self._tasks_per

    def _wait_time(self) -> float:
        """
        :return: amount of time to wait before performing a new request
        """
        return self._last_task_issued_on[0] + self._per_unit - time()

    def result(self) -> List[str]:
        """
        :return: a list containing the crawled urls
        """
        return self._state.get_crawled_urls()


class CrawlerState(VerboseObject):
    """
    Object containing the crawled urls as well as the reaining ones to explore
    """

    def __init__(self, starting_url: str, user_agent: str, robots_file: str, ignore_queries: bool = False):
        """
        Constructor
        :param starting_url: the url to start from
        :param user_agent: the user agent to use
        :param robots_file: the robot file path to consider
        :param ignore_queries: define if the query part of the url should be considered or not
        """
        super().__init__()

        # Reading robots.txt file
        self._robot_file = None
        self._ignore_queries = ignore_queries

        if robots_file is not None:
            self._robot_file = robotparser.RobotFileParser()
            self._robot_file.set_url(urljoin(starting_url, robots_file))
            self._robot_file.read()

        # Storing user agent
        self._user_agent = user_agent or "*"

        # Queue for next to visit URLs
        self._visiting_queue = [starting_url]

        # Set containing visited URLs
        self._visited = set(self._visiting_queue)

        # Initial url
        self._parsed_start_url = urlparse(starting_url)

        print(" * User-agent = {}".format(self._user_agent), file=sys.stderr)
        print(" * User URL = {}".format(starting_url), file=sys.stderr)
        print(" * Parsed URL = {}".format(self._parsed_start_url.netloc), file=sys.stderr)
        print(" * Robot file = {}".format(robots_file), file=sys.stderr)
        print(" * Ignore Queries = {}".format(self._ignore_queries), file=sys.stderr)

    def get_robots_tasks_per(self) -> Optional[int]:
        """
        Return the number of tasks authorized by the server for a specific unit.
        :return: number of tasks authorized by the server for a specific unit or None if any.
        """
        if self._robot_file is not None:
            request_rate = self._robot_file.request_rate(self._user_agent)
            if request_rate is not None:
                return request_rate.requests

        if self._robot_file is not None:
            crawl_delay = self._robot_file.crawl_delay(self._user_agent)
            if crawl_delay is not None:
                return 1

        return None

    def get_robots_per_unit(self) -> Optional[int]:
        """
        Return the unit of time (# seconds) per requests in 'request rate' option of robots.txt.
        First search if there is any request rate specified, if not, then, look for crawl delay.
        :return: unit of time (# seconds) per requests
        """
        if self._robot_file is not None:
            request_rate = self._robot_file.request_rate(self._user_agent)
            if request_rate is not None:
                return request_rate.seconds

        if self._robot_file is not None:
            crawl_delay = self._robot_file.crawl_delay(self._user_agent)
            if crawl_delay is not None:
                return crawl_delay

        return None

    def get_user_agent(self) -> str:
        return self._user_agent

    def _can_fetch(self, an_url: str) -> bool:
        """
        :param an_url: an url to consider for crawling
        :return: true if this url is authorized by the robots.txt file
        """
        return self._robot_file is None or self._robot_file.can_fetch(self._user_agent, an_url)

    def _can_visit(self, an_url: str) -> Tuple[bool, str]:
        """
        Test whether an url can be crawled later on.
        The test consist of checking if the url belongs to the considered domain, is not already crawled and if it is
        authorized by the robots.txt file.
        Return as well a the rejection reason if any, that is, respectively: DOMAIN, ALREADY_VISITED or ROBOTS.TXT
        :param an_url: an url to consider for crawling
        :return: a 2-elements tuple containing a boolean (whether crawling is possible or not) and a string describing the reason if rejected
        """
        start_url = self._parsed_start_url.netloc
        current_url = urlparse(an_url).netloc

        reason = None
        if start_url != current_url and not start_url.endswith(current_url) and not current_url.endswith(start_url):
            reason = "DOMAIN"
        elif an_url in self._visited:
            reason = "ALREADY_VISITED"
        elif not self._can_fetch(an_url):
            reason = "ROBOTS.TXT"

        return reason is None, reason

    @staticmethod
    def clean_url(an_url: str, ignore_query: bool = False) -> str:
        """
        Clean an url (ie remove any fragment and leading slashes).
        Remove as well the ending slash if ignore_query is true.
        :param an_url: an url to consider for crawling
        :param ignore_query: Remove any ending slash from the path
        :return: a cleaned url
        """
        parsed_url = urlparse(an_url)
        query_part = ""
        param_part = ""
        cleaned_path = ""

        if not ignore_query and parsed_url.query != "":
            query_part = "?{url.query}".format(url=parsed_url) if parsed_url.query is not None else ""

        if parsed_url.params != "":
            param_part = ";{}".format(parsed_url.params)

        if parsed_url.path != "":
            cleaned_path = re.sub("/{2,}", "/", parsed_url.path)
            cleaned_path = cleaned_path[:-1] if cleaned_path[-1] == "/" else cleaned_path

        cleaned_url = "{url.scheme}://{url.netloc}{cleaned_path}{param_part}{query_if_any}"
        cleaned_url = cleaned_url.format(url=parsed_url, cleaned_path=cleaned_path, param_part=param_part,
                                         query_if_any=query_part)
        return cleaned_url

    def add_url_to_visit(self, new_url: str) -> bool:
        """
        Add an url to the crawling and crawled list only if this url is authorized (cf. _can_visit())
        :param new_url: an url to add
        :return: True if the url is authorized, False otherwise
        """
        cleaned_url = CrawlerState.clean_url(new_url, self._ignore_queries)

        can_visit, reason_if_any = self._can_visit(cleaned_url)
        if can_visit:
            self._logger.print_if_level(2, "\tAdding {}".format(cleaned_url))
            self._visited.add(cleaned_url)
            self._visiting_queue.append(cleaned_url)
            return True
        else:
            self._logger.print_if_level(3, "\tSkipping {} ({})".format(cleaned_url, reason_if_any))
            return False

    def get_crawled_urls(self) -> List[str]:
        """
        :return: the crawled result
        """
        return list(self._visited)

    def nb_tasks_remaining(self) -> int:
        """
        :return: # of tasks remaining to crawl
        """
        return len(self._visiting_queue)

    def has_more_to_visit(self) -> bool:
        """
        :return: True if there is any remaining task, False otherwise
        """
        return self.nb_tasks_remaining() > 0

    def is_visited(self, an_url: str) -> bool:
        """
        :param an_url: an url to consider for crawling
        :return: True if this url is already visited by this instance, False otherwise
        """
        return an_url in self._visited

    def visit_next(self) -> Optional[str]:
        """
        :return: the next element to visit, if any, otherwise return None
        """
        if self.has_more_to_visit():
            return self._visiting_queue.pop(0)

        return None

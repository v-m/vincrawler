"""
Unit Tests for the crawler
Author: Vincenzo Musco (http://www.vmusco.com)
Date: 9 January 2019
"""
__author__ = "Vincenzo Musco (http://www.vmusco.com)"
__date__ = "9 January 2019"

from vmusco.crawler import CrawlerState
import unittest


class TestCrawler(unittest.TestCase):
    def test_simple_path(self):
        cleaned_url = CrawlerState.clean_url("http://www.domain.com")
        self.assertEqual(cleaned_url, "http://www.domain.com")

    def test_with_ending_slash(self):
        cleaned_url = CrawlerState.clean_url("http://www.domain.com/")
        self.assertEqual(cleaned_url, "http://www.domain.com")

    def test_with_way_too_much_ending_slash(self):
        cleaned_url = CrawlerState.clean_url("http://www.domain.com//////")
        self.assertEqual(cleaned_url, "http://www.domain.com")

    def test_with_query_and_ending_slash(self):
        cleaned_url = CrawlerState.clean_url("http://www.domain.com/?query=value")
        self.assertEqual(cleaned_url, "http://www.domain.com?query=value")

    def test_no_query_with_query_and_ending_slash(self):
        cleaned_url = CrawlerState.clean_url("http://www.domain.com/?query=value", True)
        self.assertEqual(cleaned_url, "http://www.domain.com")

    def test_with_fragment(self):
        cleaned_url = CrawlerState.clean_url("http://www.domain.com#fragment")
        self.assertEqual(cleaned_url, "http://www.domain.com")

    def test_with_fragment_and_ending_slash(self):
        cleaned_url = CrawlerState.clean_url("http://www.domain.com/#fragment")
        self.assertEqual(cleaned_url, "http://www.domain.com")

    def test_with_fragment_query_and_ending_slash(self):
        cleaned_url = CrawlerState.clean_url("http://www.domain.com/?query=value#fragment")
        self.assertEqual(cleaned_url, "http://www.domain.com?query=value")

    def test_no_query_with_fragment_query_and_ending_slash(self):
        cleaned_url = CrawlerState.clean_url("http://www.domain.com/?query=value#fragment", True)
        self.assertEqual(cleaned_url, "http://www.domain.com")

    def test_with_queries(self):
        cleaned_url = CrawlerState.clean_url("http://www.domain.com/?query=value&query2=value2")
        self.assertEqual(cleaned_url, "http://www.domain.com?query=value&query2=value2")

    def test_no_query_with_queries(self):
        cleaned_url = CrawlerState.clean_url("http://www.domain.com/?query=value&query2=value2", True)
        self.assertEqual(cleaned_url, "http://www.domain.com")

    def test_full_address(self):
        cleaned_url = CrawlerState.clean_url("http://www.domain.com/index.html;someparam=some;otherparam=other?query1"
                                             "=val1&query2=val2#frag")
        self.assertEqual(cleaned_url, "http://www.domain.com/index.html;someparam=some;otherparam=other?query1=val1"
                                      "&query2=val2")

    def test_no_query_full_address(self):
        cleaned_url = CrawlerState.clean_url("http://www.domain.com/index.html;someparam=some;otherparam=other?query1"
                                             "=val1&query2=val2#frag",
                                             True)
        self.assertEqual(cleaned_url, "http://www.domain.com/index.html;someparam=some;otherparam=other")


if __name__ == '__main__':
    unittest.main()

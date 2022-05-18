import logging
from datetime import datetime
from datetime import timezone
from datetime import timedelta

from django.test import TestCase

from helpers.date_helper import pretty_date


class DateHelperTest(TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def test_date_as_timestamp(self):
        """ call date helper, feed it a raw timestamp """
        test_date = datetime.now(timezone.utc).timestamp()
        result_str = pretty_date(int(test_date))
        self.assertEqual(result_str, 'just now')


    def test_negative_days(self):
        """ call date helper, feed it a negative day (-2 days) difference """
        test_date = datetime.now(timezone.utc) - timedelta(days=-2)
        result_str = pretty_date(test_date)
        self.assertEqual(result_str, '')


    def test_date_just_now(self):
        """ call date helper, ask for a date 'just now' """
        now = datetime.now(timezone.utc)
        test_date = now
        result_str = pretty_date(test_date)
        self.assertEqual(result_str, 'just now')


    def test_date_seconds_ago(self):
        """ call date helper, ask for a date '30 seconds ago' """
        test_date = datetime.now(timezone.utc) - timedelta(seconds=30)
        result_str = pretty_date(test_date)
        self.assertEqual(result_str, '30 seconds ago')


    def test_date_a_minute_ago(self):
        """ call date helper, ask for a date 'a minute ago' """
        test_date = datetime.now(timezone.utc) - timedelta(seconds=90)
        result_str = pretty_date(test_date)
        self.assertEqual(result_str, 'a minute ago')


    def test_date_minutes_ago(self):
        """ call date helper, ask for a date '5 minutes ago' """
        test_date = datetime.now(timezone.utc) - timedelta(seconds=60*5)
        result_str = pretty_date(test_date)
        self.assertEqual(result_str, '5 minutes ago')


    def test_date_an_hour_ago(self):
        """ call date helper, ask for a date 'an hour ago' """
        test_date = datetime.now(timezone.utc) - timedelta(seconds=60*60+30)
        result_str = pretty_date(test_date)
        self.assertEqual(result_str, 'an hour ago')


    def test_date_hours_ago(self):
        """ call date helper, ask for a date '2 hours ago' """
        test_date = datetime.now(timezone.utc) - timedelta(seconds=60*60*2)
        result_str = pretty_date(test_date)
        self.assertEqual(result_str, '2 hours ago')


    def test_date_yesterday(self):
        """ call date helper, ask for a date 'yesterday' """
        test_date = datetime.now(timezone.utc) - timedelta(days=1)
        result_str = pretty_date(test_date)
        self.assertEqual(result_str, 'Yesterday')


    def test_date_four_days_ago(self):
        """ call date helper, ask for a date '4 days ago' """
        test_date = datetime.now(timezone.utc) - timedelta(days=4)
        result_str = pretty_date(test_date)
        self.assertEqual(result_str, '4 days ago')


    def test_date_three_weeks_ago(self):
        """ call date helper, ask for a date '3 weeks ago' """
        test_date = datetime.now(timezone.utc) - timedelta(days=21)
        result_str = pretty_date(test_date)
        self.assertEqual(result_str, '3 weeks ago')


    def test_date_two_months_ago(self):
        """ call date helper, ask for a date '2 months ago' """
        test_date = datetime.now(timezone.utc) - timedelta(days=60)
        result_str = pretty_date(test_date)
        self.assertEqual(result_str, '2 months ago')


    def test_date_three_years_ago(self):
        """ call date helper, ask for a date '3 years ago' """
        test_date = datetime.now(timezone.utc) - timedelta(days=365*3)
        result_str = pretty_date(test_date)
        self.assertEqual(result_str, '3 years ago')

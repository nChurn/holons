import datetime
import hashlib
import json
import logging
import random

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from rays.models import RaySource
from rays.models import UpworkTalent

import holons.management.commands.v4_import_rays_rss as rays


# LOGGING = False
LOGGING = True

MASTER_RAY = RaySource.objects.filter(title='Test Master ray').first()
MASTER_RAY_PK = 108


class ImportRaysRssTestCase(TestCase):
    master_ray = []
    master_messages = []
    date_stamp = str(datetime.datetime.now().timestamp()).split('.')[0][0:8]

    def setUp(self):
        call_command('loaddata', 'holons/seed/ray_sources.json', verbosity=0)
        call_command('loaddata', 'holons/seed/master_ray_messages.json', verbosity=0)
        date_stamp = self.date_stamp
        self.password = '22test22'
        self.username = 'test_' + date_stamp
        self.user = get_user_model().objects.create_user(
          username=self.username,
          password=self.password,
          email=self.username + '@holons-test.me',
          phone_number='123'
        )
        self.user.cors_storage = json.dumps({'test': 'test'})
        self.user.save()
        self.password1 = '22test22'
        self.username1 = 'test1_' + date_stamp
        self.user1 = get_user_model().objects.create_user(
          username=self.username1,
          password=self.password1,
          email=self.username1 + '@holons-test.me',
          phone_number='222'
        )
        self.user1.cors_storage = json.dumps({'test': 'test'})
        self.user1.save()
        self.master_ray = RaySource.objects.get(title='Test Master ray')
        self.master_ray.users.add(self.user)
        self._prepare_messages()


    def tearDown(self):
        UpworkTalent.objects.all().delete()
        RaySource.objects.all().delete()
        self.user.delete()


    def _prepare_messages(self):
        """Get fixture messages and attach them to a master ray"""
        self.master_messages = UpworkTalent.objects.all()
        for message in self.master_messages:
            message.pub_date = self.date_stamp
            message.save()
            self.master_ray.messages.add(message)


    def test_sync_master_ray(self):
        """Test sync master ray
        """

        ray_source = RaySource.objects.filter(pk=MASTER_RAY_PK).get()
        rays.sync_master_ray()
        master_ray_messages = UpworkTalent.objects\
                    .filter(ray_source_id=MASTER_RAY_PK)\
                    .order_by('-id').all()[0:100]
        self.assertNotEquals(len(master_ray_messages), 0)


    def test_create_uncategorized_user_ray(self):
        """Test creation of 'ALL' ray
        """

        uncategorized_ray = rays.create_uncategorized_user_ray(self.user)
        user_ray = self.user.rays.filter(title='ALL')\
                    .exclude(pk=MASTER_RAY_PK).all().first()
        self.assertEquals(user_ray.title, 'ALL')


    def test_get_category_text(self):
        """Check category name text extraction"""
        
        category_text = ('mobile app development','motion graphics')
        messages = UpworkTalent.objects.filter(category__in=category_text)
        for message in messages:
          category = rays.get_category_text(message)
          self.assertTrue(category in category_text)


    def test_get_skills_text(self):
        """Check skills text extraction"""

        skills_text = 'illustration'
        messages = UpworkTalent.objects.filter(skills__icontains=skills_text)
        for message in messages:
          skills = rays.get_skills_text(message)
          self.assertTrue(skills_text in skills)


    def test_get_country_text(self):
        """Check country text extraction"""
        
        country_text = ('united states', 'united kingdom')
        messages = UpworkTalent.objects.filter(country__in=country_text)
        for message in messages:
          country = rays.get_country_text(message.description)
          self.assertTrue(country, country_text)


    def test_get_fresh_messages_from_master(self):
        """Count messages recieved from master"""

        messages = rays.get_fresh_messages_from_master()
        self.assertEquals(len(messages), len(self.master_messages))


    def test_prepare_unsorted_fresh_messages(self):
        """Count messages recieved from master,
        mapped to a [{message: msg, ray_id: 0}] list
        """

        messages = rays.prepare_unsorted_fresh_messages(self.user)
        self.assertEquals(len(messages), len(self.master_messages))


    def test_filter_by_country(self):
        """Get a ray with key_words
        Load all messages
        For each message run filter by country check
        compare that each True match.country is in a ray.key_words_list
        and vice versa
        """

        ray = RaySource.objects.get(title__exact='[dev] Java')
        self.user.rays.add(ray)
        for msg in self.master_messages:
            message = rays.filter_by_country(msg, ray)
            message_country = message["message"].country.replace(' ', '').strip()
            if message["save_ok"] is True:
                self.assertTrue(message_country in ray.key_words_list)
            else:
                self.assertFalse(message_country in ray.key_words_list)


    def test_filter_by_empty_budget(self):
        """Get all messages with empty budget and empty rates
        For each message run filter
        Count and compare results
        """

        messages = self.master_messages\
                      .filter(budget__isnull=True)\
                      .exclude(rate_from__isnull=False)\
                      .exclude(rate_to__isnull=False)
        messages_check = 0
        for msg in messages:
            message_save = rays.filter_by_empty_budget(msg)
            if message_save is True:
                messages_check += 1
        self.assertEquals(len(messages), messages_check)
            
            
    def test_filter_by_fixed_budget(self):
        """Get all messages with fixed budget
        For each message run filter
        Count and compare results
        """

        messages = self.master_messages\
                      .filter(budget__isnull=False)\
                      .filter(budget__gt=999)
        messages_check = 0
        for msg in messages:
            message_save = rays.filter_by_fixed_budget(budget_fixed=999, message=msg)
            if message_save is True:
                messages_check += 1
        self.assertEquals(len(messages), messages_check)


    def test_match_message_by_category(self):
        """Check for category filters"""

        ray1 = RaySource.objects.get(title='AAB. Full Stack //TEAR DOWN')
        ray2 = RaySource.objects.get(title='[test] category')
        for msg in self.master_messages:
            message = rays.match_message_by_category(msg, ray1)
            if message['save_ok']:
              self.assertTrue(message['message'].category in ray1.category_filter_list)
        for msg in self.master_messages:
            message =  rays.match_message_by_category(msg, ray2)
            if message['save_ok']:
              self.assertTrue(message['message'].category in ray2.category_filter_list)


    def test_match_message_by_title(self):
        """Get ray with title_filter set, get ray with empty title filter
        Go over master messages, make sure that filter works
        """

        ray = RaySource.objects.get(title='[dev] Java')
        ray2 = RaySource.objects.get(title='AOC. Video Editing/Post-Production [content] (19)')
        # check working filter
        for msg in self.master_messages:
            message = rays.match_message_by_title(msg, ray)
            if message['save_ok']:
                self.assertTrue('Java' in message['message'].title)
        messages_count = 0
        # check empty filter
        for msg in self.master_messages:
            message = rays.match_message_by_title(msg, ray2)
            if message['save_ok']:
                messages_count += 1
        self.assertEquals(messages_count, len(self.master_messages))


    def test_match_message_by_skill(self):
        """Check filtering by skill
        """

        ray1 = RaySource.objects.get(title='[dev] Java')
        ray2 = RaySource.objects.get(title='[dev] Ruby on Rails')
        for msg in self.master_messages:
            message = rays.match_message_by_skill(msg, ray1)
            if message['save_ok']:
                skills_count = 0
                for skill in message['message'].skills.split(','):
                  if skill.strip() in ray1.skills_filter_list:
                      skills_count += 1
                self.assertTrue(skills_count > 0)
        for msg in self.master_messages:
            message = rays.match_message_by_skill(msg, ray2)
            if message['save_ok']:
                skills_count = 0
                for skill in message['message'].skills.split(','):
                  if skill.strip() in ray2.skills_filter_list:
                      skills_count += 1
                self.assertTrue(skills_count > 0)


    def test_filter_by_budgets(self):
        """Get rays with different budget filters,
        Go over messages, run budget filter, check results
        """

        ray1 = RaySource.objects.get(title='AAB. Full Stack //TEAR DOWN')
        ray2 = RaySource.objects.get(title='[dev] Java')
        messages_check = 0
        for msg in self.master_messages:
            message = rays.filter_by_budgets(msg, ray1)
            if message['save_ok'] is True:
                msg_check = message['message']
                if msg_check.budget:
                    self.assertTrue(msg_check.budget.amount >= ray1.budget_fixed)
                elif msg_check.rate_from:
                    self.assertTrue(msg_check.rate_to.amount >= ray1.budget_rate)
                elif ray1.is_budget_empty_ok:
                    self.assertTrue(msg_check.rate_to is None and msg_check.budget is None)
        check_messages = 0
        for msg in self.master_messages:
            message = rays.filter_by_budgets(msg, ray2)
            if message['save_ok'] is True:
                check_messages += 1
        self.assertEquals(len(self.master_messages), check_messages)


    def test_attribute_messages_country(self):
        """Try to test attribution by country
        """

        ray_key_words = RaySource.objects\
                              .get(title__exact="[test] country USA")
        # create an ALL ray for a test user
        uncategorized_ray = rays.create_uncategorized_user_ray(self.user1)
        # connect key_words ray to the user
        self.user1.rays.add(ray_key_words)
        # call attribution function
        rays.attribute_messages(self.user1)
        self.assertEquals(ray_key_words.messages.all().count(), 28)
              
              
    def test_attribute_messages_category(self):
        """Try to test attribution by category
        """

        ray_category = RaySource.objects\
                              .get(title__exact="[test] category Full Stack")
        # create an ALL ray for a test user
        uncategorized_ray = rays.create_uncategorized_user_ray(self.user1)
        # connect key_words ray to the user
        self.user1.rays.add(ray_category)
        # call attribution function
        rays.attribute_messages(self.user1)
        self.assertEquals(ray_category.messages.all().count(), 6)


    def test_attribute_messages_skill(self):
        """Try to test attribution by skill
        """

        ray_skills = RaySource.objects\
                              .get(title__exact="[test] skill ROR")
        # create an ALL ray for a test user
        uncategorized_ray = rays.create_uncategorized_user_ray(self.user1)
        # connect ray_skills ray to the user
        self.user1.rays.add(ray_skills)
        # call attribution function
        rays.attribute_messages(self.user1)
        self.assertEquals(ray_skills.messages.all().count(), 2)


    def test_attribute_messages_title(self):
        """Try to test by title
        """

        ray_titles = RaySource.objects\
                              .get(title__exact="[test] title Wordpress")
        # create an ALL ray for a test user
        uncategorized_ray = rays.create_uncategorized_user_ray(self.user1)
        # connect ray_skills ray to the user
        self.user1.rays.add(ray_titles)
        messages = UpworkTalent.objects\
                              .filter(title__icontains='wordpres')
        # call attribution function
        rays.attribute_messages(self.user1)
        self.assertEquals(ray_titles.messages.all().count(), 5)


    def test_attribute_messages_by_country_and_category(self):
        """Try to test country AND category filters complex behaviour.
        """

        ray_country_category = RaySource.objects\
                              .get(title__exact="[test] country category")
        # create an ALL ray for a test user
        uncategorized_ray = rays.create_uncategorized_user_ray(self.user1)
        # connect key_words ray to the user
        messages = UpworkTalent.objects\
                              .filter(country__exact='united states')\
                              .filter(category__exact='front-end development')
        self.user1.rays.add(ray_country_category)
        # call attribution function
        rays.attribute_messages(self.user1)
        self.assertEquals(ray_country_category.messages.all().count(), 2)


    def test_attribute_messages_by_country_category_and_skill(self):
        """Try to test country AND category filters complex behaviour.
        """

        ray_country_category_skill = RaySource.objects\
                              .get(title__exact="[test] country category and skill")
        # create an ALL ray for a test user
        uncategorized_ray = rays.create_uncategorized_user_ray(self.user1)
        # connect key_words ray to the user
        messages = UpworkTalent.objects\
                              .filter(country__exact='united states')\
                              .filter(category__exact='front-end development')\
                              .filter(skills__icontains='figma')
        self.user1.rays.add(ray_country_category_skill)
        # call attribution function
        rays.attribute_messages(self.user1)
        self.assertEquals(ray_country_category_skill.messages.all().count(), 3)

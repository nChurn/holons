import datetime
import hashlib
import random
import logging
import json

from django.test import TestCase
from django.test import RequestFactory
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpRequest
from rays.models import RaySource
from rays.models import UpworkTalent

from accounts import views


TEST_MESSAGE_TITLE="Write my company's profile - Upwork"
TEST_MESSAGE_LINK='https://www.upwork.com/jobs/Write-company-profile_%7E01?source=rss'
TEST_MESSAGE_DESC  = """Write a company&#039;s profile for my proprietary trading"""
TEST_MESSAGE_DESC += """firm<br /><br /><b>Budget</b>: $50"""
TEST_MESSAGE_DESC += """<br /><b>Posted On</b>: June 09, 2021 19:32 UTC<br />"""
TEST_MESSAGE_DESC += """<b>Category</b>: #category#<br /><b>Skills</b>:"""
TEST_MESSAGE_DESC += """#skills#    """
TEST_MESSAGE_DESC += """<br /><b>Country</b>: #country#"""
TEST_MESSAGE_DESC += """<br /><a href="#link#">click to apply</a> <br /><br />"""
TEST_MESSAGE_DESC += """message_guid: 002ca74a032630cead3f235188cbdc4_108"""

RAYS_SOURCE = settings.RAYS_SOURCE

class AccountsAuthTest(TestCase):


    date_stamp = str(datetime.datetime.now().timestamp()).split('.')[0][0:8]
    def setUp(self):
        date_stamp = self.date_stamp
        self.password = '12test12'
        self.username = 'test_' + date_stamp
        self.username_wrong = 'test_wrong' + date_stamp
        self.user = get_user_model().objects.create_user(
          username=self.username,
          password=self.password,
          email=self.username + '@holons-test.me',
          phone_number='123'
        )
        self.teleport_username = ''
        self.user.save()
        '''Prepare requests'''
        self.factory = RequestFactory()


    def tearDown(self):
        # self.user_wrong.delete()
        self.user.delete()


    def test_holons_login_no_creds(self):
        """Try to login with no credentials"""
        data = json.dumps({})
        request = self.factory.post('/')
        request._body = data
        response = views.holons_login(request)
        response_data = json.loads(response.content)
        self.assertEquals(response_data['result'], 'Not OK')


    def test_holons_login_no_username(self):
        """Try to login with no username
        :todo: We need to mock API-request in order to test further
        """
        '''
        data = json.dumps({'phone_number': '123'})
        request = self.factory.post('/')
        request._body = data
        # user = authenticate(username=self.username, password=self.password)
        response = views.holons_login(request)
        response_data = json.loads(response.content)
        '''
        pass

        
    def test_user_register(self):
        """Create a Django user"""
        email = 'testuser123@holons.me'
        name = 'testuser123'
        phone = '123123'
        confirmation_code = '0000'
        user = views.user_register(email, name, phone, confirmation_code)
        self.assertEquals(user.username, name)


    def test_teleport_user_generate_password(self):
        """Check teleport password generator
        As ugly as it is written
        """
        password = views.teleport_user_generate_password(self.user)
        check_password = self.user.email.replace('@', '_at_') + '_password_disabled' 
        self.assertEquals(password, check_password)


    def _create_upwork_message(self, title: str = '', description: str = '', **kwargs) -> UpworkTalent:
        """Utility function to create a basic UpworkTalent message
        """
        message = UpworkTalent.objects.create(
          title=title,
          description=description,
          **kwargs,
        )
        return message

    def _create_message(self, ray: RaySource,
                        category: str ='', skills: str ='', title: str ='',
                        budget_fixed: str = '',
                        budget_rate: str = '',
                        **kwargs):
        """Utility function to create similar messages with set Category, Skills, Title
        """

        h = hashlib.new('md5')
        h.update(str(random.random()).encode('utf-8'))
        hash_guid = str(h.hexdigest())[0:8]
        
        description = TEST_MESSAGE_DESC\
                                      .replace('#category#', category)\
                                      .replace('#skills#', skills)\
                                      .replace('#country#', 'United States')
        description += kwargs.get('key_words', '')
        description += f' random string: {hash_guid}'  
        if budget_fixed != '':
            description = description\
                          .replace('<b>Budget</b>: $50', '<b>Budget</b>: $' + budget_fixed)
        if budget_rate != '':
            description = description\
                          .replace('<b>Budget</b>: $50', '<b>Hourly Range</b>: $' + budget_rate + '-$100')
        title += f' {hash_guid}'  
        message = self._create_upwork_message(title, description, guid=hash_guid + f'_{ray.id}')
        ray.messages.add(message)
        return message


    def _create_ray(self, title: str = '', key_words: str = '', stop_words: str = '',
                    title_filter: str = '', skills_filter: str = '',
                    category_filter: str = '', budget_rate: str = 0,
                    budget_fixed: int = 0, link: str = '',
                    budget_ignored: bool = True) -> RaySource:
        """Utility function to create RaySettings
        """
        if budget_fixed != 0 or budget_rate != 0:
            budget_ignored = False 

        ray_source = RaySource.objects.create(
          title=title,
          link=link,
          stop_words=stop_words,
          key_words=key_words,
          title_filter=title_filter,
          skills_filter=skills_filter,
          category_filter=category_filter,
          is_budget_empty_ok=budget_ignored,
          budget_rate=int(budget_rate),
          budget_fixed=int(budget_fixed),
          is_active=True
        )
        ray_source.save()
        # ray_source.users.add(self.user)

        return ray_source


    def test_user_login(self):
        ray1 = self._create_ray(title='ray1 categb',
                                category_filter='find me, findme',
                                budget_fixed='98')
        ray2 = self._create_ray(title='ray2 skillb',
                                skills_filter='find me skill, skill1',
                                budget_fixed='8')
        ray3 = self._create_ray(title='ray3 title',
                                title_filter='find me',
                                budget_fixed='50')
        """Create a Django user"""
        email = 'talant@holons.me'
        name = RAYS_SOURCE
        phone = '333333'
        confirmation_code = '0000'
        data = json.dumps({
          'phone_number': phone,
          'confirmation_code': confirmation_code,
        })
        user = views.user_register(email, name, phone, confirmation_code)
        user.rays.add(ray1)
        user.rays.add(ray2)
        user.rays.add(ray3)
        message1 = self._create_message(
                              ray1,
                              category='find me',
                              skills='find me',
                              title='fixed budget 100',
                              budget_fixed='100'
                            )
        message2 = self._create_message(
                              ray2,
                              category='find me',
                              skills='find me',
                              title='fixed budget 22',
                              budget_fixed='22'
                            )
        message3 = self._create_message(
                              ray3,
                              category='find me',
                              skills='find me',
                              title='fixed_budget 66',
                              budget_fixed='66'
                            )
        email = 'testuser123@holons.me'
        name = 'testuser123'
        phone = '123123'
        confirmation_code = '0000'
        data = json.dumps({
          'phone_number': phone,
          'confirmation_code': confirmation_code,
        })
        request = self.factory.post('/')
        request._body = data
        request.user = AnonymousUser()
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        user = views.user_register(email, name, phone, confirmation_code)
        # user = authenticate(username=self.username, password=self.password)
        response = views.confirmation(request)
        # self.assertEquals(user.username, name)

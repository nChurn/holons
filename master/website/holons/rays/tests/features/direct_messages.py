import datetime
import json
import logging
import os

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import RequestFactory
from django.test import TestCase

from rays.direct_messages import *
from rays.models.ray import Ray


class DirectMessagesTest(TestCase):


    date_stamp = str(datetime.datetime.now().timestamp()).split('.')[0][0:8]
    def setUp(self):
        self.RAY_SOURCES = settings.RAY_SOURCES
        image_path = os.path.join(str(settings.BASE_DIR), "mock/sample_image.jpg")
        userpic = SimpleUploadedFile(name='sample_image.jpg',
          content=open(image_path, 'rb').read(),
          content_type='image/jpeg')
        call_command('loaddata', 'accounts/seed/fixed_users.json', verbosity=0)
        date_stamp = self.date_stamp
        self.password = '12test12'
        self.username = 'test_' + date_stamp

        self.username_second = 'test_wrong' + date_stamp
        self.user_from = get_user_model().objects.create_user(
          username=self.username + '_from',
          password=self.password,
          email=self.username + '_from' + '@holons-test.me',
          phone_number='123'
        )
        self.user_from.userpic = userpic
        self.user_to = get_user_model().objects.create_user(
          username=self.username + '_to',
          password=self.password,
          email=self.username  + '_to' + '@holons-test.me',
          phone_number='222'
        )
        self.user_to.userpic = userpic
        self.user_third = get_user_model().objects.create_user(
          username=self.username + '_third',
          password=self.password,
          email=self.username  + '_third' + '@holons-test.me',
          phone_number='333'
        )
        self.user_third.userpic = userpic
        self.teleport_username = ''
        self.user_from.save()
        self.user_to.save()
        self.user_third.save()
        '''Prepare requests'''

        self.factory = RequestFactory()

        self.message1 = {
          'subject': 'message1 subject',
          'message_body': 'message1 body',
        }
        self.message2 = {
          'subject': 'message2 subject',
          'message_body': 'message2 body',
        }
        self.message3 = {
          'subject': 'message3 subject',
          'message_body': 'message3 body',
        }


    def tearDown(self):
        self.user_from.delete()
        self.user_to.delete()
        self.user_third.delete()


    def test_rays_custom_message_no_creds(self):
        """Test sending a custom message AnonymousUser"""
        url = '/'
        request = self.factory.post(url)
        request.user = AnonymousUser()
        request.session = {}
        response = rays_custom_message(request)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/auth')


    def test_rays_custom_message(self):
        """test sending a direct message"""
        url = '/'
        """check empty request behavior"""
        request = self.factory.post(url, content_type='application/json')
        request.user = self.user_from
        response = rays_custom_message(request)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(json.loads(response.content)['message'], 'empty request')
        """Check partial data request behavior"""
        data = {
          'wrong_title': 'test title',
        }
        request = self.factory.post(url, data, content_type='application/json')
        request.user = self.user_from
        response = rays_custom_message(request)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(json.loads(response.content)['message'], 'empty title')
        data = {
          'title': 'test title',
        }
        request = self.factory.post(url, data, content_type='application/json')
        request.user = self.user_from
        response = rays_custom_message(request)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(json.loads(response.content)['message'], 'empty description')
        data = {
          'title': 'test title',
          'description': 'test description',
        }
        request = self.factory.post(url, data, content_type='application/json')
        request.user = self.user_from
        response = rays_custom_message(request)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(json.loads(response.content)['message'], 'empty ray source')
        """Check all correct data request behavior"""
        data = {
          'title': 'test title',
          'description': 'test description',
          'ray_source': 'moneta',
        }
        request = self.factory.post(url, data, content_type='application/json')
        request.user = self.user_from
        response = rays_custom_message(request)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content)['message'], data['title'])
        """:todo: CHECK FOR AN ACTUAL MESSAGE"""


    def test_rays_send_direct_message_no_creds(self):
        """Test sending a direct message AnonymousUser"""
        url = '/'
        request = self.factory.post(url)
        request.user = AnonymousUser()
        request.session = {}
        response = rays_send_direct_message(request)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/auth')


    def test_rays_send_direct_message(self):
        """test sending a direct message"""
        url = '/'
        """check empty request behavior"""
        request = self.factory.post(url, content_type='application/json')
        request.user = self.user_from
        response = rays_send_direct_message(request)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(json.loads(response.content)['message'], 'empty request')
        """Check partial data request behavior"""
        data = {
          'wrong_title': 'test title',
        }
        request = self.factory.post(url, data, content_type='application/json')
        request.user = self.user_from
        response = rays_send_direct_message(request)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(json.loads(response.content)['message'], 'empty to')
        """Check partial data request behavior"""
        data = {
          'to': self.user_to.id.id,
        }
        request = self.factory.post(url, data, content_type='application/json')
        request.user = self.user_from
        response = rays_send_direct_message(request)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(json.loads(response.content)['message'], 'empty subject')
        """Check partial data request behavior"""
        data = {
          'to': self.user_to.id.id,
          'subject': self.message1['subject'],
        }
        request = self.factory.post(url, data, content_type='application/json')
        request.user = self.user_from
        response = rays_send_direct_message(request)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(
          json.loads(response.content)['message'], 'empty message_body'
        )
        """Check all correct data request behavior"""
        data = {
          'to': self.user_to.id.id,
          'subject': self.message1['subject'],
          'message_body': self.message1['message_body'],
        }
        request = self.factory.post(url, data, content_type='application/json')
        request.user = self.user_from
        response = rays_send_direct_message(request)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(
          json.loads(response.content)['message'], 'message sent'
        )
        """Check sending a reply request"""
        data = {
          'to': self.user_to.id.id,
          'subject': self.message1['subject'],
          'message_body': self.message1['message_body'],
          'reply_to_id': json.loads(response.content)['message_id'],
        }
        request = self.factory.post(url, data, content_type='application/json')
        request.user = self.user_from
        response = rays_send_direct_message(request)
        
        self.assertEquals(response.status_code, 200)
        self.assertEquals(
          json.loads(response.content)['message'], 'message sent as a reply'
        )


    def test_create_common_ray(self):
        """test creation of a common Ray"""
        common_ray = create_common_ray(self.user_from, self.user_to)
        """Make sure we have a Ray object"""
        self.assertTrue(isinstance(common_ray, Ray))
        """Make sure the Ray has from and to users"""
        self.assertEquals(common_ray.users.all()[0].id, self.user_from.id)
        self.assertEquals(common_ray.users.all()[1].id, self.user_to.id)


    def test_get_common_ray(self):
        """create a common Ray"""
        created_common_ray = create_common_ray(self.user_from, self.user_to)
        common_ray = get_common_ray(self.user_from, self.user_to)
        """check we are getting a Ray instance"""
        self.assertTrue(isinstance(common_ray, Ray))
        """destroy the ray"""
        common_ray.delete()
        """rerun get_"""
        common_ray = get_common_ray(self.user_from, self.user_to)
        """check we are getting a Ray instance"""
        self.assertTrue(isinstance(common_ray, Ray))
        """destroy the ray"""
        common_ray.delete()
        """check creation of a common ray in case user has a normal non-shared ray"""
        ray = Ray.objects.create()
        created_common_ray = create_common_ray(self.user_from, self.user_third)
        orphan_ray = get_common_ray(self.user_from, self.user_to)
        """check we are getting a Ray instance"""
        self.assertTrue(isinstance(common_ray, Ray))


    def test_list_user_direct_rays(self):
        """Make sure user gets a list of Rays with direct messages
        
        * post a message1 user_from -> user_to
        * post a message2 user_from -> user_third
        * post a message3 to user_to -> user_from 
        * call list_user_direct_rays on user_from 
        * call list_user_direct_rays on user_to 
        * call list_user_direct_rays on user_third
        * check user_from has message1
        * check user_from has message2
        * check user_from has message3
        * check user_to has message1
        * check user_to has message3
        * check user_third has message2
        
        :todo: consider checking message attribution more extensively
        :todo: invent a way to check for a message in a more simple way

        """

        def _check_message_subject_in_rays(user_rays: list, subject: str) -> bool:
            for el in user_rays:
              for msg_thread in el['message_threads']:
                for msg in msg_thread['messages']:
                  if msg['subject'] == subject:
                    return True

        url = '/'
        
        """Send message1"""
        data = {
          'to': self.user_to.id.id,
          'subject': self.message1['subject'],
          'message_body': self.message1['message_body'],
        }
        request = self.factory.post(url, data, content_type='application/json')
        request.user = self.user_from
        response = rays_send_direct_message(request)
        """Send message2"""
        data = {
          'to': self.user_third.id.id,
          'subject': self.message2['subject'],
          'message_body': self.message2['message_body'],
        }
        request = self.factory.post(url, data, content_type='application/json')
        request.user = self.user_from
        response = rays_send_direct_message(request)
        """Send message3"""
        data = {
          'to': self.user_from.id.id,
          'subject': self.message3['subject'],
          'message_body': self.message3['message_body'],
        }
        request = self.factory.post(url, data, content_type='application/json')
        request.user = self.user_to
        response = rays_send_direct_message(request)
        
        user_from_rays = list_user_direct_rays(self.user_from)
        user_to_rays = list_user_direct_rays(self.user_to)
        user_third_rays = list_user_direct_rays(self.user_third)

        subject1_uf_check = _check_message_subject_in_rays(
          user_from_rays, self.message1['subject'])
        subject2_uf_check = _check_message_subject_in_rays(
          user_from_rays, self.message2['subject'])
        subject3_uf_check = _check_message_subject_in_rays(
          user_from_rays, self.message3['subject'])
        subject1_uto_check = _check_message_subject_in_rays(
          user_to_rays, self.message1['subject'])
        subject3_uto_check = _check_message_subject_in_rays(
          user_to_rays, self.message3['subject'])
        subject2_uth_check = _check_message_subject_in_rays(
          user_third_rays, self.message2['subject'])

        self.assertTrue(subject1_uf_check)
        self.assertTrue(subject2_uf_check)
        self.assertTrue(subject3_uf_check)
        self.assertTrue(subject1_uto_check)
        self.assertTrue(subject3_uto_check)
        self.assertTrue(subject2_uth_check)


    def test_user_rays_direct_no_creds(self):
        """Make sure a random dude can not get a list of direct rays"""
        url = '/'
        request = self.factory.get(url)
        request.user = AnonymousUser()
        request.session = {}
        response = user_rays_direct(request)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/auth')


    def test_user_rays_direct(self):
        """Test List of direct rays for a given user
        :todo: this is a kind of stub, enhance it with real fixed_rays users data
        """

        url = '/'
        request = self.factory.get(url)
        request.user = self.user_from
        response = user_rays_direct(request)
        self.assertEquals(response.status_code, 200)

        """Create user->user ray"""


    def test_add_default_rays(self):
        """Check each user has default rays attached
        """
        """Create some direct rays by sending messages"""
        """Send message1"""
        url = '/'
        data = {
          'to': self.user_to.id.id,
          'subject': self.message1['subject'],
          'message_body': self.message1['message_body'],
        }
        request = self.factory.post(url, data, content_type='application/json')
        request.user = self.user_from
        response = rays_send_direct_message(request)
        """Send message2"""
        data = {
          'to': self.user_third.id.id,
          'subject': self.message2['subject'],
          'message_body': self.message2['message_body'],
        }
        request = self.factory.post(url, data, content_type='application/json')
        request.user = self.user_from
        response = rays_send_direct_message(request)
        """Get users rays with defaults added"""
        user = self.user_to
        """Add all possible default messages"""
        rays = add_default_rays(user)
        """Check messages exist"""
        fixed_users = get_fixed_users()
        rays_m_total_count = 0
        for f_id in fixed_users:
          rays_opened = user.rays_dm_recieved.all().filter(user_from__id=f_id).count()
          rays_m_total_count += 1 
          self.assertEqual(rays_opened, 1)
        self.assertEqual(rays_m_total_count, len(fixed_users))


    def test_get_fixed_users(self):
        """Get list of fixed users ids, load them from db,
        check their handles match with those from SETTINGS"""
        fixed_users = get_fixed_users()
        for user_id in fixed_users:
          user = User.objects.filter(pk__exact=user_id).get()
          self.assertTrue(user.handle in self.RAY_SOURCES)


    def test_rays_thread_delete(self):
        """Make sure thread delete not available using GET"""
        logger = logging.getLogger('django.request')
        previous_level = logger.getEffectiveLevel()
        logger.setLevel(logging.ERROR)
        url = '/'
        request = self.factory.get(url)
        request.user = AnonymousUser()
        request.session = {}
        response = rays_thread_delete(request)
        self.assertEquals(response.status_code, 405)
        """Make sure a random dude can not delete a thread"""
        request = self.factory.delete(url)
        request.user = AnonymousUser()
        request.session = {}
        response = rays_thread_delete(request)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/auth')
        """Create a direct message"""
        direct_message = create_direct_message(
          self.user_from,
          self.user_to,
          'sample subject',
          'sample body'
        )
        self.assertFalse(direct_message.message_thread.is_deleted)
        """Attempt to delete it's thread"""
        request = self.factory.delete(url)
        request.user = self.user_from
        response = rays_thread_delete(request, direct_message.message_thread.id)
        message_thread = MessageThread.objects.filter(pk=direct_message.message_thread.id).get()
        logger.setLevel(previous_level)
        self.assertTrue(message_thread.is_deleted)
        """:TODO: make sure only sender/reciever user can delete a thread"""


    def test_rays_thread_archive(self):
        logger = logging.getLogger('django.request')
        previous_level = logger.getEffectiveLevel()
        logger.setLevel(logging.ERROR)
        """Make sure thread archive not available using GET"""
        url = '/'
        request = self.factory.get(url)
        request.user = AnonymousUser()
        request.session = {}
        response = rays_thread_archive(request)
        self.assertEquals(response.status_code, 405)
        """Make sure a random dude can not archive a thread"""
        url = '/'
        request = self.factory.patch(url)
        request.user = AnonymousUser()
        request.session = {}
        response = rays_thread_archive(request)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/auth')
        """Create a direct message"""
        direct_message = create_direct_message(
          self.user_from,
          self.user_to,
          'sample subject',
          'sample body'
        )
        self.assertFalse(direct_message.message_thread.is_deleted)
        """Attempt to archive it's thread"""
        request = self.factory.patch(url)
        request.user = self.user_from
        response = rays_thread_archive(request, direct_message.message_thread.id)
        message_thread = MessageThread.objects.filter(pk=direct_message.message_thread.id).get()
        self.assertTrue(message_thread.is_archived)
        """:TODO: make sure only sender/reciever user can delete a thread"""
        logger.setLevel(previous_level)


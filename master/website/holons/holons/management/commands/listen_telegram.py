import logging
import requests
import json
import praw

from datetime import timezone

from django.core.management.base import BaseCommand
from django.conf import settings

from telethon import TelegramClient, events, sync

from fora.models import ForaChannel



class Command(BaseCommand):
    help = 'Listen to Telegram Channels listed in Fora Channels db table'
    """
    """

    TELEGRAM_API_ID = settings.TELEGRAM_API_ID
    TELEGRAM_API_HASH = settings.TELEGRAM_API_HASH
    MATRIX_MASTER_USER = settings.MATRIX_MASTER_USER
    MATRIX_MASTER_PASSWORD = settings.MATRIX_MASTER_PASSWORD
    MATRIX_URL = 'https://magic1.the.gt/_matrix/client/r0/'
    REDDIT_URL = settings.REDDIT_URL
    REDDIT_OAUTH_URL = settings.REDDIT_OAUTH_URL
    REDDIT_CLIENT_ID = settings.REDDIT_CLIENT_ID
    REDDIT_CLIENT_SECRET = settings.REDDIT_CLIENT_SECRET
    REDDIT_PASSWORD = settings.REDDIT_PASSWORD
    REDDIT_USERNAME = settings.REDDIT_USERNAME
    REDDIT_USER_AGENT = 'HOLONS v.1'

    ENABLE_MATRIX = False
    ENABLE_REDDIT = True

    reddit = None

    def handle(self, *args, **options):
        """
        Call main command logic
        Write command name to the logs

        √ Connect/login to Matrix Synapse Server
             √ Get Matrix Synapse Token

        Connect to the Fora Reddit API

        √ Connect to the given Telegram account
            √ Get all Telegram Dialogs
            √ Filter Telegram Dialogs, match against ForaChannels

            For each matched ForaChannel:
                √ Check for corresponding Matrix Room
                √ Create a new room if it does not exist
                √ Post a message to the room

                Check for corresponding subreddit
                Create a new subreddit if it does not exist
                Post a message to the subreddit




        :param args:
        :param options:
        :return:
        """

        logging.info('I am listen_telegram command v. 1.0')
        logging.info('I write results to stdout')
        logging.info('Telegram API id: ' + str(self.TELEGRAM_API_ID))
        logging.info('Telegram API hash: ' + str(self.TELEGRAM_API_HASH))

        if self.ENABLE_MATRIX:
            logging.info('Connecting to the MATRIX:')
            login_data = {
                "type": "m.login.password",
                "identifier": {
                    "type": "m.id.user",
                    "user": self.MATRIX_MASTER_USER
                },
                "password": self.MATRIX_MASTER_PASSWORD
            }
            url = self.MATRIX_URL + 'login'
            headers = {'Content-type': 'application/json'}
            r = requests.post(url, data=json.dumps(login_data), headers=headers)
            matrix_token = r.json().get('access_token', None)
            logging.info(matrix_token)
            room_creation_url = self.MATRIX_URL + 'createRoom'

        if self.ENABLE_REDDIT:
            self.reddit = praw.Reddit(
                client_id=self.REDDIT_CLIENT_ID,
                client_secret=self.REDDIT_CLIENT_SECRET,
                user_agent=self.REDDIT_USER_AGENT,
                reddit_url=self.REDDIT_URL,
                oauth_url=self.REDDIT_OAUTH_URL,
                password=self.REDDIT_PASSWORD,
                username=self.REDDIT_USERNAME
            )

        client = TelegramClient('fora_listener', api_id=self.TELEGRAM_API_ID, api_hash=self.TELEGRAM_API_HASH)
        client.start()

        dialogs = client.get_dialogs()
        fora_channels = ForaChannel.objects.all()
        for dialog in dialogs:
            for fora_channel in fora_channels:
                if self.ENABLE_MATRIX:
                    self.post_to_matrix(dialog, fora_channel, matrix_token, room_creation_url)
                if self.ENABLE_REDDIT:
                    self.post_to_reddit(dialog, fora_channel)


        # @TODO: rewrite telegram logic to use async/await in production like this
        # with TelegramClient('fora_listener', api_id=self.TELEGRAM_API_ID, api_hash=self.TELEGRAM_API_HASH) as client:
        #     client.start()
        #     client.loop.run_until_complete(client.send_message('me', 'Hello, myself2!'))
        # print(client.download_profile_photo('me'))


    def post_to_matrix(self, dialog, fora_channel, matrix_token, room_creation_url):
        """
        Create Teleport/Matrix room for the channel (get room_id if it's already there)
        Check if message exists in room
        Post message if it doesn't exist

        :param dialog:
        :param fora_channel:
        :param matrix_token:
        :param room_creation_url:
        :return:
        """

        if fora_channel.title == dialog.title:
            logging.info(dialog.name)
            logging.info(dialog.message)
            # create matrix room for a given channel
            room_alias = fora_channel.title.lower().strip().replace(' ', '_')
            room_creation_data = {
                "preset": "public_chat",
                "room_alias_name": room_alias,
                "name": fora_channel.title,
                "topic": "",
                "creation_content": {
                    "m.federate": False
                }
            }
            headers = {'Content-type': 'application/json', 'Authorization': 'Bearer ' + matrix_token}
            r = requests.post(room_creation_url, data=json.dumps(room_creation_data), headers=headers)
            logging.info('Room data: ')
            logging.info(r.json())
            if r.json().get('errcode', False):
                room_by_alias_url = self.MATRIX_URL + 'directory/room/%23' + room_alias + '%3Amagic1.the.gt'
                r = requests.get(room_by_alias_url, headers=headers)

            room_id = r.json().get('room_id', False).replace('!', '%21').replace(':', '%3A')

            timestamp = dialog.message.date.replace(tzinfo=timezone.utc).timestamp()

            message_check_url = self.MATRIX_URL + 'rooms/' + room_id + '/messages?dir=b' + \
                                '&limit=200&filter={\"types\":[\"m.room.message\"]}'
            r = requests.get(message_check_url, headers=headers)
            room_messages = r.json()
            message_exists = False
            if room_messages:
                for message in room_messages.get('chunk', []):
                    message_content = message.get('content', False)
                    if message_content and dialog.message.message == message_content.get('body', ''):
                        message_exists = True
                        continue

            if not message_exists:
                post_message_url = self.MATRIX_URL + 'rooms/' + room_id + '/send/m.room.message/' + str(timestamp)
                message_data = {
                    "body": dialog.message.message,
                    "format": "org.matrix.custom.html",
                    "formatted_body": dialog.message.message.replace('\n\n', '<br>'),
                    "msgtype": "m.text"
                }
                r = requests.put(post_message_url, data=json.dumps(message_data), headers=headers)


    def post_to_reddit(self, dialog, fora_channel):

        # for logger_name in ("praw", "prawcore"):
        #     logger = logging.getLogger(logger_name)
        #     logger.setLevel(logging.DEBUG)
        #     logger.addHandler(handler)

        subreddit_name = fora_channel.title.lower().strip().replace(' ', '_')

        subreddit_name = 'yoyo'

        try:
            subreddit = self.reddit.subreddit.create(
                name=subreddit_name,
                title=fora_channel.title,
                link_type='any',
                subreddit_type='public',
                wikimode='disabled'
            )
        except praw.exceptions.RedditAPIException as error:
            handler = logging.StreamHandler()
            handler.setLevel(logging.DEBUG)
            logging.info('Error: ' + error.message)
            subreddit = self.reddit.subreddits.search_by_name(subreddit_name, False, True)
            submissions = subreddit[0].stream.submissions()
            for submission in submissions:
                logging.info('submission: ')
            #     logging.info(submission)

        pass

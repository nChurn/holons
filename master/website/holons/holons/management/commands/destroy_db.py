import logging

from django.utils.six.moves import input
from django.core.management.base import BaseCommand
from django.conf import settings

from accounts.models import User

class Command(BaseCommand):
    help = 'This will DELETE all data but for grintender and alexb'

    USERS_TO_SAVE = ['alexb', 'grintender']
    USER_IDS_TO_SAVE = [7,8]
    # USERS_TO_SAVE = ['grintender']
    # USER_IDS_TO_SAVE = [8]

    def handle(self, *args, **options):
        """This command will DELETE all data but for grintender and alexb
        It'll ask for the confirmation first
        """

        logging.info('I am data wiper command 1.0')
        logging.info('I destroy all data')
        ok_destroy = self.ask_confirmation()
        if ok_destroy:
          self.wipe_db()

    def ask_confirmation(self):
        """Force user to confirm data wipe"""
        question = 'Do you really want to delete everything in the DB.\nAll USER DATA WILL BE DESTROYED if you answer yes: '
        result = input("%s " % question)
        default = 'n'
        if not result and default is not None:
            return default
        while len(result) < 1 or result[0].lower() not in "yn":
            result = input("Please answer yes or no: ")
        return result[0].lower() == "y"


    def wipe_db(self):
        """Proceed with database wipe
        * Get list of users, excluding users we don't want to wipe
        * Go over all of M2M relations
        * Count each relation
        * Delete all elements of each relation
        * Log deleted count
        * Finally, delete User
        """
        users_list = self.get_all_users()
        for el in users_list:
          logging.info('User:  ' + el.username)
          deleted = {
            'mailboxes': str(self.delete_mailboxes(el)),
            'rays': str(self.delete_rays(el)),
            'rays_direct': str(self.delete_rays_direct(el)),
            'offers': str(self.delete_offers(el)),
            'offers_accepted': str(self.delete_offers_accepted(el)),
            'campaigns': str(self.delete_campaigns(el)),
            'entities': str(self.delete_entities(el)),
            'social': str(self.delete_social(el)),
            'token': str(self.delete_token(el)),
            'invitation_token': str(self.delete_invitation_token(el)),
            'invitation_used': str(self.delete_invitation_used(el)),
          }

          logging.info('\t mailboxes: ' + str(len(el.mailboxes.all())) + ' deleted:' + deleted['mailboxes'])
          logging.info('\t rays: ' + str(len(el.rays.all())))
          logging.info('\t ray_messages: ' + str(len(el.ray_messages.all())) + ' deleted:' + deleted['rays'])
          logging.info('\t rays_direct: ' + str(len(el.rays_direct.all())) + ' deleted:' + deleted['rays_direct'])
          logging.info('\t offers: ' + str(len(el.offers.all())) + ' deleted:' + deleted['offers'])
          logging.info('\t offers_accepted: ' + str(len(el.offers_accepted.all())) + ' deleted:' + deleted['offers'])
          logging.info('\t offers: ' + str(len(el.offers.all())) + ' deleted:' + deleted['offers'])
          logging.info('\t campaigns: ' + str(len(el.campaigns.all())) + ' deleted:' + deleted['campaigns'])
          logging.info('\t entities: ' + str(len(el.entities.all())) + ' deleted:' + deleted['entities'])
          logging.info('\t social: ' + str(len(el.social.all())) + ' deleted:' + deleted['social'])
          logging.info('\t token: ' + el.token + ' deleted:' + deleted['token'])
          logging.info('\t invitation_token: ' + str(len(el.invitation_token.all())) + ' deleted:' + deleted['invitation_token'])
          logging.info('\t invitation_used: ' + str(len(el.invitation_used.all())) + ' deleted:' + deleted['invitation_used'])
          logging.info('')


    def get_all_users(self) -> list:
        """Get all users, exclude those we need to save from extinction"""
        users_list = User.objects\
                                .exclude(id__in=self.USER_IDS_TO_SAVE)\
                                .exclude(username__in=self.USERS_TO_SAVE)\
                                .all()
        return list(users_list)


    def delete_mailboxes(self, el: User) -> int:
        """Receive User object, get list of mailboxes, delete mailboxes, return deleted count
        :return: int: number of mailboxes deleted
        """  
        deleted = el.mailboxes.all().delete()
        return deleted


    def delete_rays_messages(self, el: User) -> int:
        """Receive User object, get list of rays messages, delete rays messages, return deleted count
        :return: int: number of rays messages deleted
        """
        deleted = el.rays_messages.all().delete()
        return deleted


    def delete_rays(self, el: User) -> int:
        """Receive User object, get list of rays, delete rays, return deleted count
        :return: int: number of rays deleted
        """
        deleted = el.rays.all().delete()
        return deleted


    def delete_rays_direct(self, el: User) -> int:
        """Receive User object, get list of direct rays, delete direct rays, return deleted count
        :return: int: number of direct rays deleted
        """
        deleted = el.rays_direct.all().delete()
        return deleted


    def delete_offers_accepted(self, el: User) -> int:
        """Receive User object, get list of offers accepted, delete offers accepted, return deleted count
        :return: int: number of direct offers accepted
        """
        deleted = el.offers_accepted.all().delete()
        return deleted


    def delete_offers(self, el: User) -> int:
        """Receive User object, get list of offers, delete offers, return deleted count
        :return: int: number of direct offers deleted
        """
        deleted = el.offers.all().delete()
        return deleted


    def delete_campaigns(self, el: User) -> int:
        """Receive User object, get list of campaigns, delete campaigns accepted, return deleted count
        :return: int: number of direct campaigns accepted
        """
        deleted = el.campaigns.all().delete()
        return deleted


    def delete_entities(self, el: User) -> int:
        """Receive User object, get list of entities, delete entities, return deleted count
        :return: int: number of direct entities
        """
        deleted = el.entities.all().delete()
        return deleted


    def delete_social(self, el: User) -> int:
        """Receive User object, get list of social elements, delete social elements, return deleted count
        :return: int: number of social elements
        """
        deleted = el.social.all().delete()
        return deleted


    def delete_token(self, el: User) -> int:
        """Receive User object, get token, delete token, return deleted count
        :return: int: number of token deleted (0|1)
        """
        return 0


    def delete_invitation_token(self, el: User) -> int:
        """Receive User object, get list of invitation tokens, delete invitation tokens, return deleted count
        :return: int: number of invitation tokens
        """
        deleted = el.invitation_token.all().delete()
        return deleted


    def delete_invitation_used(self, el: User) -> int:
        """Receive User object, get list of invitation tokens used, delete invitation tokens used, return deleted count
        :return: int: number of invitation tokens used
        """
        deleted = el.invitation_used.all().delete()
        return deleted

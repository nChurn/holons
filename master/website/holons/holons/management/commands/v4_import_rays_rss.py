import feedparser
import hashlib
import logging
import random
import re

from cProfile import Profile
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from django.conf import settings
from django.core.management.base import BaseCommand

from helpers import html_helper
from helpers.num_helper import num

from accounts.models import User
from holons.exceptions import RaysImportException
from rays.models import RaySource
from rays.models import UpworkTalent


MASTER_RAY_PK = settings.MASTER_RAY_PK
MASTER_RAY = RaySource.objects.filter(pk=MASTER_RAY_PK).first()
LOGGING = True


class Command(BaseCommand):
    """Fill up Plato's Flywheel
    Get fresh vacansies from rss feeds
    Store messages to the MASTER_RAY
    For each user having rays store attributed
    messages to the corresponding Plato's Flywheel  Ray

    Note to self, I graph this command like this
    pycallgraph --include="holons.management.commands.*"  \
    graphviz -- ./manage.py import_rays_rss

    """
    
    help = 'Get RaysSettings from the database, parse external RSS feed by url,\
    save contents to the database'


    def _handle(self, *args, **options):
        """
        Call main command logic

        """

        logging.info('I am import_rays_rss command v. 4')
        logging.info('I write results to: talents database')
        if not LOGGING:
            logging.info('Rays import logging DISABLED')
            logging.disable(logging.WARNING)
        # Sync global ray messages
        sync_master_ray()
        # Get all users having RaySource
        users_having_rays = User.objects.filter(rays__isnull=False).distinct()
        # Development time setting, include only one user in production
        '''
        if settings.ENV == 'develop':
          for user in users_having_rays:
              attribute_messages(user)
        else:
        '''
        # debug for a single user
        user = User.objects.get(pk=7)
        attribute_messages(user)
        logging.info('Messages saved, import finished')


    def add_arguments(self, parser):
        parser.add_argument('--profile', action='store_true', default=False)

    def handle(self, *args, **options):
        if options.get('profile', False):
            profiler = Profile()
            profiler.runcall(self._handle, *args, **options)
            profiler.print_stats()
        else:
            self._handle(*args, **options)


def sync_master_ray():
    """Initiate download for each RSS-feed
    :return:
    """

    if LOGGING:
      logging.info('Initiate master ray')
    rss_rays = RaySource.objects.filter(is_active=True).exclude(link__exact='#')
    for ray in rss_rays:
        download_rss_feed(ray)


def download_rss_feed(ray: RaySource):
    """Get Ray's RSS
    For each item in RSS, store message in the DB,

    :param ray:
    :return:
    """

    try:
        rss = feedparser.parse(ray.link)
        save_rss_messages(rss.entries, rss, provider=ray.provider)
    except RaysImportException as err:
        logging.info('Incorrect RSS feed')
        logging.info(err.args)


def save_rss_messages(entries: dict, raw_rss: dict, provider: str = 'upwork') -> int:
    """Save messages to the Master Ray

    :param provider:
    :param entries:
    :param raw_rss:
    :return:
    """

    messages_count = 0
    for item in entries:
        store_ray_message(item, MASTER_RAY, provider)
        messages_count += 1
    return messages_count


def prepare_unsorted_fresh_messages(user: User, timespan_seconds: int = 900) -> list:
    """Get fresh messages from MASTER
    Get or create an ALL ray for the user
    Map messages into [{message: ALL.ray.id}] list
    """
  
    # all_ray = create_uncategorized_user_ray(user)
    messages = []

    raw_msgs = get_fresh_messages_from_master(timespan_seconds)
    for message in raw_msgs:
      # messages.append({'message': message, 'ray_id': all_ray.id})
      messages.append({'message': message, 'ray_id': 0})
    return messages
    

def get_fresh_messages_from_master(timespan_seconds: int = 900) -> list:
    """Select messages from MASTER_RAY based on date
    """

    now = datetime.now(timezone.utc)
    start_time = now - timedelta(seconds=timespan_seconds)
    # :todo: that's a hack to remove cyrilic msgs
    messages = UpworkTalent.objects.filter(ray_source_id=MASTER_RAY_PK)\
              .exclude(provider='habr')\
              .filter(pub_date__range=[start_time, now])
    return list(messages)


def filter_by_budgets(message: UpworkTalent, ray: RaySource) -> dict:
    """Call budget filters
    """

    msg_save = {
      'save_ok': False,
      'message': message,
      }

    budget_ignored = ray.is_budget_empty_ok 
    budget_rate_min = int(ray.budget_rate)
    budget_fixed = int(ray.budget_fixed)
    
    ''' fun with budgets ''' 
    # if no budgets are set, we are ok with any message
    if budget_fixed == 0 and budget_rate_min == 0 and budget_ignored is False:
        msg_save['message'].trace_message += '\n'
        msg_save['message'].trace_message += f'budget filters are not set'
        msg_save['save_ok'] = True
        return msg_save

    # if budget_fixed: exclude messages out of fixed budget 
    if budget_fixed != 0:
        include_msg = filter_by_fixed_budget(budget_fixed, message)
        if include_msg is True:
            msg_save['message'].trace_message += '\n'
            msg_save['message'].trace_message += f'fixed budget: {budget_fixed}, '
            msg_save['message'].trace_message += f'ray title: {ray.title}'
            msg_save['save_ok'] = True
            return msg_save
        else:
            msg_save['save_ok'] = False
    # if budget_rate: exclude messages out of fixed budget 
    if budget_rate_min != 0:
        include_msg = filter_by_budget_rate(budget_rate_min, message)
        if include_msg is True:
            msg_save['message'].trace_message += '\n'
            msg_save['message'].trace_message += f'budget rate: {budget_rate_min}, '
            msg_save['message'].trace_message += f'ray title: {ray.title}'
            msg_save['save_ok'] = True
            return msg_save
        else:
            msg_save['save_ok'] = False
    # if no_budget: include messages with empty budget if needed
    if budget_ignored is True:
        include_msg = filter_by_empty_budget(message)
        if include_msg is True:
            msg_save['message'].trace_message += '\n'
            msg_save['message'].trace_message += f'empty budget, '
            msg_save['message'].trace_message += f'ray title: {ray.title}'
            msg_save['save_ok'] = True
            return msg_save
        else:
            msg_save['save_ok'] = False
    return msg_save
    

def match_message_by_category(message: UpworkTalent, ray: RaySource) -> dict:
    """Check category_filter for single message

    :param category_filter:
    :param message:
    :return:
    """

    if ray.category_filter_list == ['']\
        and ray.skills_filter_list == ['']\
        and ray.title_filter_list == ['']:
        msg_save = {
          'save_ok': True,
          'message': message,
          }
        return msg_save

    msg_save = {
      'save_ok': False,
      'message': message,
      }
    category_haystack = message.category_list
    for category in ray.category_filter_list:
      category_needle = html_helper.sanitize_str(category)
      for single_category in category_haystack:
        single_category = html_helper.sanitize_str(single_category)
        if category_needle.strip() != '' and single_category != '':
          if category_needle.strip() == single_category:
              trace_message = '\n'
              trace_message +=  f'matched category: {category_needle} : '
              trace_message +=  f'{single_category}, ray title: {ray.title}'
              message.trace_message += trace_message
              msg_save['save_ok'] = True
              msg_save['message'] = message
              return msg_save
        else:
              msg_save['save_ok'] = False
              msg_save['message'] = message
            
    return msg_save


def match_message_by_title(message: UpworkTalent, ray: RaySource) -> bool:
    """Match single message by title
    :param title_filter:
    :return:
    """

    title_filter = ray.title_filter_list

    msg_save = {
      'save_ok': False,
      'message': message,
      }
    if ray.title_filter_list == ['']\
        and ray.category_filter_list == ['']\
        and ray.skills_filter_list == ['']:
        msg_save['save_ok'] = True
        return msg_save
    if ray.title_filter_list == ['']:
        msg_save['save_ok'] = False
        return msg_save
    for title_str in title_filter:
        title_needle = html_helper.sanitize_str(title_str)\
                                    .replace('[', '')\
                                    .replace(']', '')
        title_haystack = html_helper.sanitize_str(message.title)\
                                    .replace('[', '')\
                                    .replace(']', '')
        if re.search('(^|\s)' + title_needle + '($|\s)', title_haystack):
            trace_message = '\n'
            trace_message += f'matched title: {title_needle} : '
            trace_message += f'{title_haystack}, ray title: {ray.title}'
            message.trace_message += trace_message
            msg_save['save_ok'] = True
            msg_save['message'] = message
            return msg_save
    return msg_save


def match_message_by_skill(message: UpworkTalent, ray: RaySource) -> dict:
    """Check single message against skills_filter
    Matches exact string
    only works for Upwork provider
    
    :todo: looks too hairy, mabe we could simplify it?

    :param skills_filter:
    :return:
    """

    skills_filter = ray.skills_filter_list
    if ray.category_filter_list == ['']\
        and ray.skills_filter_list == ['']\
        and ray.title_filter_list == ['']:
        msg_save = {
          'save_ok': True,
          'message': message,
          }
        return msg_save

    msg_save = {
      'save_ok': False,
      'message': message,
      }
    if skills_filter != ['']:
        skills = message.skills_list
        for skills_str in skills_filter:
            skills_needle = html_helper.sanitize_str(skills_str)
            for skill in skills:
              if skills_needle == skill.strip():
                  trace_message = '\n'
                  trace_message += f'matched skill: {skills_needle} : '
                  trace_message += f'{skill}, ray title: {ray.title}'
                  message.trace_message += trace_message
                  msg_save['save_ok'] = True
                  msg_save['message'] = message
    return msg_save


def get_country_text(description: str) -> str:
    """Use string methods and trim message to the country only
    :nb: Only works for Upwork
    """

    country = ''
    str_start = description.find('<b>Country')
    str_end = -1
    country = description[str_start:str_end]
    country_trim_pos = country.find('<br')
    country = country[0:country_trim_pos].replace('<b>Country</b>:', '')
    country = html_helper.strip_tags(country)
    return country.lower().strip()


def get_category_text(msg: dict) -> str:
    """Use string methods and trim message to the category only
    :nb: Only works for Upwork
    """

    category = get_category_from_str(msg.description)
    return category


def get_category_from_str(description: str) -> str:
    str_start = description.find('<b>Category')
    str_end = description.find('<b>Skills')
    if str_end < 0:
        str_end = description.find('<b>Country')
    category = description[str_start:str_end]
    category = category.replace('<b>Category</b>:', '').replace('<br />', '')
    category = html_helper.sanitize_str(category)
    return category
    

def get_skills_text(msg: dict) -> str:
    """Use string methods and trim message to get skills
    :nb: Only works for Upwork
    """

    skills = get_skills_from_str(msg.description)
    return skills


def get_skills_from_str(description: str) -> str:
    """Extract skills text from the message
    """

    str_start = description.find('<b>Skills')
    str_end = description.find('<b>Country')
    skills = description[str_start:str_end]
    skills_trim_pos = skills.find('\n')
    skills = skills[0:skills_trim_pos]
    skills = skills.replace('<b>Skills</b>:', '').replace('<br />', '')
    skills = html_helper.sanitize_str(skills)
    return skills


def sanitize_description_text(description: str) -> str:
    """Remove Upwork  description meta, leave only Skills
    """

    str_start = description.find('<b>Skills')
    str_end = description.find('<b>Country')
    skills = description[str_start-1:str_end]
    trim_1 = description.find('<b>Posted On')
    description = description[0:trim_1]
    trim_2 = description.find('<b>Hourly Range')
    description = description[0:trim_2]
    trim_3 = description.find('<b>Budget:')
    description = description[0:trim_3]
    description = description.replace(skills, '')
    return description + skills


def filter_by_country(message: UpworkTalent, ray: RaySource) -> dict:
    """Return msg['save_ok'] = True if message.country is in ray.key_words
    :todo: how extensive is this? Maybe we could do matching inside DB
    """

    if ray.key_words_list == ['']:
        msg_save = {
          'save_ok': True,
          'message': message,
          }
        return msg_save

    msg_save = {
      'save_ok': False,
      'message': message,
      }
    if ray.key_words_list != ['']:
      for needle in ray.key_words_list:
        if needle == message.country_clean:
          msg_save['save_ok'] = True
          trace_message = '\n'
          trace_message += f'geo: {needle}: {message.country_clean}, '
          trace_message += f'ray title: {ray.title}'
          message.trace_message += trace_message
          return msg_save
        else:
          msg_save['save_ok'] = False
    return msg_save


def discard_message_by_stopwords(stop_words: str, message: UpworkTalent) -> dict:
    """
    Get message, return False if it contains any of the stop_words

    :param stop_words:
    :param messages:
    :return:
    """

    if '' == stop_words:
        return message
    include_message = True
    stop_words = stop_words.lower().split(',')
    for needle in stop_words:
        needle = substr.strip().lower()
        haystack = message.description.lower()
        if needle in haystack:
            include_message = False
            return include_message
        else:
            include_message = True
            return include_message
    return include_message


def filter_by_fixed_budget(budget_fixed: int, message: UpworkTalent) -> bool:
    """
    Go over messages, return only the messages having budget >= then the budget_fixed

    :return:
    """

    save_msg = False
    if message.budget is not None and int(message.budget.amount) > budget_fixed:
        save_msg = True
    return save_msg


def filter_by_budget_rate(budget_rate: int, message: UpworkTalent) -> bool:
    """Return True if the message has budget_rate_from >= then the budget_rate_from

    :return:
    """

    save_msg = False
    if message.rate_to is not None and int(message.rate_to.amount) >= int(budget_rate):
        save_msg = True
    return save_msg


def filter_by_empty_budget(message: UpworkTalent) -> bool:
    """Return True if the message hasno budget data

    :return:
    """

    save_msg = False
    if message.budget is None and message.rate_to is None:
        save_msg = True
    return save_msg


def create_uncategorized_user_ray(user: User) -> RaySource:
    """
    Get or create ALL Ray for a given user

    :param user:
    :return:
    """

    title = 'ALL'
    url = '#'
    stop_words = ''
    ray_settings = user.rays.filter(title=title).first()
    if ray_settings is None:
        ray_settings = RaySource.objects.create(
                                                title=title,
                                                link=url,
                                                stop_words=stop_words
                                                )
        ray_settings.save()
        ray_settings.users.add(user)
    return ray_settings


def simple_store_ray_message(item: UpworkTalent, ray: RaySource, ray_all: RaySource):
    """Save message
    Check message existence
    Create message hash


    :param provider:
    :param item:
    :param ray:
    :return:
    """

    item = item.__dict__
    complex_guid = get_message_guid(item, ray)
    if check_message_exists(ray_all, complex_guid) is False:
        summary = item.get('summary', '')
        # trace_message = item.get('trace_message', '')
        # trace_message +=  '\n' + f'message_guid: {complex_guid}'

        talent_record = UpworkTalent.objects.create(
              title = item.get('title', 'No Title'),
              link = item.get('link', ''),
              description = item.get('description', ''),
              ray_source = ray,
              guid = complex_guid,
              provider = item.get('provider', ''),
              country = item.get('country', ''),
              budget = item.get('budget', ''),
              rate_from = item.get('rate_from', None),
              rate_to = item.get('rate_to', ''),
              trace_message = item.get('trace_message', ''),
              category = item.get('category', ''),
              skills = item.get('skills', ''),
        )
        for ray_user in ray.users.all():
            talent_record.users.add(ray_user)
        ray.messages.add(talent_record)


def store_ray_message(item: dict, ray: RaySource, provider: str = 'upwork'):
    """Save message to the MASTER
    Get message budget settings
    Get message existence
    Create message hash


    :param provider:
    :param item:
    :param ray:
    :return:
    """

    complex_guid = get_message_guid(item, ray)
    if check_message_exists_in_master(complex_guid) is False:
        summary = item.get('summary', '')

        # trace_message = ''
        msg_meta = parse_message_description(item)
        country = msg_meta['country']
        budget_fixed = msg_meta['budget_fixed']
        budget_rate_from = msg_meta['budget_rate_from']
        budget_rate_to = msg_meta['budget_rate_to']
        summary = msg_meta['summary']
        trace_message = f'message_guid: {complex_guid}'

        if summary == '':
            summary = item.get('description', '')
        talent_record = UpworkTalent.objects.create(
              title = item.get('title', 'No Title'),
              link = item.get('link', ''),
              trace_message = trace_message,
              description = summary,
              ray_source = ray,
              guid = complex_guid,
              provider = provider,
              country = country,
              budget = budget_fixed,
              rate_from = budget_rate_from,
              rate_to = budget_rate_to,
              category = get_category_from_str(summary),
              skills = get_skills_from_str(summary),
        )
        talent_record.users.add(MASTER_RAY.users.first())
        MASTER_RAY.messages.add(talent_record)


def parse_message_description(item: dict) -> dict:
    """Get dict of Upwork-like message, return a dict with it's meta"""

    description = item.get('summary', '')
    if description == '':
        description = item.get('description', '')
    return {
            'country': get_country_text(description),
            'budget_fixed': get_budget_fixed(description),
            'budget_rate_from': get_budget_rate(description, 'from'),
            'budget_rate_to': get_budget_rate(description, 'to'),
            'summary': description,
            }


def check_message_exists_in_master(complex_guid: str):
    """Make sure the message is unique across all the rays of a given user
    """

    message_exists = UpworkTalent.objects\
                         .filter(ray_source_id=MASTER_RAY_PK)\
                         .filter(guid=complex_guid)\
                         .count()
    if message_exists < 1:
        return False
    return True


def check_message_exists(ray: RaySource, complex_guid: str):
    """Make sure the message is unique across all the rays of a given user
    """

    ray_user = ray.users.first()
    unsorted_ray = ray
    cleanup_unsorted_ray(unsorted_ray, complex_guid)
    message_exists = ray_user.ray_messages\
                         .filter(guid__startswith=complex_guid.split('_')[0])\
                         .count()
    if message_exists < 1:
        return False
    return True


def cleanup_unsorted_ray(ray: RaySource, complex_guid: str):
    """A user might have the message already in ALL ray
    as a result of previous rays processing
    here we delete the message from ALL ray in order to 
    make it available for saving into a normal ray
    """

    message = ray.messages.filter(guid__startswith=complex_guid.split('_')[0])
    message.delete()
    

def get_message_guid(message: dict, ray: RaySource) -> str:
    """Generate message_ray guid or load existing
    """

    if message.get('pub_date', None):
        hash_guid = message.get('guid')
    else:
        h = hashlib.new('md5')
        h.update((message.get('guid', str(random.random())).encode('utf-8')))
        hash_guid = str(h.hexdigest())
    # guid is a fixed length thing, so we hardcode it's length
    complex_guid = hash_guid[0:31] + '_' + str(ray.id)
    return complex_guid


def get_budget_rate(description: str, pos: str = 'from'):
    """
    Parse message body, get Hourly rate, return either first num or second as an int

    :param item:
    :return:
    """

    budget_rate_from = None
    budget_rate_to = None
    str_start = description.find('<b>Hourly Range')
    str_end = description.find('<b>Posted On')
    budget_rate = description[str_start:str_end]
    budget_rate = budget_rate.replace('<b>Hourly Range</b>:', '')\
                              .replace('<br />', '')\
                              .replace('$', '')\
                              .replace(',', '')\
                              .replace('.00', '')
    budget_rate = budget_rate.split('-')
    budget_rate_from = int(num(budget_rate[0].strip()))
    # :todo: Rewrite this spaghetti of returns, get rid of nested ifs
    if pos == 'to' and len(budget_rate) > 1:
      budget_rate_to = int(num(budget_rate[1].strip()))
      if budget_rate_to != 0:
        return budget_rate_to
      else:
        return None
    if budget_rate_from != 0:
      return budget_rate_from
    else:
      return None


def get_budget_fixed(description: str):
    """
    Parse message body, return Fixed budget value as an int

    :param item:
    :return:
    """

    str_start = description.find('<b>Budget')
    str_end = description.find('<b>Posted On')
    budget_rate = description[str_start:str_end]
    budget_rate = budget_rate.replace('<b>Budget</b>:', '')\
                              .replace('<br />', '')\
                              .replace('$', '')\
                              .replace(',', '')
    budget_rate = int(num(budget_rate.strip()))
    if 0 != budget_rate:
      return budget_rate
    else:
      return None


def attribute_messages(user: User):
    """Filtering and sorting of the messages
    """
    
    # Get fresh messages from MASTER
    # Create a list of [message:0]
    messages = prepare_unsorted_fresh_messages(user)
    msg_save = {}
    logging.info(f'Sort messages {user}')
    
    rays = user.rays.filter(is_active=True)\
      .exclude(title__exact='ALL')\
      .exclude(pk=MASTER_RAY_PK)\
      .all()
    ray_all = user.rays.filter(title__exact='ALL')\
      .first()

    # keep only correct countries
    # failed countries go to ALL by default
    for msg in messages:
      trace_message = ''
      for ray in rays:
          msg_save = filter_by_country(msg['message'], ray)
          if msg_save['save_ok'] is True:
              # trace_message += '\n Countries OK'
              # when geography is ok, check budgets
              msg_save = filter_by_budgets(msg['message'], ray)
              if msg_save['save_ok'] is True:
                  # trace_message += '\n Budgets OK'
                  # when budgets are ok:
                  # run category, then skill, then title one after another
                  # don't care if any of them returns False, next one might work
                  # but run additional checks if the filter passes
                  msg_save = match_message_by_category(msg['message'], ray)
                  if msg_save['save_ok'] is True:
                      trace_message += '\n 1. Category OK'
                      trace_message += f' : {ray.id} —  {ray.title}'
                      msg['ray_id'] = ray.id
                      msg_save = match_message_by_skill(msg['message'], ray)
                      # if category is matched, check skills
                      if msg_save['save_ok'] is True:
                          trace_message += '\n 1.1 Category and Skills OK'
                          trace_message += f' : {ray.id} —  {ray.title}'
                          msg['ray_id'] = ray.id
                          # if skill is matched, go for title
                          msg_save = match_message_by_title(msg['message'], ray)
                          if msg_save['save_ok'] is True:
                              trace_message += '\n 1.2 Category, Skills and Title OK'
                              trace_message += f' : {ray.id} —  {ray.title}'
                              msg['ray_id'] = ray.id
                  # if category fails, check skills
                  else:
                    msg_save = match_message_by_skill(msg['message'], ray)
                    if msg_save['save_ok'] is True:
                        trace_message += '\n 2. Skills OK'
                        trace_message += f' : {ray.id} —  {ray.title}'
                        msg['ray_id'] = ray.id
                        # then check title
                        msg_save = match_message_by_title(msg['message'], ray)
                        if msg_save['save_ok'] is True:
                            trace_message += '\n 2.1 Skills and Title OK'
                            trace_message += f' : {ray.id} —  {ray.title}'
                            msg['ray_id'] = ray.id
                        # if skill check fails, once again check title
                        else:
                            trace_message += '\n 2.2 Skills OK'
                            trace_message += f' : {ray.id} —  {ray.title}'
                    else:
                        msg_save = match_message_by_title(msg['message'], ray)
                        if msg_save['save_ok'] is True:
                            trace_message += '\n 3. Title OK'
                            trace_message += f' : {ray.id} —  {ray.title}'
                            msg['ray_id'] = ray.id
                        else:
                            if msg['ray_id'] == 0 and trace_message != '':
                                trace_message += '\n 3.1 Save to ALL'
                                trace_message += f' : {ray.id} —  {ray.title}'
                                msg['ray_id'] = ray_all.id
              else:
                  # failed budgets go to ALL
                  if msg['ray_id'] == 0 and trace_message != '':
                      trace_message += '\n 4. Save to ALL'
                      trace_message += f' : {ray.id} —  {ray.title}, {ray.provider}'
                      msg['ray_id'] = ray_all.id
          # wrong country
          else:
              if msg['ray_id'] == 0:
                  trace_message += '\nWrong country'
                  trace_message += f' : {ray.id} —  {ray.title}, {ray.provider}'

      msg['message'].trace_message = trace_message
      logging.info('=======')
      logging.info(msg)
      logging.info(trace_message)
              

    logging.info(f'End sort messages {user}')

    logging.info(f'Start saving messages {user}')
    for msg in messages:
        if msg['ray_id'] == 0:
            msg['ray_id'] = ray_all.id
        ray = RaySource.objects.filter(pk=msg['ray_id']).get()
        simple_store_ray_message(msg['message'], ray, ray_all)
    logging.info(f'End saving messages {user}')


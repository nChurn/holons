import datetime
import feedparser
import hashlib
import logging
import random
import re
import sys
import time

from contextlib import redirect_stderr
from datetime import datetime, timezone, timedelta
from django.conf import settings
from django.core.management.base import BaseCommand

from accounts.models import User
from helpers import html_helper
import rays.client_stats as client_stats
from rays.models import RaySource
from rays.models import UpworkTalent


MASTER_RAY_PK = settings.MASTER_RAY_PK
MASTER_RAY = RaySource.objects.filter(pk=MASTER_RAY_PK).first()
LOGGING = True
RSS_IMPORT_ON = True

trace_message = ''


class Command(BaseCommand):
    """
    Overall algorithm should look like this:
    
    1) Sync Global Ray
    â€” store all messages locally
    
    FOR EACH USER:    
    2) For each user's ray:
        Go over all FRESH local messages:
            Discard messages including stop_words, GEO and Graph
            Discard same messages already saved in DB
            Check category:
                2.1. Keep matched category messages in RAM
                2.2. Assign the rest on â€œALLâ€ ray

    3) For each Categorized Message
        Go over each users's rays:
            Check Skills
            Store matched Message to the DB
            Discard stored message from RAM

    4) For each of the rest of categorized messages:
        Go over each users's rays:
            Check for Title keywords
            Store matched message

    5) Assign items remaining in RAM based on category 
    """
    
    help = 'Get RaysSettings from the database, parse external RSS feed by url,\
    save contents to the database'


    def handle(self, *args, **options):
        """
        Call main command logic
        Write command name to the logs
        Get all RaySource objects
        Loop through each of them, skip rays not linked to any user
        Call fetch method for each ray-url

        :param args:
        :param options:
        :return:
        """

        logging.info('I am import_rays_rss command v. 3.2')
        logging.info('I write results to: talents database')

        if not LOGGING:
            logging.info('Rays import logging DISABLED')
            logging.disable(logging.CRITICAL)

        # Sync global ray messages
        sync_master_ray()
        # Get all users having RaySource (except the first one?)
        users_having_rays = User.objects.filter(rays__isnull=False).distinct()
        for user in users_having_rays:
            process_rays_for_user(user)


def sync_master_ray():
    """
    Get MASTER_RAY
    Download RSS-feed
    Go over provider-specific rays, download their RSS
    Store each message from the feed

    :return:
    """

    master_ray = MASTER_RAY
    if LOGGING:
      logging.info('Initiate master ray')
    rss_rays = RaySource.objects\
        .filter(is_active=True)\
        .exclude(link__exact='#')\
        .exclude(pk=MASTER_RAY_PK)

    # disable rss if we are debugging
    if RSS_IMPORT_ON:
        download_rss_feed(master_ray)
        for ray in rss_rays:
            download_rss_feed(ray)


def download_rss_feed(ray: RaySource):
    """
    Get Ray's RSS
    For each item in RSS, store message in the DB,

    :param ray:
    :return:
    """

    # :todo: Add exception type here
    rss = feedparser.parse(ray.link)
    save_rss_messages(rss.entries, rss, provider=ray.provider)
    '''
    try:
        rss = feedparser.parse(ray.link)
        save_rss_messages(rss.entries, rss, provider=ray.provider)
    except:
        logging.info('Incorrect RSS feed')
    '''


def save_rss_messages(entries: dict, raw_rss: dict, provider: str = 'upwork') -> int:
    """
    Save messages to the Master Ray

    :param provider:
    :param entries:
    :param raw_rss:
    :return:
    """

    messages_count = 0
    master_ray = MASTER_RAY
    for item in entries:
        messages_count += 1
        store_ray_message(item, master_ray, provider)
        if settings.ENV != 'develop':
           client_stats.store_client_stats(raw_rss, item.get('id'), item)
    return messages_count


def process_rays_for_user(user: User) -> int:
    """
    Get list of user's Rays
    Process RaySettings for each Ray
    Get or create ALL ray for the user
    Get messages for each ray

    :param user:
    :return:
    """

    rays_processed = 0
    uncategorized_ray = create_uncategorized_user_ray(user)
    rays = user.rays.filter(is_active=True)\
            .exclude(pk=MASTER_RAY_PK)\
            .exclude(title='ALL')\
            .all()
    for ray in rays:
        process_ray_messages(ray, uncategorized_ray)
        rays_processed += 1
    # :todo: add ALL ray processing call here
    return rays_processed


def get_fresh_messages_from_master() -> list:
    """Select messages from MASTER_RAY based on date
    """

    now = datetime.now(timezone.utc)
    start_time = now - timedelta(seconds=900)
    messages = UpworkTalent.objects.filter(ray_source_id=MASTER_RAY_PK)\
              .filter(pub_date__range=[start_time, now])
    return list(messages)


def process_ray_messages(ray: RaySource, uncategorized_ray: RaySource, log: bool = LOGGING):
    """
    Get fresh messages from master_ray
    Get stop_words from RaySource
    Get key_words from RaySource
    Get categories_filter
    Get skills_filter
    Get title_filter

    Go over fresh messages, discard messages including any of the stop_words
    Go over messages, select only messages including any of the key_words
    Store remaining messages to self.uncategorized_messages
    Go over uncategorized_messages, check category_filter for each message
       Move matched message to categorized_messages
    Go over uncategorized_messages, store all the messages to the uncategorized_ray
    Go over categorized_messages
       Check each message against skills_filter, store matched to the ray
       Remove matched from the categorized_messages
    Get uncategorized_ray.user.rays
    Go over each of the uncategorized_ray.user's rays
        Go over categorized_messages
            Check each message against uncategorized_ray.user's.ray.title_filter,
            store matched to the uncategorized_ray.user.rays
    Assign each of the remaining categorized_messages to the ray


    :param uncategorized_ray:
    :param ray:
    :return:
    """

    global trace_message
    trace_message = '' 



    log_msg =  f'\n\n======\n{ray.title}: {ray.id} provider: {ray.provider}\n======\n'
    log_msg += f'category_filter {ray.category_filter}\nskills_filter {ray.skills_filter}\n'
    log_msg += f'title_filter {ray.title_filter}\n'
    if not ray.is_budget_empty_ok:
      log_msg += f'budget_rate_min {ray.budget_rate}\nbudget_fixed {ray.budget_rate}\n'
    else:
      log_msg += f'budget_ignored {ray.is_budget_empty_ok}\n\t\n'

    
    messages = get_fresh_messages_from_master()
    messages = preliminary_filter_messages(messages, ray)
    matched = match_messages(messages, ray)

    log_msg += f'\tcategory {len(matched["category_messages"])}\n'
    log_msg += f'\ttitle {len(matched["title_messages"])}\n'
    log_msg += f'\tskills {len(matched["skill_messages"])}\n\tunsorted {len(matched["rest_messages"])}\n'

    for msg in matched['title_messages']:
        store_ray_message(msg, ray, provider=ray.provider)
    for msg in matched['category_messages']:
        store_ray_message(msg, ray, provider=ray.provider)
    for msg in matched['skill_messages']:
        store_ray_message(msg, ray, provider=ray.provider)
    for msg in matched['rest_messages']:
        store_ray_message(msg, uncategorized_ray, provider=ray.provider)
    if log:
        logging.info(log_msg)


def preliminary_filter_messages(messages: list, ray: RaySource) -> list:
    """First step of filtering:
   
    * get rid of messages, containing stop_words
    * include messages containing key_words
    * call budget filters
    """

    budget_ignored = ray.is_budget_empty_ok 
    budget_rate_min = int(ray.budget_rate)
    budget_fixed = int(ray.budget_fixed)

    ''' leave only messages containing key_words '''
    if ray.key_words is not None and ray.key_words != '':
        messages = include_messages_by_keywords(ray.key_words, messages)

    '''remove messages based on key_words '''
    if ray.stop_words is not None and ray.stop_words != '':
        messages = discard_messages_by_stopwords(ray.stop_words, messages)
    
    '''leave only messages with a correct fixed budget '''
    if budget_ignored is False and budget_fixed != 0:
        messages = filter_by_fixed_budget(budget_fixed, messages)

    '''leave only messages with a correct  budget '''
    if budget_ignored is False and budget_rate_min != 0:
        messages = filter_by_budget_rate_from(budget_rate_min, messages)
    return messages
    

def match_messages(messages: list, ray: RaySource) -> dict:
    """Main message matcher logic
    Category -> Skill -> Title matching
    """

    global trace_message
    matched_msgs = {
      'category_messages': [],
      'skill_messages': [],
      'title_messages': [],
      'rest_messages': [],
    }

    for message in messages[:]:
        for category in ray.category_filter_list:
            if '' != category:
                matched = match_message_by_category(category, message)
                if matched is True:
                    trace_message += '\n' + f'matched category {category}'
                    matched_msgs['category_messages'].append(message)
                    messages.remove(message)

    for message in messages[:]:
        matched = match_message_by_skill(ray.skills_filter_list, message)
        if matched is True:
            trace_message += '\n' + f'matched skill {ray.skills_filter}'
            matched_msgs['skill_messages'].append(message)
            messages.remove(message)

    if [''] != ray.title_filter_list:
        for message in messages[:]:
            matched = match_message_by_title(ray.title_filter_list, message)
            if matched is True:
                trace_message += '\n' + f'matched title {ray.title_filter}'
                matched_msgs['title_messages'].append(message)
                messages.remove(message)

        for message in matched_msgs['category_messages'][:]:
            matched = match_message_by_title(ray.title_filter_list, message)
            if matched is True:
                trace_message += '\n' + f'matched title {ray.title_filter}'
                matched_msgs['title_messages'].append(message)
                matched_msgs['category_messages'].remove(message)
        
        for message in matched_msgs['skill_messages'][:]:
            matched = match_message_by_title(ray.category_filter_list, message)
            if matched is True:
                trace_message += '\n' + f'matched title {ray.title_filter}'
                matched_msgs['title_messages'].append(message)
                matched_msgs['skill_messages'].remove(message)
    matched_msgs['rest_messages'] = messages
    return matched_msgs


def match_message_by_category(category_needle: str, message: UpworkTalent) -> bool:
    """Check category_filter for single message

    :param category_filter:
    :param message:
    :return:
    """

    global trace_message
    category_haystack = get_category_text(message)\
              .strip()\
              .replace('&amp;', ' ')\
              .replace('&', ' ')
              
    category_needle = category_needle.strip()\
                      .replace('&amp;', ' ')\
                      .replace('&', ' ')\
                      .lower()

    if re.search('(^|\s)' + category_needle + '($|\s)', category_haystack):
        return True

    return False


def match_message_by_title(title_filter: list, message: UpworkTalent) -> bool:
    """Match single message by title
    :param title_filter:
    :return:
    """

    for title_str in title_filter:
        title_needle = title_str.strip().replace('&amp;', ' ').replace('&', ' ')
        title_haystack = message.title.replace('&amp;', ' ').replace('&', ' ').lower()
        if re.search('(^|\s)' + title_needle + '($|\s)', title_haystack):
            return True

    return False


def match_message_by_skill(skills_filter: list, message: UpworkTalent):
    """Check single message against skills_filter
    Matches exact string
    only works for Upwork provider
    
    :todo: looks too hairy, mabe we could simplify it?

    :param skills_filter:
    :return:
    """

    if skills_filter != ['']:
        skills = get_skills_text(message)\
                  .replace('&amp;', ' ')\
                  .replace('&', ' ')\
                  .split(',')

        skills_clean = []
        for skill in skills:
            skills_clean.append(skill.strip())
        for skills_str in skills_filter:
            skills_needle = skills_str.strip()\
                            .replace('&amp;', ' ')\
                            .replace('&', ' ')\
                            .lower()
            if skills_needle in skills_clean:
                return True

        return False


def get_country_text(msg: dict) -> str:
    """Use string methods and trim message to the country only
    :nb: Only works for Upwork
    """

    country = ''
    str_start = msg.description.find('<b>Country')
    str_end = -1
    country = msg.description[str_start:str_end]
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
    category = html_helper.strip_tags(category)
    return category.lower().strip()
    


def get_skills_text(msg: dict) -> str:
    """Use string methods and trim message to get skills
    :nb: Only works for Upwork
    """

    skills = get_skills_from_str(msg.description)
    return skills


def get_skills_from_str(description: str) -> str:
    str_start = description.find('<b>Skills')
    str_end = description.find('<b>Country')
    skills = description[str_start:str_end]
    skills_trim_pos = skills.find('\n')
    skills = skills[0:skills_trim_pos]
    skills = skills.replace('<b>Skills</b>:', '').replace('<br />', '')
    skills = html_helper.strip_tags(skills)
    skills = skills.replace('\t', '')
    skills = skills.replace('     ', ' ')
    return skills.lower().strip()


def include_messages_by_keywords(key_words: str, messages: list) -> dict:
    """
    Go over messages, store to the RAM messages containing any of the key_words

    :param stop_words:
    :param messages:
    :return:
    """

    if '' == key_words:
        return messages
    included_messages = []
    key_words = key_words.lower().split(',')
    for msg in messages:
        discard_msg = True
        for substr in key_words:
            needle = substr.strip().lower()
            haystack = msg.description.lower()
            if re.search('(^|\s)' + needle + '($|\s)', haystack):
                included_messages.append(msg)
                continue

    return included_messages


def discard_messages_by_stopwords(stop_words: str, messages: list) -> dict:
    """
    Go over messages, store to the RAM messages not containing any of the stop_words

    :param stop_words:
    :param messages:
    :return:
    """

    if '' == stop_words:
        return messages
    included_messages = []
    stop_words = stop_words.lower().split(',')
    for msg in messages:
        discard_msg = False
        for substr in stop_words:
            needle = substr.strip().lower()
            haystack = msg.description.lower()
            if needle in haystack:
                discard_msg = True
        if discard_msg is False:
            included_messages.append(msg)

    return included_messages


def filter_by_fixed_budget(budget_fixed: int, messages: list) -> dict:
    """
    Go over messages, return only the messages having budget >= then the budget_fixed

    :return:
    """

    if budget_fixed == 0:
        return messages
    global trace_message
    included_messages = []
    for msg in messages:
        discard_msg = False
        msg_budget = get_budget_fixed(msg)
        if msg_budget < budget_fixed:
            discard_msg = True
        if discard_msg is False:
            included_messages.append(msg)
            trace_message += '\n' + f'Budget fixed match: {msg_budget}'
            trace_message += f' ray:{budget_fixed}'

    return included_messages


def filter_by_budget_rate_from(budget_rate_from: int, messages: list) -> dict:
    """
    Go over messages,
    return only the messages having budget_rate_from >= then the budget_rate_from

    :return:
    """

    if budget_rate_from == 0:
        return messages
    global trace_message
    included_messages = []
    for msg in messages:
        discard_msg = False
        msg_budget = get_budget_rate(msg)
        if msg_budget < budget_rate_from:
            discard_msg = True
        if discard_msg is False:
            included_messages.append(msg)
            trace_message += '\n' + 'fBudget rate match: {msg_budget}'
            trace_message += f' ray:{budget_rate_from}'

    return included_messages


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
        ray_settings = RaySource.objects.create(title=title, link=url, stop_words=stop_words)
        ray_settings.save()
        ray_settings.users.add(user)
    return ray_settings


def store_ray_message(item: dict, ray: RaySource, provider: str = 'upwork'):
    """Save message
    Check message budget settings
    Check message existence
    Create message hash


    :param provider:
    :param item:
    :param ray:
    :return:
    """

    global trace_message
    country = ''
    budget_fixed = None
    budget_rate_from = None
    budget_rate_to = None

    if isinstance(item, UpworkTalent):
        country = item.country
        item = item.__dict__
    elif isinstance(item, feedparser.util.FeedParserDict):
      if item.get('provider', None) != 'habr':
        country = get_country_text(item)
        budget_fixed = get_budget_fixed(item)
        budget_rate_from = get_budget_rate(item, 'from')
        budget_rate_to = get_budget_rate(item, 'to')

    complex_guid = get_message_guid(item, ray)

    if check_message_exists(ray, complex_guid) is False:
        summary = item.get('summary', '')

        trace_message += '\n' + f'message_guid: {complex_guid}'

        if summary == '':
            summary = item.get('description', '')
        talent_record, created = UpworkTalent.objects.get_or_create(
            title=item.get('title', 'No Title'),
            link=item.get('link', ''),
            trace_message=trace_message,
            description=summary,
            ray_source=ray,
            guid=complex_guid,
            provider=provider,
            country=country,
            budget=budget_fixed,
            rate_from=budget_rate_from,
            rate_to=budget_rate_to,
            category=get_category_from_str(summary),
            skills=get_skills_from_str(summary),
        )
        for ray_user in ray.users.all():
            talent_record.users.add(ray_user)
        ray.messages.add(talent_record)
        trace_message = ''


def check_message_exists(ray: RaySource, complex_guid: str):
    """Make sure the message is unique across all the rays of a given user
    """

    if ray.id != MASTER_RAY_PK:
        ray_user = ray.users.first()
        unsorted_ray = ray_user.rays.filter(title='ALL').first()
        cleanup_unsorted_ray(unsorted_ray, complex_guid)
        message_exists = len(ray_user.ray_messages
                             .exclude(ray_source_id=MASTER_RAY_PK)
                             # .exclude(ray_source_id=unsorted_ray.pk)
                             .filter(guid__startswith=complex_guid.split('_')[0])
                            )
    else:
        message_exists = len(UpworkTalent.objects
                             .filter(ray_source_id=MASTER_RAY_PK)
                             .filter(guid=complex_guid)
                            )
    if message_exists < 1:
        return False
    return True


def cleanup_unsorted_ray(unsorted_ray: RaySource, complex_guid: str):
    """A user might have the message already in ALL ray
    as a result of previous rays processing
    here we delete the message from ALL ray in order to 
    make it available for saving into a normal ray
    """

    message = unsorted_ray.messages.filter(guid__startswith=complex_guid.split('_')[0])
    message.delete()
    

def get_message_guid(message: dict, ray: RaySource) -> str:
    """Generate message_ray guid or load existing
    """

    if not message.get('pub_date', None):
        h = hashlib.new('md5')
        h.update((message.get('guid', str(random.random())).encode('utf-8')))
        hash_guid = str(h.hexdigest())
    else:
        hash_guid = message.get('guid')
    str_start = hash_guid.find('_')
    complex_guid = hash_guid[0:str_start] + '_' + str(ray.id)
    return complex_guid


def get_budget_rate(item: dict, pos: str = 'from'):
    """
    Parse message body, get Hourly rate, return either first num or second as an int

    :param item:
    :return:
    """

    budget_rate_from = None
    budget_rate_to = None
    if isinstance(item, UpworkTalent):
        item = item.__dict__

    str_start = item['description'].find('<b>Hourly Range')
    str_end = item['description'].find('<b>Posted On')
    budget_rate = item['description'][str_start:str_end]
    budget_rate = budget_rate.replace('<b>Hourly Range</b>:', '').replace('<br />', '').replace('$', '')
    budget_rate = budget_rate.split('-')
    budget_rate_from = int(num(budget_rate[0].replace('.00', '').strip()))
    # :todo: Rewrite rhis spaghetti of returns, get rid of nested ifs
    if pos == 'to' and len(budget_rate) > 1:
      budget_rate_to = int(num(budget_rate[1].replace('.00', '').strip()))
      if budget_rate_to != 0:
        return budget_rate_to
      else:
        return None

    if budget_rate_from != 0:
      return budget_rate_from
    else:
      return None


def get_budget_fixed(item):
    """
    Parse message body, return Fixed budget value as an int

    :param item:
    :return:
    """

    if isinstance(item, UpworkTalent):
        item = item.__dict__
    str_start = item['description'].find('<b>Budget')
    str_end = item['description'].find('<b>Posted On')
    budget_rate = item['description'][str_start:str_end]
    budget_rate = budget_rate.replace('<b>Budget</b>:', '').replace('<br />', '').replace('$', '')
    budget_rate = int(num(budget_rate.strip()))
    if 0 != budget_rate:
      return budget_rate
    else:
      return None


def num(s):
    """
    Utility unction
    takes a string, returns int/zero

    :param s:
    :return:
    """
    s = s.split('.')[0]
    try:
        return int(s)
    except ValueError:
        return 0


import string
import random
import logging

from django.conf import settings


def token_generate(
    size: int = 24,
    chars: str = (string.ascii_lowercase + string.digits),
    delimiter: str = '',
    chars_in_group: int = 6
  ) -> str:
  """
  Get number of chars/digits, and create custom grouped and delimited random token

  """

  random_str = ''.join(
    random.choice(chars) for _ in range(size)
  )

  token = delimiter.join(
    random_str[i:i+chars_in_group] for i in range(0, size, chars_in_group)
  )

  return token

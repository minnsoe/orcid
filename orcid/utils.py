# standard library
from collections import namedtuple


Tokens = namedtuple('Tokens',
                    ['access','refresh', 'expires_in', 'timestamp'])

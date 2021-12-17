import string
import random
import datetime
import json
from decimal import Decimal
from uuid import UUID


def is_valid_uuid(val):
    try:
        return UUID(str(val))
    except ValueError:
        return None


def convertSatangToBaht(satang):
    return '{0:.02f}'.format(float(satang) / 100.0)


def random_id(size=20, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    # log.info("call random id:")
    return ''.join(random.choice(chars) for _ in range(size))


def create_ref(size=20, chars=string.ascii_uppercase + string.digits):
    # log.info("call random id:")
    return ''.join(random.choice(chars) for _ in range(size))


"""Serialize Python dates and decimals in JSON."""


class _DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o.quantize(Decimal("1.00")))

        if isinstance(o, datetime.datetime):
            return str(o.isoformat())

        return super(_DecimalEncoder, self).default(o)


def _fix_data(o):
    if isinstance(o, Decimal):
        return str(o.quantize(Decimal("1.00")))

    if isinstance(o, datetime.datetime):
        return str(o.isoformat())

    if isinstance(o, UUID):
        return str(o)

    return o

# def fix_json_data(obj):
#     """Fixed Python dictionary data in-place to be JSON serializable.

#     Converts decimals and datetimes to string presentation.

#     :param obj: List or Dictionary
#     """
#     return dictutil.traverse(obj, _fix_data)

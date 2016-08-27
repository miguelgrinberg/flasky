# -*- coding: utf-8 -*-

from enum import Enum
from flask import jsonify, request
from . import app

UPLOAD_SIZE = 2 ** 24  # the maximum size of uploaded pictures
TOKEN_TIME_OUT_MIN = 1000000  # token lifetime
CODE_TIME_OUT_SEC = 300  # validation code lifetime
ADJOIN_BOOK_SPACE_SECONDS = 30*60  # protection space between two adjoin bookings
CARD_CHARGE_DURATION_SECONDS = 6*60*60  # maximum length of charging by owner card
ADMIN_USER = 'admin'  # admin login user name
ADMIN_PASS = 'admin123'  # admin login password

FLASKY_POSTS_PER_PAGE = 12 #page size


class BookStatus(Enum):
    NPAID = 0  # Guest Not Paid
    PAID = 1  # Guest Paid
    ACCEPT = 2  # Pile Owner Accept
    DECLINE = 3  # Pile Owner Decline
    CHARGING = 4  # Guest Start Charging
    COMPLETE = 5  # Guest Complete Charging
    OVERDUE = 6
    CANCEL = 7 # Guest cancel the book before charging


class SettingKey(Enum):
    SMS_ACCOUNT = 0
    SMS_PASSWORD = 1
    VERSION = 2


class TransType(Enum):
    TOPUP = 0
    WITHDRAW = 1
    PAY = 2
    RECEIVE = 3


class TransStatue(Enum):
    PENDING = 0
    SUCCESS = 1
    FAIL = 2


class TransUsage(Enum):
    APPOINTMENT = 0
    SERVICE = 1
    COMMISSION = 2


class ErrNo(Enum):
    OK = 0  # Success
    PARAM = 1  # Parameter invalid, lost, etc
    DB = 2  # Database operation failure
    DUP = 3  # Duplicate key, i.e. user name used, mobile phone registered, etc.
    NOID = 4  # No record, i.e. user, book not exists
    INACT = 5  # Inactive user

    PASSWD = 6  # Password incorrect
    TOKEN = 7  # Token incorrect
    TIMEOUT = 8  # Timeout
    NOAUTH = 9  # No authority
    BIG = 10  # Uploaded file exceeds the size limit

    SMS = 11  # Failed to send SMS
    INVALID = 12  # Invalid verification code/book time slot ...
    MNS = 13  # Failed to send MNS message
    NOMONEY = 14  # Insufficent money


def result(errno, **msgs):
    if app.debug:
        return jsonify(ret=errno.value, request_url=request.url, **msgs)
        # return jsonify(ret=errno.value, request=request.data, request_url=request.url, **msgs)
    return jsonify(ret=errno.value, **msgs)



#define authorization
class Permission:
    USER = 'user'
    MERCHANT = 'merchant'
    MAINTAINER = 'maintainer'
    ADMIN = 'admin'

#define no permission message
def permissionDenied(msg="permission denied"):
    return jsonify({
        'success': False,
        'msg': msg
    })
import os
import configparser

basedir = os.path.abspath(os.path.dirname(__file__))
configp = configparser.RawConfigParser()
configp.read(os.path.expanduser('~/.hh-farms.cfg'))

SECRET_KEY = 'SECRET STUFF'  # configp['site']['secretkey'] or 'hard to guess stuff'
MAIL_SUBJECT_PREFIX = '[HH-Farms]'
MAIL_SENDER = 'HH-Farms Admin <admin@hh-farms.com>'
FARM_ADMIN = 'mhilema@gmail.com'
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = "user"  # configp['mail']['username']
MAIL_PASSWORD = "pass"  # configp['mail']['password']

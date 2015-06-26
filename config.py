import os
import configparser

basedir = os.path.abspath(os.path.dirname(__file__))
configp = configparser.RawConfigParser()
configp.read(os.path.expanduser('~/.hhfarms.cfg'))

SECRET_KEY = configp['site']['secretkey'] or 'hard to guess stuff'
MAIL_SUBJECT_PREFIX = '[HH-Farms]'
MAIL_USERNAME = configp['mail']['username']
MAIL_PASSWORD = configp['mail']['password']
MAIL_SENDER = 'HH-Farms Admin <admin@hh-farms.com>'
FARM_ADMIN = 'mhilema@gmail.com'
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
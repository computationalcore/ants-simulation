"""
   Load configuration file into configparser object.
"""
import os
import ConfigParser

dir_name = os.path.abspath(os.path.dirname(__file__))

config = ConfigParser.RawConfigParser()
config.read( 'app.cfg')

ANT_COUNT = config.getint('general', 'ants')
SCREEN_SIZE = (config.getint('general', 'screen_size_x'), config.getint('general', 'screen_size_y'))
NEST_POSITION = (config.getint('nest', 'position_x'), config.getint('nest', 'position_y'))
NEST_SIZE = config.getfloat('nest', 'size')
SPIDER_HEALTH = config.getint('general', 'spider_health')
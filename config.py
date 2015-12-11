"""
   Load configuration file into configparser object.
"""
import os
import ConfigParser

dir_name = os.path.abspath(os.path.dirname(__file__))

config = ConfigParser.ConfigParser()
config.read(os.path.join(dir_name, 'app.cfg'))
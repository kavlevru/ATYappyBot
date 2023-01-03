import requests
from config import load_conf


class Jira(object):


    def __int__(self):
        self.config = load_conf()
        self.url = self.config.JIRA_URL


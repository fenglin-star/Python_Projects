# coding=utf-8

# coding=utf-8
from python_def.config import *
import requests
from bs4 import BeautifulSoup
from python_def.caiyun import *
from python_def.Mysqldb_server import mysql_url,read_mysql
from python_def.WordPress import wordpress_artice
from multiprocessing import Pool
from requests.adapters import HTTPAdapter
from zhconv import convert
import redis
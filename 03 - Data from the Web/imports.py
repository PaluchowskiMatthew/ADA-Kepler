# We are going to use requests to do the HTTP-calls for gathering data, and BeautifulSoup for parsing the 
# HTML that we recieve
import requests
from bs4 import BeautifulSoup

# re will help us parse the html by using regular expressions
import re

# Furthermore, we will use the normal stack of pandas, numpy, matplotlib and seaborn
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Statistical test library
import scipy.stats as stats
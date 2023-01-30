from login import Login
from apiScraper import ApiScraper
import yaml

with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

user = config['user']
pswd = config['password']
auth = Login(user, pswd)
auth.getAuth()
scraper = ApiScraper(auth.cacheGuid, auth.token)
print(scraper.get_positions())
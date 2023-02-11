from login import Login
from apiScraper import ApiScraper
import yaml

def represent_none(self, _):
    return self.represent_scalar('tag:yaml.org,2002:null', '')

yaml.add_representer(type(None), represent_none)

with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)

auth = Login(config['authentication'])
auth.getAuth()

config['authentication']['token'] = auth.token
config['authentication']['cacheGuid'] = auth.cacheGuid
with open('config.yml', 'w') as file:
    yaml.dump(config, file)

scraper = ApiScraper(config['authentication']['cacheGuid'], config['authentication']['token'])

# print(scraper.get_positions(config['positions']['date']))
# scraper.get_hist_positions(
#     config['historicalPositions']['dateStart'],
#     config['historicalPositions']['dateEnd'],
#     config['historicalPositions']['freq'],
#     config['historicalPositions']['write']
# )
# scraper.get_earnings(
#     config['historicalPositions']['dateStart'],
#     config['historicalPositions']['dateEnd'],
#     config['historicalPositions']['write']
# )
scraper.get_trades(
    config['historicalPositions']['dateStart'],
    config['historicalPositions']['dateEnd'],
    config['historicalPositions']['write']
)
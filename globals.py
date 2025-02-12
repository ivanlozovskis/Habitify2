from datetime import datetime
import json
from datetime import datetime

with open("config.json", "r") as file:
    config = json.load(file)['database']





date_freeze = datetime.strptime(config['freeze_time'], "%Y-%m-%d %H:%M:%S")

print(config['freeze_time'])


CURRENT_MONTH = datetime.now().month if config['freeze'] == 0 else date_freeze.month
CURRENT_YEAR = datetime.now().year if config['freeze'] == 0 else date_freeze.year ###CRYR
CURRENT_YEAR1 = datetime.now().year if config['freeze'] == 0 else date_freeze.year###CURRENT_YEAR
YEAR_MONTH = datetime.now().strftime("%Y-%m") if config['freeze'] == 0 else date_freeze.strftime("%Y-%m")
CONT_MONTH = 0

YEAR_LABEL = 0
BTN_LEFT = 0
BTN_RIGHT = 0

MONTH_LABEL = 0
MBTN_RIGHT = 0
MBTN_LEFT = 0



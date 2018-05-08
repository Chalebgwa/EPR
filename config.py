from  datetime import datetime,timedelta

from bottle import Bottle
from models import *
app=Bottle()
SECRET_KEY="@ug/!5i43nhhtvowszAJF"
TOKEN_TIME = datetime.utcnow() + timedelta(hours=1)
REQUIRE_PERMISSION=[GP]
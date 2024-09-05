from django_neomodel import DjangoNode
from neomodel import (
    StringProperty,
    UniqueIdProperty,
    EmailProperty,
    IntegerProperty,
    DateTimeProperty
)
from datetime import datetime, timedelta
import pytz

class Interview(DjangoNode):
    uid = UniqueIdProperty()
    question = StringProperty(default="None")
    answer = StringProperty(default="None")
    user = StringProperty(default="None")

    def __str__(self):
        return self.username

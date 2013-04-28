from datetime import date, timedelta
from collections import Counter

from messaging.models import Message


class Stats(object):
    def __init__(self, user):
        self.user = user

    def get_query_set(self):
        return Message.objects.filter(user=self.user)

    def monthly(self):
        today = date.today() + timedelta(days=1)
        month_ago = today - timedelta(days=31)

        qs = self.get_query_set()

        messages = qs.filter(date_sent__gt=month_ago,
                             date_sent__lt=today)

        counted = Counter([x.date_sent.date() for x in messages])

        monthly = []

        for day in [month_ago + timedelta(days=i) for i in range(31)]:
            monthly.append([day, counted[day]])

        return monthly

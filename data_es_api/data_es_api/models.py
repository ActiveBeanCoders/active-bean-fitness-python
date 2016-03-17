from data_all_api.models import Activity


class ActivityEsFields:
    id = 'id'
    activity = 'activity'
    comment = 'comment'
    date = 'date'
    distHour = 'distHour'
    distMin = 'distMin'
    distSec = 'distSec'
    distance = 'distance'
    unit = 'unit'
    userId = 'userId'


class ActivityEs(Activity):
    def save(self, *args, **kwargs):
        # TODO save
        print("TODO save")



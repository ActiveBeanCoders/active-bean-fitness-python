class ActivityEsFields:
    id = 'id'
    activity = 'activity'
    comment = 'comment'
    date = 'date'
    dist_hour = 'distHour'
    dist_min = 'distMin'
    dist_sec = 'distSec'
    distance = 'distance'
    unit = 'unit'
    user_id = 'userId'
    alltext = 'alltext'


class ActivityEs:
    id = -1
    activity = None
    comment = None
    date = None
    dist_hour = None
    dist_min = None
    dist_sec = None
    distance = None
    unit = None
    user_id = None
    alltext = None

    def __str__(self):
        return str(self.id) + ': ' + self.activity + ' ' + str(self.distance) + ' ' + self.unit + ' on ' + str(
                self.date)


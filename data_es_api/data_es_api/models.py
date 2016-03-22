from data_all_api.models import Activity


class ActivityEsFields:
    id = 'id'
    activity = 'activity'
    comment = 'comment'
    date = 'date'
    dist_hour = 'dist_hour'
    dist_min = 'dist_min'
    dist_sec = 'dist_sec'
    distance = 'distance'
    unit = 'unit'
    user_id = 'user_id'


class ActivityEs(Activity):
    def save(self, *args, **kwargs):
        # TODO save
        print("TODO save")

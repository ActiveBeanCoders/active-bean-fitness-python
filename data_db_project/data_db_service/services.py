from data_all_api.models import Activity
import threading


# TODO: move this to common location
def synchronized(func):
    func.__lock__ = threading.Lock()

    def synced_func(*args, **kws):
        with func.__lock__:
            return func(*args, **kws)

    return synced_func


class ActivityService:
    max_doc_id = -1

    def get(self, doc_id):
        return Activity.objects.get(id=int(doc_id))

    def add(self, activity):
        # if ID is missing, assign it
        if not hasattr(activity, 'id'):
            activity.id = self.next_id()
        activity.save()

    def recent(self, count):
        if count is None or int(count) <= 0:
            count = 10
        return Activity.objects.order_by('-date')[:int(count)]

    def search(self, criteria):
        # get the full text search criterion
        full_text = criteria['simple_criteria']['fullText']

        # use the criterion to get search results
        return Activity.objects.filter(alltext__contains=full_text)

    def max_id(self):
        return Activity.objects.latest('id').id

    # TODO: this is a bottleneck.  Need to get around this somehow.
    @synchronized
    def next_id(self):
        if self.max_doc_id < 0:
            self.max_doc_id = self.max_id()
        self.max_doc_id += 1
        return self.max_doc_id


activity_service = ActivityService()

import operator

class Event(object):

    def __init__(self, first_come, time, block):
        self.first_come = first_come
        self.time = time
        self.block = block

class Queue:
    event_list=[] # this is where future events will be stored
    def add_event(event):
        Queue.event_list += [event]
    def remove_event(event):
        del Queue.event_list[0]
    def get_next_event():
        Queue.event_list.sort(key=operator.attrgetter('time'), reverse=False) # sort events -> earliest one first
        return Queue.event_list[0]
    def size():
        return len(Queue.event_list)
    def isEmpty():
        return len(Queue.event_list) == 0
    def clear(self):
        self.event_list = []
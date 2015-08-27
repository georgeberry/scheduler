import datetime, sqlite3, argparse, json
'''
interface with events through the event name

the elegance here:
    dump a bunch of events in and it schedules for you
    schedules stuff you don't want to do first, to get it out of the way

todo:
Preferences
Google calendar integration
Summary output

simple json file logging right now
'''


#file locations

all_events_path = 'data/all_events.json'
active_events_path = 'data/active_events.json'
preferences_path = 'data/preferences.json'


#parser

parser = argparse.ArgumentParser(description='Schedule your tasks')

#add/delete events
parser.add_argument('-a', '--add', nargs='+', help='add events separated by ^')
parser.add_argument('-f', '--finish', nargs='+')

#diagnostics
parser.add_argument('-p', '--preferences')
parser.add_argument('-l', '--list') #list all

#summarize
parser.add_argument('-t', '--today')
parser.add_argument('-w', '--week')
parser.add_argument('-m', '--month')


#class

class Event:
    def __init__(self, name, duration, start_time, due_date, recurrence, category, desire):
        self.name = name
        self.duration = duration
        self.start_time = start_time
        self.due_date = due_date
        self.recurrence = recurrence
        self.category = category
        self.desire = desire

    def as_dict(self):
        d = {
            'name': self.name,
            'duration': self.duration,
            'start time': self.start_time,
            'due date': self.due_date,
            'recurrence': self.recurrence,
            'category': self.category,
            'desire': self.desire
        }
        return d

    def __str__(self):
        '''
        This will be printed for the user
        '''
        pass


#functions

def load_json_file(filepath):
    try:
        with open(filepath, 'rb') as f:
            return json.load(f)
    except Exception as e:
        print e
        with open(filepath, 'wb') as f:
            f.write(json.dumps({}))
            print('created file')
        return {}


def save_json_file(data, filepath):
    with open(filepath, 'wb') as f:
        f.write(json.dumps(data))


def gather_arguments(arg_list):
    args = []

    whole_arg = ''
    for arg in arg_list:
        if arg != '^':
            whole_arg += arg + ' '
        else:
            args.append(whole_arg.strip())
            whole_arg = ''

    if whole_arg != '':
        args.append(whole_arg.strip())

    return args


def create_event(name):
    duration = raw_input('How many hours do you estimate {} will take? '.format(name))
    start_time = raw_input('Does {} have a defined start time? '.format(name))
    due_date = raw_input('Does {} have a due date? '.format(name))
    recurrence = raw_input('What days of the week does {} recur on? '.format(name))
    category = raw_input('Does {} belong to a larger project? '.format(name))
    desire = raw_input('From 1-10, how much do you want to do {}?'.format(name))

    event = Event(name, duration, start_time, due_date, recurrence, category, desire).as_dict()

    return event


def add_event(event, all_events, active_events):
    name = event['name']
    if name not in all_events:
        all_events[name] = event
        print('Success at inserting {} into all_events!'.format(name))
    else:
        print('Event {} already exists!'.format(name))
    if name not in active_events:
        active_events[name] = event
        print('Success at inserting {} into active_events!'.format(name))
    else:
        print('Event {} already exists!'.format(name))


def finish_event(name, active_events):
    if name in active_events:
        active_events.pop(name)
        print('Success!')
    else:
        print('Event {} is not active!'.format(name))


def list_active(active_events):
    for event in active_events:
        print(Event(event))


if __name__ == '__main__':
    parsed_arguments = parser.parse_args()
    all_events = load_json_file(all_events_path)
    active_events = load_json_file(active_events_path)

    print parsed_arguments.add

    if parsed_arguments.add:
        to_add = gather_arguments(parsed_arguments.add)
        print to_add
        for arg in to_add:
            event = create_event(arg)
            add_event(event, all_events, active_events)



    if parsed_arguments.finish:
        pass
    if parsed_arguments.list:
        pass
    if parsed_arguments.month:
        pass
    if parsed_arguments.today:
        pass
    if parsed_arguments.week:
        pass

    save_json_file(all_events, all_events_path)
    save_json_file(active_events, active_events_path)

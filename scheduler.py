#!/usr/local/bin/python3
import argparse
import sqlite3
import datetime
import json

"""
Command line task scheduler

Argparse (and subclases) should get inputs ready to user

Flags:
    --start -s: task start time, takes datetime and converts to unix
    --end -e: task end time, takes datetime and converts to unix
    --repeat -r: daily, weekly, monthly, yearly
    --name -n: unique name for task
    --list -l: print tasks to command line in order of start time

Stretch goals:
    1) Pretty print
    2) Google Calendar integration via API
    3) Collab

~

Can we add support for: "today", "this" and "next". i.e. this monday

Can we use a symbol to separate date and time
I.e. 'this monday; 12:00'
"""
# sqlite3 class

class SQLHandler:
    """
    Creates table, manages SQLite connection
    """
    def __init__(
        self,
        dbpath='/Users/g/Google Drive/independent-work/scheduler/testdb.db'
    ):
        self.conn = sqlite3.connect(dbpath)

    def execute(self, query, args=None):
        c = self.conn.cursor()
        if args:
            c.execute(query, args)
        else:
            c.execute(query)
        self.conn.commit()

    def create_table(self):
        schema = """
            CREATE TABLE tasks (
                name text,
                start timestamp,
                end timestamp
            )
        """
        self.execute(schema)

    def insert_row(self, name, start, end):
        args = (name, start, end)
        query = """
            INSERT INTO tasks VALUES (
                ?,
                ?,
                ?
            )
        """
        self.execute(query, args)

    def remove_rows(self, name):
        args = (name,) # godda be a tuple
        query = """
            DELETE FROM tasks
            WHERE name=?
        """
        self.execute(query, (name,))

    def print_table(self):
        c = self.conn.cursor()
        for row in c.execute('SELECT * FROM tasks'):
            print(row)
        self.conn.close()

# wrap sql stuff in functions
def add_to_table(args):
    s = SQLHandler()
    s.insert_row(
        args.name[0],
        args.start[0],
        args.end[0],
    )

def print_table(args):
    s = SQLHandler()
    s.print_table()

def create_table():
    pass

def delete_table():
    pass

def remove_from_table(args):
    s = SQLHandler()
    s.remove_rows(
        args.name[0],
    )

# argparse stuff

class ParseDateAction(argparse.Action):
    def __call__(self, parser, namespace, value, option_string=None):
        date_value = self.date_parse(value)
        setattr(namespace, self.dest, date_value)

    @staticmethod
    def date_parse(date_string):
        # todo: date parsing goes here
        return date_string

parser = argparse.ArgumentParser(
    description='Command line task scheduler'
)

subparsers = parser.add_subparsers(help='sub-command help')

# add task stuff

parser_add = subparsers.add_parser('add', help='create')
parser_add.add_argument(
    '--name', '-n',
    type=str,
    nargs=1,
    metavar='N',
    help='Task name.'
)
parser_add.add_argument(
    '--start', '-s',
    type=str,
    nargs=1,
    action=ParseDateAction,
    metavar='YY-MM-DD-HH',
    help='Start time of task in YY-MM-DD-HH format.'
)
parser_add.add_argument(
    '--end', '-e',
    type=str,
    nargs=1,
    action=ParseDateAction,
    metavar='YY-MM-DD-HH',
    help='End time of task in YY-MM-DD-HH format.'
)
parser_add.add_argument(
    '--repeat', '-r',
    type=str,
    choices=['daily', 'weekly', 'monthly', 'yearly'],
    nargs=1,
    metavar='FREQ',
    help='How often to repeat the task. Choose from: daily, weekly, monthly, yearly. If no --occ -o flag is specified, assumes 7 repeats.',
)
parser_add.add_argument(
    '--occ', '-o',
    type=int,
    nargs=1,
    default=1,
    metavar='OCC',
    help='How many repeat occurrences. Defaults to 1. Ignored if no --repeat -r flag is specified.'
)
parser_add.set_defaults(func=add_to_table)

# remove task

parser_rm = subparsers.add_parser('rm', help='delete help')
parser_rm.add_argument(
    '--name', '-n',
    type=str,
    nargs=1,
    metavar='N',
    help='Task name.'
)
parser_rm.set_defaults(func=remove_from_table)

# print upcoming stuff

parser_list = subparsers.add_parser('list', help='list help')
parser_list.set_defaults(func=print_table)

if __name__ == '__main__':
    args = parser.parse_args()
    # route everything through the default function for the subparser
    args.func(args)

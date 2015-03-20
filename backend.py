#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''D-Logger - backend module
'''

from __future__ import with_statement, division, absolute_import, print_function

import os
import re
#import time
from datetime import datetime, timedelta
from glob import glob

import pytz
try:
    import simplejson as json
except ImportError:
    import json


DATE_FMT = '%Y-%m-%d'
TIME_FMT = '%H:%M:%S%z'
ITEM_DATETIME_FMT = DATE_FMT + ' ' + TIME_FMT
BREAK_ITEM = '*BREAK*'
LOG_NAME_TIME_FMT = TIME_FMT.replace(':', '')
LOG_NAME_FMT = 'dlogger_' + DATE_FMT + '_' + LOG_NAME_TIME_FMT + '.dlog'

SLUG_RE = re.compile(r'[^-._0-9A-Za-z]+')


def get_now_time():
    '''Returns current UTC datetime
    '''
    return datetime.now(tz=pytz.utc)


def get_dt_str_by_fmt(log_name_fmt, dt_obj=None):
    '''Generates formatted date/time string
    '''
    return (dt_obj or get_now_time()).strftime(log_name_fmt)


def get_last_log_name():
    '''Gets the last log name
    '''
    # any same day logs?
    fn_mask = get_dt_str_by_fmt(LOG_NAME_FMT.replace(LOG_NAME_TIME_FMT, '*'))
    filenames = glob(fn_mask)
    if filenames:
        return (filenames[-1], True)
    # just any logs?
    fn_mask = LOG_NAME_FMT.replace(DATE_FMT, '*').replace(LOG_NAME_TIME_FMT,
        '*')
    filenames = sorted(glob(fn_mask))
    if filenames:
        return (filenames[-1], False)
    # no logs...
    return (get_dt_str_by_fmt(LOG_NAME_FMT), False)


def read_log_data(log_name, mode):
    '''Reads JSON log
    '''
    with open(log_name, mode) as fd_obj:
        line = True
        while line:
            line = fd_obj.readline()
            str_line = line.strip()
            if str_line:
                yield json.loads(str_line)


def get_label_slug(label):
    '''Gets label's slug
    '''
    return SLUG_RE.sub('', label)


def parse_items(json_data):
    '''Parses log data
    '''
    items = []
    slugs = []
    for item in json_data:
        if not isinstance(item, list) or len(item) != 2:
            continue
        dt_str, task_label = item
        items.append((datetime.strptime(dt_str, ITEM_DATETIME_FMT), task_label))
        slug = get_label_slug(task_label)
        if slug not in slugs:
            slugs.append(slug)
    slugs.reverse()
    return (items, slugs)


def tdelta_to_str(tdelta):
    '''Returns timedelta as 'HH:MM:SS' string
    '''
    tdelta_int = tdelta.total_seconds()
    hours, remainder = divmod(tdelta_int, 3600)
    minutes, seconds = divmod(remainder, 60)
    return '{:02d}:{:02d}:{:02d}'.format(int(hours), int(minutes), int(seconds))


class DayLogger:
    '''Day logger class
    '''

    def __init__(self, log_name=None):
        '''Initializer

        Args:
            log_name - (optional) log filename to use
        '''
        self._log_name = log_name
        self._need_new_log = False
        self._json_data = []
        self._items = []
        self._slugs = []


    def set_log(self, log_name):
        '''Sets (new) log name
        '''
        self._log_name = log_name


    def get_log(self):
        '''Gets current log name
        '''
        return self._log_name


    def iter_slugs(self):
        '''Iterates over current slugs
        '''
        for slug in self._slugs:
            yield slug


    def load_log(self):
        '''Loads log
        '''
        try:
            if not self._log_name:
                self._log_name, same_day = get_last_log_name()
                if same_day:
                    self._need_new_log = False
                else:
                    self._need_new_log = True
            self._json_data = read_log_data(self._log_name, 'r')
        except (OSError, IOError, ValueError):
            self._need_new_log = True
            self._json_data = []


    def parse_data(self):
        '''Parses log's data
        '''
        try:
            self._items, self._slugs = parse_items(self._json_data)
        except FileNotFoundError:
            self._need_new_log = True
            self._items = []
            self._slugs = []

        if self._need_new_log:
            self._log_name = get_dt_str_by_fmt(LOG_NAME_FMT)
            self._items = []


    def log_append(self, label):
        '''Appends line to the log
        '''
        item = [get_now_time(), label]
        with open(self._log_name, 'a+') as fd_obj:
            log_item = [
                get_dt_str_by_fmt(ITEM_DATETIME_FMT, dt_obj=item[0]),
                item[1],
            ]
            fd_obj.write(json.dumps(log_item) + '\n')
        return item


    def add_log_item(self, label):
        '''Adds an item to the log
        '''
        item = self.log_append(label)
        self._items.append(item)
        slug = get_label_slug(label)
        if slug in self._slugs:
            self._slugs.remove(slug)
        self._slugs.insert(0, slug)


    def render_stats(self):
        '''Renders statistics
        '''
        dt_now = get_now_time()
        stats_dc = {slug: timedelta(0) for slug in self._slugs}
        dt_last = None
        slug_last = None
        for dt_curr, label in self._items:
            slug_curr = get_label_slug(label)

            if dt_last and slug_last:
                tdelta = timedelta(0)
                if dt_curr > dt_last:
                    tdelta += dt_curr - dt_last
                stats_dc[slug_last] += tdelta

            dt_last = dt_curr
            slug_last = slug_curr

        if dt_last and slug_last and dt_now > dt_last:
            stats_dc[slug_last] += dt_now - dt_last

        stats_lst = list(stats_dc.items())
        stats_lst.sort(key=lambda item: item[1], reverse=True)

        out_str = ''
        for slug, tdelta in stats_lst:
            out_str += '{:<20}: {}\n'.format(slug, tdelta_to_str(tdelta))

        return out_str



def main():
    '''Main method
    '''
    if len(os.sys.argv) >= 2:
        dlog = DayLogger(log_name=os.sys.argv[1])
    else:
        dlog = DayLogger()
    dlog.load_log()

    print('Latest log name:', dlog.get_log())

    dlog.parse_data()

    print('*NEW* log name:', dlog.get_log())

    if len(os.sys.argv) >= 3:
        dlog.add_log_item(os.sys.argv[2])

    stats_str = dlog.render_stats()

    print('stats:\n{}'.format(stats_str))


if __name__ == '__main__':
    main()


# vim: ts=4:sw=4:et:fdm=indent:ff=unix

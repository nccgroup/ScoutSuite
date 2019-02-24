# -*- coding: utf-8 -*-

from threading import Thread
from six.moves.queue import Queue

from ScoutSuite.core.console import print_exception


def thread_work(targets, function, params={}, num_threads=0):
    """
    Generic multithreading helper

    :param targets:
    :param function:
    :param params:
    :param num_threads:

    :return:
    """
    q = Queue(maxsize=0)
    if not num_threads:
        num_threads = len(targets)
    for i in range(num_threads):
        worker = Thread(target=function, args=(q, params))
        worker.setDaemon(True)
        worker.start()
    for target in targets:
        q.put(target)
    q.join()


def threaded_per_region(q, params):
    """
    Helper for multithreading on a per-region basis

    :param q:
    :param params:

    :return:
    """
    while True:
        try:
            params['region'] = q.get()
            method = params['method']
            method(params)
        except Exception as e:
            print_exception(e)
        finally:
            q.task_done()

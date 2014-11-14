#!/usr/bin/env python
import logging
import ecflow


def connect():
    logger = logging.getLogger()
    logger.info('Connecting to the ecflow server.')
    client = ecflow.Client()
    client.ping()
    return client


if __name__ == '__main__':
    c = connect()
    c.delete_all()
    c.load('test.def')
    # c.replace('/test', 'test.def')
    c.begin_suite('test')

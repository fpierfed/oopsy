#!/usr/bin/env python
import logging
import os
import ecflow


def create_suite():
    here = os.path.abspath(os.path.dirname(__file__))

    logger = logging.getLogger()
    logger.info('Creating suite definition.')

    defs = ecflow.Defs()
    suite = defs.add_suite('test')
    suite.add_variable('ECF_HOME', here)
    suite.add_variable('ECF_INCLUDE', here)
    suite.add_family(create_family1())
    suite.add_family(create_family2())
    return defs


def create_family1():
    f = ecflow.Family('f1')
    f.add_variable("SLEEP", 5)

    f.add_task('t1').add_meter("progress", 1, 100, 90)

    t2 = f.add_task('t2')
    t2.add_variable("SLEEP", 3)
    t2.add_trigger('t1 eq complete')
    t2.add_event("a")
    t2.add_event("b")

    f.add_task("t3").add_trigger("t2:a")

    t4 = f.add_task("t4")
    t4.add_trigger("t2 eq complete")
    t4.add_complete('t2:b')

    f.add_task("t5").add_trigger("t1:progress ge 30")
    f.add_task("t6").add_trigger("t1:progress ge 60")
    f.add_task("t7").add_trigger("t1:progress ge 90")
    return f


def create_family2():
    f = ecflow.Family('f2')
    f.add_variable("SLEEP", 5)

    f.add_task("t1").add_time('+00:00 00:02 00:01')

    f.add_task("t2").add_trigger("/test/f1/t3 eq complete")
    return f


if __name__ == '__main__':
    d = create_suite()
    assert len(d.check_job_creation()) == 0, 'Job generation failed.'
    d.save_as_defs('test.def')

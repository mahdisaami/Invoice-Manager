import unittest

import coverage
from coverage.html import os

from app import manager

COV = coverage.coverage(
    branch=True,
    include=['app.py', 'views.py', 'models.py', 'main.py'],
    omit=['tests/*']
)
COV.start()


@manager.command
def test():
    """Run the unit tests without test coverage. """
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def cov():
    """Run the unit tests with coverage. """
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage summary: ')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()
        return 0
    return 1


if __name__ == "__main__":
    manager.run()

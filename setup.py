import os
from distutils.core import setup, Command

import unittest

import logging.config
try:
    logging.config.fileConfig('stomp.log.conf')
except:
    pass

import stomp

os.environ['STD_HOST'] = '192.168.1.92'
os.environ['STD_PORT'] = '62613'
os.environ['STD_SSL_PORT'] = '62614'
os.environ['RABBITMQ_HOST'] = '192.168.1.92'
os.environ['RABBITMQ_PORT'] = '61613'
os.environ['STOMPSERVER_HOST'] = '192.168.1.92'
os.environ['STOMPSERVER_PORT'] = '63613'


class TestCommand(Command):
    user_options = [ ('test=', 't', 'specific test to run') ]

    def initialize_options(self):
        self.test = '*'

    def finalize_options(self):
        pass

    def run(self):
        suite = unittest.TestSuite()
        if self.test == '*':
            print('Running all tests')
            import test
            for tst in test.__all__:
                suite.addTests(unittest.TestLoader().loadTestsFromName('test.%s' % tst))
        else:
            suite = unittest.TestLoader().loadTestsFromName('test.%s' % self.test)
        unittest.TextTestRunner(verbosity=2).run(suite)

class DoxygenCommand(Command):
    user_options = [ ]

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('doxygen config.dox')
        
def version():
    s = []
    for num in stomp.__version__:
        s.append(str(num))
    return '.'.join(s)

setup(
    name = 'stomp.py',
    version = version(),
    description = 'Python STOMP client, supporting versions 1.0 and 1.1 of the protocol',
    license = 'Apache',
    url = 'http://code.google.com/p/stomppy',
    author = 'Jason R Briggs',
    author_email =  'jasonrbriggs@gmail.com',
    platforms = ['any'],
    packages = ['stomp'],
    cmdclass = { 'test' : TestCommand, 'docs' : DoxygenCommand }
)

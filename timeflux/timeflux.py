"""Timeflux entry point"""

import sys
import os
import psutil
import logging
from argparse import ArgumentParser
from importlib import import_module
from dotenv import load_dotenv
from timeflux import __version__
from timeflux.core.manager import Manager

LOGGER = logging.getLogger(__name__)

def main():
    sys.path.append(os.getcwd())
    args = _args()
    LOGGER.info('Timeflux %s' % __version__)
    load_dotenv(args.env)
    _init_logging(args.debug)
    _run_hook('pre')
    try:
        Manager(args.app).run()
    except Exception as error:
        LOGGER.error(error)
    _terminate()

def _args():
    parser = ArgumentParser()
    parser.add_argument('-v', '--version', action='version', version='Timeflux %s' % __version__)
    parser.add_argument('-d', '--debug', default=False, action='store_true', help='enable debug messages')
    parser.add_argument('-e', '--env', default='./.env', help='path to an environment file')
    parser.add_argument('app', help='path to the YAML or JSON application file')
    args = parser.parse_args()
    return args

def _terminate():
    psutil.wait_procs(psutil.Process().children())
    _run_hook('post')
    LOGGER.info('Terminated')
    logging.shutdown()
    sys.exit(0)

def _init_logging(debug):
    if debug:
        logging.getLogger().setLevel('DEBUG')
    else:
        try:
            logging.getLogger().setLevel(os.getenv('TIMEFLUX_LOG_LEVEL'))
        except Exception:
            logging.getLogger().setLevel('INFO')

def _run_hook(name):
    module = os.getenv('TIMEFLUX_HOOK_' + name.upper())
    if module:
        LOGGER.info('Running %s hook' % name)
        _import(module)

def _import(module):
    try:
        import_module(module)
    except Exception as error:
        LOGGER.exception(error)

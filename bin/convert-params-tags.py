#!/usr/bin/env python2
#
# Script to transform a parameters or tags file in AWS CLI JSON
# or YAML
# format to the commandline options, i.e. from:
# [
#   { 
#      "ParameterKey": "ParameterKey1",
#      "ParameterValue": "ParameterValue1"
#    }
#  ]
# 
# or
#
#  - ParameterKey: ParameterKey1,
#    ParameterValue: ParameterValue1
#
# to:
#
# ParameterKey1=ParameterValue1
#
import os
import yaml
import sys
import logging
from logging.handlers import SysLogHandler
import argparse

# FIXME: should be in a library file
# might be better to use a dictConfig available in Python 2.7 instead
def configure_logging(logger_name=None, level="DEBUG",
        cformat='%(asctime)s - %(module)s.%(funcName)s \
                (%(process)d) - %(levelname)s - %(message)s',
        sformat='%(module)s.%(funcName)s (%(process)d): \
                %(levelname)s %(message)s',
        console_output=True, syslog_output=True):
    # Get the root logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(getattr(logging, level))
    logger.handlers = []
    # Console log handler
    ch = logging.StreamHandler()
    ch.setLevel(getattr(logging, level))
    # Console log formatter
    cformatter = logging.Formatter(cformat)
    # add console formatter to console handler
    ch.setFormatter(cformatter)
    # Syslog handler
    if sys.platform == "darwin":
        syslog_address = '/var/run/syslog'
    else:
        syslog_address = '/dev/log'
    if syslog_output:
        sh = SysLogHandler(address=syslog_address,
                facility=SysLogHandler.LOG_DAEMON)
        sh.setLevel(getattr(logging, level))
        sformatter = logging.Formatter(sformat)
        sh.setFormatter(sformatter)
        logger.addHandler(sh)
    if console_output:
        # Running from the commandline, not in a pipe or cron-initiated
        # add console handler to the logger
        logger.addHandler(ch)
    return logger

def main():
    """ 
    Script to transform a parameters or tags file in AWS CLI JSON
    format to the commandline options, i.e. from:
    [
      { 
         "ParameterKey": "ParameterKey1",
         "ParameterValue": "ParameterValue1"
       }
     ]

    to:

    ParameterKey1=ParameterValue1
    """
    debug = False
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-file', dest='input_file',
            help='Input file with parameters/tags in JSON format',
            required=True)
    parser.add_argument('-o', '--output-file', dest='output_file',
            help='Output file with the parameters/tags in the options format',
            required=True)
    parser.add_argument('-K', '--key-name', dest='key_name',
            help='Name of the keys in the input file',
            required=True)
    parser.add_argument('-V', '--value-name', dest='value_name',
            help='Name of the values in the input file',
            required=True)
    parser.add_argument('-v', '--verbose',
            help='Increase output verbosity',
            action='count',
            default=0)
    parser.add_argument('-n', '--dryrun',
            help='Dry-run: show what is going to be done',
            action='store_true')
    parser.add_argument('-q', '--quiet',
            help='Quiet mode', action='store_true')
    args = parser.parse_args()

    if args.verbose > 0:
        logger.setLevel(logging.DEBUG)
    if args.verbose > 1:
        logging.getLogger('boto3').setLevel(logging.DEBUG)
        logging.getLogger('botocore').setLevel(logging.DEBUG)
        logging.getLogger('nose').setLevel(logging.DEBUG)
        logging.getLogger('s3transfer').setLevel(logging.DEBUG)
    if args.quiet:
        logger.setLevel(logging.CRITICAL)

    input_file_path = os.path.expanduser(args.input_file)
    output_file_path = os.path.expanduser(args.output_file)
    input_cfg = yaml.load(open(os.path.realpath(input_file_path), 'r'))
    output_cfg = open(os.path.realpath(output_file_path), 'w')

    transformed = [ item[args.key_name] + "='" + item[args.value_name] + "'"
                        for item in input_cfg ]
    for w in transformed:
        output_cfg.write(w+" ")
    output_cfg.close()

if __name__ == '__main__':
    main()

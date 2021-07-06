"""
Manages app configuration
"""
import os
from dotenv import dotenv_values

ENV_DB = (
    'DOCRMV_DB_SOCKET',
    'DOCRMV_DB_HOST',
    'DOCRMV_DB_PORT',
    'DOCRMV_DB_USER',
    'DOCRMV_DB_PASS',
    'DOCRMV_DB_DATABASE',
    'DOCRMV_DB_SSL_CA',
    'DOCRMV_DB_SSL_KEY',
    'DOCRMV_DB_SSL_CERT',)

ENV_DRIVE = (
    'GOOGLE_APPLICATION_CREDENTIALS',
    'DRIVE_DELEGATE_ACCOUNT',
    'DRIVE_TRAVELER_IMAGES',
    'DRIVE_TRAVELER_FILES',
    'DRIVE_REQUEST_IMAGES',
    'DRIVE_REQUEST_FILES',
    'DRIVE_DOCUMENT_IMAGES',
    'DRIVE_DOCUMENT_FILES',
    'DRIVE_DELETED_FILES',)

ENV_OPTIONS = ('SAMPLE_OWNER',)

ENVVARS = ENV_DB + ENV_DRIVE + ENV_OPTIONS

def load(envpath = '.env'):
    """
    Returns configuration defined in ENV file or environment variables
    ENV file takes precedence over environment variables
    """
    config = get_env()
    if os.path.exists(envpath):
        config.update(dotenv_values(envpath))
    return config

def get_env():
    """
    Extracts configuration from environment variables
    """
    return {k: v for k, v in os.environ.items() if k in ENVVARS}

def check_db_conf(envpath = '.env'):
    """
    Checks DB configuration
    """
    errs = []
    conf = load(envpath)
    for key in ENV_DB:
        if key not in conf:
            errs.append(key + ' Not Found')
    return errs

def check_drive_conf(envpath = '.env'):
    """
    Checks Drive configuration
    """
    errs = []
    conf = load(envpath)
    for key in ENV_DRIVE:
        if key not in conf:
            errs.append(key + ' Not Found')
    return errs

def check(envpath = '.env'):
    """
    Check configuration file
    """
    return check_db_conf(envpath) + check_drive_conf(envpath)

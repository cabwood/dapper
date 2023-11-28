import os, sys
from functools import wraps
from dotenv import load_dotenv


TRUE_VALUES = {'1', 'true', 'yes'}
FALSE_VALUES = {'0', 'false', 'no'}
BOOL_VALUES = TRUE_VALUES | FALSE_VALUES


class EnvironmentError(ValueError):
    pass


class MissingError(EnvironmentError):

    def __init__(self, name):
        super().__init__(f'Missing environment variable "{name}".')


class InvalidError(EnvironmentError):

    def __init__(self, name):
        super().__init__(f'Invalid environment variable "{name}".')


class Missing:
    """
    Placeholder for default parameters, to distinguish them from None.
    """
    pass

MISSING = Missing()


def handle_error(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except EnvironmentError as exc:
            error(str(exc), True)
    return wrapper

def error(message, fatal=False):
    sys.stderr.write(f"{message}\n")
    if fatal:
        sys.exit(1)

def load(file=None):
    # Load environment from given file
    if file:
        try:
            load_dotenv(file)
        except Exception as exc:
            error(str(exc), True)
    # Load environment from local '.env' file
    try:
        load_dotenv(override=True)
    except Exception as exc:
        error(str(exc), True)

@handle_error
def get(name, default=MISSING):
    value = os.getenv(name)
    if value is None:
        if default is MISSING:
            raise MissingError(name)
        else:
            return default
    return value

@handle_error
def get_int(name, default=MISSING):
    value = os.getenv(name)
    if value is None:
        if default is MISSING:
            raise MissingError(name)
        else:
            return default
    try:
        return int(value)
    except:
        raise InvalidError(name)

@handle_error
def get_bool(name, default=MISSING):
    value = os.getenv(name)
    if value is None:
        if default is MISSING:
            raise MissingError(name)
        else:
            return default
    value = value.strip().lower()
    if not value in BOOL_VALUES:
        raise InvalidError(name)
    return value in TRUE_VALUES



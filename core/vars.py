from os import environ


class ServiceVariables:
    """

    """
    URL = environ.get('BASE_URL') or '127.0.0.1:8080'
    CUSTOM_HEAD_LABEL = environ.get('CUSTOM_HEAD_LABEL') or 'Лицевая сторона'
    CUSTOM_TAIL_LABEL = environ.get('CUSTOM_TAIL_LABEL') or 'Обратная сторона'
    SHRINK_HISTORY_TO = environ.get('SHRINK_HISTORY_TO') or 5
    ''' '''

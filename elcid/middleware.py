import logging
import time
import random
from datetime import datetime

from django.conf import settings
from django.db import connection


class SessionMiddleware(object):
    logger = logging.getLogger('elcid.sessionLogger')

    def process_request(self, request):
        username = 'anonymous'
        path = request.path
        # add an empty line seprator per request
        self.logger.info('')

        if request.user.is_authenticated():
            username = request.user.username
        self.logger.info('{0} received a request with user {1} for {2}'.format(
            datetime.now().strftime('%d/%m/%Y %H:%M:%S'), username, path
        ))
        self.logger.info('cookies')
        self.logger.info(request.COOKIES)
        self.logger.info('session')
        self.logger.info(request.session.items())
        expiry = request.session.get_expiry_date().isoformat()
        self.logger.info('expiry {}'.format(expiry))

    def process_response(self, request, response):
        username = 'anonymous'
        path = request.path

        if request.user.is_authenticated():
            username = request.user.username

        self.logger.info('responding to a request with user {0} for {1}'.format(
            username, path
        ))

        if request.user.is_authenticated():
            if 'expired_token' in request.session:
                self.logger.info(
                    'now logged in, clearing {}'.format(
                        request.session['expired_token']
                    )
                )
                del request.session['expired_token']

        if not request.user.is_authenticated():
            if "expired_token" not in request.session:
                expiration_id = random.randint(1, 1000000000)
                self.logger.info(
                    'no session token found, setting expiry to {}'.format(
                        expiration_id
                    )
                )
                request.session["expired_token"] = expiration_id

        return response


class LoggingMiddleware(object):
    logger = logging.getLogger('elcid.requestLogger')

    def process_request(self, request):
        self.start_time = time.time()

    def process_response(self, request, response):
        try:
            username = "-"
            extra_log = ""
            if hasattr(request, 'user'):
                username = getattr(request.user, 'username', '-')
            req_time = time.time() - self.start_time

            if settings.DEBUG:
                sql_time = sum(float(q['time']) for q in connection.queries) * 1000
                extra_log += " (%s SQL queries, %s ms)" % (len(connection.queries), sql_time)

            self.logger.info("%s %s %s %s %s (%.02f seconds)%s" % (
                datetime.now(), username, request.method, request.get_full_path(),
                response.status_code, req_time, extra_log)
            )
        except Exception as e:
            logging.error("LoggingMiddleware Error: %s" % e)

        return response

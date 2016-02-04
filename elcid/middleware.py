from django.conf import settings
from django.db import connection
from datetime import datetime
import logging
import time

logger = logging.getLogger('elcid.requestLogger')


class LoggingMiddleware(object):
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

            logger.info("%s %s %s %s %s (%.02f seconds)%s" % (
                datetime.now(), username, request.method, request.get_full_path(),
                response.status_code, req_time, extra_log)
            )
        except Exception, e:
            logging.error("LoggingMiddleware Error: %s" % e)
            
        return response

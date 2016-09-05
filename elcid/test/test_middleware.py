import datetime
from mock import MagicMock, patch
from django.test import override_settings
from opal.core.test import OpalTestCase
from elcid.middleware import SessionMiddleware, LoggingMiddleware


class SessionMiddlewareTestCase(OpalTestCase):
    def setUp(self):
        self.middleware = SessionMiddleware()
        self.middleware.logger.info = MagicMock()
        self.request = self.rf.get("/")
        self.request.user = MagicMock()
        self.request.user.is_authenticated = MagicMock()
        self.request.session = MagicMock()
        self.request.session.items = MagicMock()
        self.request.session.get_expiry_date = MagicMock()
        self.request.COOKIES = "cookies information"

    def test_anonymous_process_request(self):
        """ if the user is not logged in, log all the information
        """
        self.request.user.is_authenticated.return_value = False
        self.request.session.items.return_value = {}
        self.request.session.get_expiry_date.return_value = datetime.datetime(
            2016, 9, 5, 11, 14, 3, 529434
        )
        self.middleware.process_request(self.request)
        call_args = self.middleware.logger.info.call_args_list
        self.assertEqual(call_args[0][0][0], '')
        self.assertEqual(
            call_args[1][0][0],
            'received a request with user anonymous for /'
        )
        self.assertEqual(
            call_args[2][0][0],
            'cookies'
        )
        self.assertEqual(
            call_args[3][0][0],
            'cookies information'
        )
        self.assertEqual(
            call_args[4][0][0],
            'session'
        )
        self.assertEqual(
            call_args[5][0][0],
            {}
        )
        self.assertEqual(
            call_args[6][0][0],
            'expiry 2016-09-05T11:14:03.529434'
        )

    def test_logged_in_process_request(self):
        """ if the user is logged in, just log the request normally
        """
        self.request.user.is_authenticated.return_value = True
        self.request.user.username = "someone"
        self.middleware.process_request(self.request)
        call_args = self.middleware.logger.info.call_args_list
        self.assertEqual(
            call_args[1][0][0],
            'received a request with user someone for /'
        )

    def test_logged_in_process_response(self):
        """ if the user is now logged in, clear the expiry token
        """
        self.request.user.is_authenticated.return_value = True
        self.request.user.username = "someone"
        self.request.session.__contains__.return_value = True
        self.request.session.__getitem__.return_value = 1231212
        response = self.middleware.process_response(
            self.request, "some response"
        )
        call_args = self.middleware.logger.info.call_args_list

        self.assertEqual(
            call_args[0][0][0],
            'responding to a request with user someone for /'
        )

        self.assertEqual(
            call_args[1][0][0],
            'now logged in, clearing 1231212'
        )

        self.assertEqual(response, "some response")
        self.request.session.__contains__.assert_called_once_with("expired_token")
        self.request.session.__getitem__.assert_called_once_with("expired_token")

    @patch('elcid.middleware.random')
    def test_anonymous_first_process_response(self, random):
        """ we should set the expiry toke if its not set
        """
        self.request.user.is_authenticated.return_value = False
        self.request.session.__contains__.return_value = False
        random.randint = MagicMock(return_value=20)
        self.middleware.process_response(
            self.request, "some response"
        )

        call_args = self.middleware.logger.info.call_args

        self.assertEqual(
            call_args[0][0][0],
            'responding to a request with anonymous someone for /'
        )

        self.assertEqual(
            call_args[1][0][0],
            'no session token found, setting expiry to 20'
        )

        self.request.session.__setitem__.assert_called_once_with(
            "expired_token", 20
        )

    @patch('elcid.middleware.random')
    def test_anonymous_first_process_response(self, random):
        """ we shouldn't replace the expiry token if its already set
        """
        self.request.user.is_authenticated.return_value = False
        self.request.session.__contains__.return_value = True
        self.middleware.process_response(
            self.request, "some response"
        )
        self.assertFalse(random.randint.called)

@patch('elcid.middleware.time')
class LoggingMiddlewareTestCase(OpalTestCase):
    def setUp(self):
        self.middleware = LoggingMiddleware()
        self.middleware.logger.info = MagicMock()
        self.middleware.logger.error = MagicMock()
        self.request = self.rf.get("/")
        self.request.user = MagicMock()
        self.request.get_full_path = MagicMock(return_value="/")
        self.request.user.username = "someone"
        self.response = MagicMock(name='response')
        self.response.status_code = 200

    def test_process_request(self, time):
        time.time.return_value = 1231212
        self.middleware.process_request(self.request)
        self.assertEqual(self.middleware.start_time, 1231212)

    @override_settings(DEBUG=False)
    @patch('elcid.middleware.connection')
    @patch('elcid.middleware.datetime')
    def test_process_response_without_debug(self, dt, connection, time):
        self.middleware.start_time = 1231211
        time.time.return_value = 1231212
        dt.now.return_value = datetime.datetime(2016, 9, 5, 11, 14, 3, 529434)
        response = self.middleware.process_response(
            self.request, self.response
        )
        self.assertEqual(response, self.response)
        self.middleware.logger.info.assert_called_once_with(
            '2016-09-05 11:14:03.529434 someone GET / 200 (1.00 seconds)'
        )

    @override_settings(DEBUG=True)
    @patch('elcid.middleware.connection')
    @patch('elcid.middleware.datetime')
    def test_process_response_with_debug(self, dt, connection, time):
        self.middleware.start_time = 1231211
        connection.queries = [{"time": 10}]
        time.time.return_value = 1231212
        dt.now.return_value = datetime.datetime(2016, 9, 5, 11, 14, 3, 529434)
        response = self.middleware.process_response(
            self.request, self.response
        )
        self.assertEqual(response, self.response)
        self.middleware.logger.info.assert_called_once_with(
            '2016-09-05 11:14:03.529434 someone GET / 200 (1.00 seconds) (1 SQL queries, 10000.0 ms)'
        )

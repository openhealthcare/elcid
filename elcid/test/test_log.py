import logging
import mock
from django.test import override_settings
from opal.core.test import OpalTestCase
from elcid.log import ConfidentialEmailer


# we mock the stream handler because we don't want
# unnecessary logging critical statements when running tests
@override_settings(DEBUG=False, OPAL_BRAND_NAME="Amazing elCID App")
@mock.patch('logging.StreamHandler.emit')
@mock.patch('django.utils.log.AdminEmailHandler.send_mail')
class LogOutputTestCase(OpalTestCase):
    def test_request_logging_critical(self, send_mail, stream_handler):
        logger = logging.getLogger('django.request')
        logger.error('confidential error')
        self.assertTrue(send_mail.called)
        expected_subject = "Amazing elCID App error"
        expected_body = "censored"
        call_args = send_mail.call_args
        self.assertEqual(expected_subject, call_args[0][0])
        self.assertIn(expected_body, call_args[0][1])
        self.assertEqual(call_args[1]["html_message"], None)

    def test_request_logging_with_arguments(self, send_mail, stream_handler):
        logger = logging.getLogger('django.request')
        logger.error('%s error', "confidential")
        self.assertTrue(send_mail.called)
        expected_subject = "Amazing elCID App error"
        expected_body = "censored"
        call_args = send_mail.call_args
        self.assertEqual(expected_subject, call_args[0][0])
        self.assertIn(expected_body, call_args[0][1])
        self.assertEqual(call_args[1]["html_message"], None)

    @mock.patch('elcid.log.AdminEmailHandler.emit')
    def test_record_formatting(self, emitter, send_mail, stream_handler):
        emailer = ConfidentialEmailer()
        record = mock.MagicMock()
        record.exc_text = "confidential"
        record.args = ["some_args"]
        record.filename = "some_file.py"
        record.lineno = 20
        request = self.rf.get("/some/url")
        request.user = self.user
        request.session = {}
        record.request = request
        emailer.emit(record)
        self.assertEqual(
            emitter.call_args[0][0].exc_text,
            """from some_file.py:20\nsent to host None  on application Amazing elCID App from user testuser with GET"""
        )

    @mock.patch('elcid.log.AdminEmailHandler.emit')
    def test_anonymous_user_record_formatting(self, emitter, send_mail, stream_handler):
        emailer = ConfidentialEmailer()
        record = mock.MagicMock()
        record.exc_text = "confidential"
        record.args = ["some_args"]
        record.filename = "some_file.py"
        record.lineno = 20
        request = self.rf.get("/some/url")
        request.user = self.user

        request.session = {}
        record.request = request
        with mock.patch.object(request.user, "is_authenticated") as is_authenticated:
            is_authenticated.return_value = False
            emailer.emit(record)
        self.assertEqual(
            emitter.call_args[0][0].exc_text,
            """from some_file.py:20\nsent to host None  on application Amazing elCID App from user anonymous with GET"""
        )

    def test_no_email_on_info(self, send_mail, stream_handler):
        logger = logging.getLogger('django.request')
        logger.info('%s error', "confidential")
        self.assertFalse(send_mail.called)

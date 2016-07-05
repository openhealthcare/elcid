import logging
import mock
from django.test import override_settings
from opal.core.test import OpalTestCase
from elcid.log import ConfidentialEmailer


# we mock the stream handler because we don't want
# unnecessary logging critical statements when running tests
@override_settings(DEBUG=False)
@mock.patch('logging.StreamHandler.emit')
@mock.patch('django.utils.log.AdminEmailHandler.send_mail')
class LogOutputTestCase(OpalTestCase):
    def test_request_logging_critical(self, send_mail, stream_handler):
        logger = logging.getLogger('django.request')
        logger.error('confidential error')
        self.assertTrue(send_mail.called)
        expected_subject = "elCID error"
        expected_body = "censored"
        call_args = send_mail.call_args
        self.assertEqual(expected_subject, call_args[0][0])
        self.assertIn(expected_body, call_args[0][1])
        self.assertEqual(call_args[1]["html_message"], None)

    def test_request_logging_with_arguments(self, send_mail, stream_handler):
        logger = logging.getLogger('django.request')
        logger.error('%s error', "confidential")
        self.assertTrue(send_mail.called)
        expected_subject = "elCID error"
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
        record.status_code = 500
        record.args = ["some_args"]
        record.filename = "some_file.py"
        record.lineno = 20
        emailer.emit(record)
        self.assertEqual(
            emitter.call_args[0][0].exc_text,
            "status code 500 from some_file.py:20"
        )

    def test_no_email_on_info(self, send_mail, stream_handler):
        logger = logging.getLogger('django.request')
        logger.info('%s error', "confidential")
        self.assertFalse(send_mail.called)

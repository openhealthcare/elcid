import logging
import mock


from django.test import override_settings

from opal.core.test import OpalTestCase


@override_settings(DEBUG=False)
@mock.patch('django.utils.log.AdminEmailHandler.send_mail')
class test_log_output(OpalTestCase):

    def test_request_logging_output(self, send_mail):
        logger = logging.getLogger('django.request')
        logger.critical('confidential error')
        self.assertTrue(send_mail.called)
        expected_subject = "elCID error"
        expected_body = "elcid/elcid/test/test_log.py:16"
        call_args = send_mail.call_args
        self.assertEqual(call_args[0][0], expected_subject)
        self.assertIn(expected_body, call_args[0][1])
        self.assertEqual(call_args[1]["html_message"], None)

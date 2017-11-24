from opal.core.test import OpalTestCase
from elcid.management.commands import error_emailer
import mock


class ErrorEmailerTestCase(OpalTestCase):

    @mock.patch('elcid.management.commands.error_emailer.logging')
    def test_error_emailer(self, logging):
        command = error_emailer.Command()
        command.handle("Some error")
        logging.getLogger.assert_called_once_with("error_emailer")
        logging.getLogger().error.assert_called_once_with("Some error")

    def test_add_arguments(self):
        command = error_emailer.Command()
        parser = mock.MagicMock()
        command.add_arguments(parser)
        parser.add_argument.assert_called_once_with("error", type=str)

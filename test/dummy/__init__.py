from wizlib.app import WizApp
from wizlib.config_handler import ConfigHandler
from wizlib.stream_handler import StreamHandler
from wizlib.ui_handler import UIHandler

from .command import DummyCommand


class DummyApp(WizApp):

    base = DummyCommand
    handlers = [StreamHandler, ConfigHandler, UIHandler]
    name = 'dummy'

from wizlib.app import WizApp
from wizlib.stream_handler import StreamHandler
from wizlib.config_handler import ConfigHandler
from wizlib.ui_handler import UIHandler

from template.command import TemplateCommand


class TemplateApp(WizApp):

    base = TemplateCommand
    name = 'template'
    handlers = [StreamHandler, ConfigHandler, UIHandler]

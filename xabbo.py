import os
from os import path
import sys
import inspect
from datetime import datetime
from typing import Callable, Union

from g_python.gextension import Extension
from g_python.hdirection import Direction
from g_python.hmessage import HMessage
from g_python.hpacket import HPacket

from options import Options

import importlib

VERSION = "1.1.0"

CMD_PREFIX = '/'

class XabboExt(Extension):
    opts: Options
    __cmds: dict[str, Callable[[list[str]], None]]

    def __init__(self):
        super().__init__({
            'title': 'xabbo.py',
            'description': 'yes',
            'version': VERSION,
            'author': 'b7'
        }, sys.argv)
        self.on_event('init', lambda: self.log('Extension initialized'))
        self.on_event('connection_start', lambda: self.log('Connection established'))
        self.on_event('connection_end', lambda: self.log('Connection lost'))
        self.intercept_out(self.__on_whisper, 'Whisper')
        self.intercept_out(self.__on_chat, 'Chat')
        self.intercept_out(self.__on_chat, 'Shout')
        self.opts = Options()
        self.__cmds = dict()
    
    def init(self):
        self.log(f'--- xabbo.py v{VERSION} ---')
        components_dir = path.join(path.dirname(__file__), 'components')
        for filename in os.listdir(components_dir):
            if filename.endswith('.py'):
                module_name = 'components.' + filename[:-3]
                module = importlib.import_module(module_name)
                members = inspect.getmembers(module, inspect.isclass)
                for className, member in members:
                    if not className.endswith('Component'): continue
                    componentName = className[:-len('Component')]
                    if len(componentName) == 0: continue
                    export = getattr(module, className)
                    component = export()
                    component.ext = self
                    component.opts = self.opts
                    component.init()
                    self.log(f'Loaded {componentName} component');

    def info(self, message: str):
        self.send_to_client(HPacket('Whisper', -1, message, 0, 2, 0, 0))
    
    def log(self, message: str):
        print(f'[{datetime.now():%H:%M:%S}] {message}')
    
    def intercept_out(self,
                      callback: Callable[[HMessage], None],
                      id: Union[int, str] = -1,
                      mode: str = 'default'):
        self.intercept(Direction.TO_SERVER, callback, id, mode)
    
    def intercept_in(self,
                     callback: Callable[[HMessage], None],
                     id: Union[int, str] = -1,
                     mode: str = 'default'):
        self.intercept(Direction.TO_CLIENT, callback, id, mode)
    
    def register_cmd(self,
                     command: str,
                     handler: Callable[[list[str]], None],
                     aliases: Union[str, list[str]] = []):
        if isinstance(aliases, str):
            aliases = [aliases]
        for cmd in [command, *aliases]:
            cmd = cmd.lower()
            if cmd in self.__cmds:
                raise Exception(f'The command \'{cmd}\' is already registered')
            self.__cmds[cmd] = handler
    
    def __on_whisper(self, msg: HMessage):
        message = msg.packet.read_string()
        index = message.find(' ')
        if index < 0: return
        message = message[index+1:]
        if message[0] == CMD_PREFIX:
            msg.is_blocked = True
            self.handle_command(message)

    def __on_chat(self, msg: HMessage):
        message = msg.packet.read_string()
        if message[0] == CMD_PREFIX:
            msg.is_blocked = True
            self.handle_command(message)

    def handle_command(self, message: str):
        if message[0] != '/':
            return
        args = message.strip().split()
        command = args[0][1:].lower()
        args = args[1:]
        if command in self.__cmds:
            self.__cmds[command](args)
        else:
            self.info(f'Unknown command: \'{command}\'')
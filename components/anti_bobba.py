import re
from typing import Match
from g_python.hmessage import HMessage

from component import Component
from xabbo import CMD_PREFIX

ANTI_BOBBA = "ƳƷ"

def inject_anti_bobba(text: str) -> str:
    if isinstance(text, Match):
        text = text[1]
    return ANTI_BOBBA.join(text)

def apply_anti_bobba(text: str, localized: bool) -> str:
    if localized:
        text = re.sub(r'\[([^\[\]]+)\]', inject_anti_bobba, text)
    else:
        text = inject_anti_bobba(text)
    return text

class AntiBobbaComponent(Component):
    def init(self):
        self.ext.register_cmd('bobba', self.handle_cmd, 'ab')
        self.ext.intercept_out(self.on_whisper, 'Whisper')
        self.ext.intercept_out(self.on_chat, 'Chat')
        self.ext.intercept_out(self.on_chat, 'Shout')

    def handle_cmd(self, args: list[str]):
        if len(args) == 0:
            self.ext.opts.AntiBobba = not self.opts.AntiBobba
        else:
            mode = args[0].lower()
            if mode == 'off':
                self.opts.AntiBobba = False
                self.ext.info('Anti-bobba disabled')
            elif mode == 'local':
                self.opts.AntiBobba = True
                self.opts.AntiBobbaLocalized = True
            elif mode == 'full':
                self.opts.AntiBobba = True
                self.opts.AntiBobbaLocalized = False
            else:
                return
        if self.opts.AntiBobba:
            if self.opts.AntiBobbaLocalized:
                self.ext.info('Localized anti-bobba enabled')
            else:
                self.ext.info('Full anti-bobba enabled')
        else:
            self.ext.info('Anti-bobba disabled')

    def on_whisper(self, msg: HMessage):
        text = msg.packet.read_string()
        index = text.find(' ')
        if index < 0: return
        target = text[:index]
        text = text[index+1:]
        if text.startswith(CMD_PREFIX): return
        if self.opts.AntiBobba:
            text = apply_anti_bobba(text, self.opts.AntiBobbaLocalized)
            msg.packet.replace_string(6, f'{target} {text}')

    def on_chat(self, msg: HMessage):
        text = msg.packet.read_string()
        if text.startswith(CMD_PREFIX): return
        if self.opts.AntiBobba:
            text = apply_anti_bobba(text, self.opts.AntiBobbaLocalized)
            msg.packet.replace_string(6, text)
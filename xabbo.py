import sys
import re
from datetime import datetime
from typing import Match

from g_python.gextension import Extension
from g_python.hmessage import Direction, HMessage
from g_python.hpacket import HPacket

# --- Options ---
class Options:
    AntiIdle = True
    AntiTyping = True
    AntiBobba = True
    AntiBobbaLocalized = True
    AntiLook = True

opts = Options()

# --- Constants ---
ANTI_BOBBA = "ƳƷ"
DIRECTIONS = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
VECTORS = [
    ( -1000, -10000 ), # N
    ( 1000, -10000 ),  # NE
    ( 10000, -1000 ),  # E
    ( 10000, 1000 ),   # SE
    ( 1000, 10000 ),   # S
    ( -1000, 10000 ),  # SW
    ( -10000, 1000 ),  # W
    ( -10000, -1000 )  # NW
]

# --- Utility ---
def log(message: str):
    print(f'[{datetime.now():%H:%M:%S}] {message}')

def info(message: str):
    ext.send_to_client(HPacket('Whisper', -1, message, 0, 2, 0, 0))

def handle_command(text) -> bool:
    if text[0] != '/':
        return False
    args = text[1:].split()
    cmd = args[0].lower()
    args = args[1:]
    if cmd in cmd_handlers:
        cmd_handlers[cmd](args)
    else:
        info(f'Unknown command: \'{cmd}\'')
    return True

def inject_anti_bobba(text: str) -> str:
    if isinstance(text, Match):
        text = text[1]
    return ANTI_BOBBA.join(text)

def apply_anti_bobba(text: str) -> str:
    if opts.AntiBobbaLocalized:
        text = re.sub(r'\[([^\[\]]+)\]', inject_anti_bobba, text)
    else:
        text = inject_anti_bobba(text)
    return text

# --- Commands ---
def cmd_anti_idle(args):
    opts.AntiIdle = not opts.AntiIdle
    status = ('disabled', 'enabled')[opts.AntiIdle]
    info(f'Anti-idle {status}')

def cmd_anti_typing(args):
    opts.AntiTyping = not opts.AntiTyping
    status = ('disabled', 'enabled')[opts.AntiTyping]
    info(f'Anti-typing {status}')    

def cmd_anti_bobba(args):
    if len(args) == 0:
        opts.AntiBobba = not opts.AntiBobba
    else:
        mode = args[0].lower()
        if mode == 'off':
            opts.AntiBobba = False
            info('Anti-bobba disabled')
        elif mode == 'local':
            opts.AntiBobba = True
            opts.AntiBobbaLocalized = True
        elif mode == 'full':
            opts.AntiBobba = True
            opts.AntiBobbaLocalized = False
        else:
            return
    if opts.AntiBobba:
        if opts.AntiBobbaLocalized:
            info('Localized anti-bobba enabled')
        else:
            info('Full anti-bobba enabled')
    else:
        info('Anti-bobba disabled')

def cmd_anti_look(args):
    opts.AntiLook = not opts.AntiLook
    status = ('disabled', 'enabled')[opts.AntiLook]
    info(f'Anti-look {status}')

def cmd_turn(args):
    if len(args) == 0:
        return
    dir = args[0].lower()
    if dir in DIRECTIONS:
        index = DIRECTIONS.index(dir)
        vector = VECTORS[index]
        ext.send_to_server(HPacket('LookTo', vector[0], vector[1]))

cmd_handlers = {
    'idle': cmd_anti_idle,
    'type': cmd_anti_typing,
    'bobba': cmd_anti_bobba,
    'look': cmd_anti_look,
    'turn': cmd_turn
}

# --- Intercepts ---
def on_ping(msg: HMessage):
    if opts.AntiIdle:
        ext.send_to_server(HPacket('AvatarExpression', 0))
        log('Anti-idle')

def on_whisper(msg: HMessage):
    text = msg.packet.read_string()
    if ' ' not in text:
        return
    index = text.index(' ')
    target = text[:index]
    text = text[index+1:]
    log(f'whisper({target}, {text})')
    if handle_command(text):
        msg.is_blocked = True
    elif opts.AntiBobba:
        text = apply_anti_bobba(text)
        msg.packet.replace_string(6, f'{target} {text}')

def on_chat(msg: HMessage):
    text = msg.packet.read_string()
    if handle_command(text):
        msg.is_blocked = True
    elif opts.AntiBobba:
        text = apply_anti_bobba(text)
        msg.packet.replace_string(6, text)

def on_look_to(msg: HMessage):
    if opts.AntiLook:
        msg.is_blocked = True

def on_start_typing(msg: HMessage):
    if opts.AntiTyping:
        msg.is_blocked = True

# --- Extension ---
ext = Extension({
    'title': 'xabbo.py',
    'description': 'yes',
    'version': '1.0.1',
    'author': 'b7'
}, sys.argv)

def on_initialized():
    log('Extension initialized')

def on_connection_start():
    log('Connection established')

def on_connection_end():
    log('Connection lost')

ext.on_event('init', on_initialized)
ext.on_event('connection_start', on_connection_start)
ext.on_event('connection_end', on_connection_end)

ext.intercept(Direction.TO_CLIENT, on_ping, 'Ping')
ext.intercept(Direction.TO_SERVER, on_whisper, 'Whisper')
ext.intercept(Direction.TO_SERVER, on_chat, 'Chat')
ext.intercept(Direction.TO_SERVER, on_chat, 'Shout')
ext.intercept(Direction.TO_SERVER, on_look_to, 'LookTo')
ext.intercept(Direction.TO_SERVER, on_start_typing, 'StartTyping')

ext.start()

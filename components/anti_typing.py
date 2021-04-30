from g_python.hmessage import HMessage

from component import Component

class AntiTypingComponent(Component):
    def init(self):
        self.ext.register_cmd('type', self.handle_cmd, 'at')
        self.ext.intercept_out(self.on_start_typing, 'StartTyping')
    
    def handle_cmd(self, args: list[str]):
        self.opts.AntiTyping = not self.opts.AntiTyping
        status = ('disabled', 'enabled')[self.opts.AntiTyping]
        self.ext.info(f'Anti-typing {status}')

    def on_start_typing(self, msg: HMessage):
        if self.opts.AntiTyping:
            msg.is_blocked = True
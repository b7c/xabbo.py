from g_python.hmessage import HMessage

from component import Component

class AntiLookComponent(Component):
    def init(self):
        self.ext.register_cmd('look', self.handle_cmd, 'al')
        self.ext.intercept_out(self.on_look, 'LookTo')
    
    def handle_cmd(self, args: list[str]):
        self.opts.AntiLook = not self.opts.AntiLook
        status = ('disabled', 'enabled')[self.opts.AntiLook]
        self.ext.info(f'Anti-look {status}')
    
    def on_look(self, msg: HMessage):
        if self.opts.AntiLook:
            msg.is_blocked = True
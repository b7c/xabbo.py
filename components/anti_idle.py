from g_python.hmessage import HMessage
from g_python.hpacket import HPacket

from component import Component

class AntiIdleComponent(Component):
    def init(self):
        self.ext.register_cmd('idle', self.handle_cmd, 'ai')
        self.ext.intercept_in(self.on_ping, 'Ping')
    
    def handle_cmd(self, args: list[str]):
        self.opts.AntiIdle = not self.opts.AntiIdle
        status = ('disabled', 'enabled')[self.opts.AntiIdle]
        self.ext.info(f'Anti-idle {status}')
    
    def on_ping(self, msg: HMessage):
        if self.opts.AntiIdle:
            self.ext.send_to_server(HPacket('AvatarExpression', 0))
            self.ext.log('Anti-idle')
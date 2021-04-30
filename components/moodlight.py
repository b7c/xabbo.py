from g_python.hpacket import HPacket

from component import Component

class MoodlightComponent(Component):
    def init(self):
        self.ext.register_cmd('mood', self.handle_cmd)
    
    def handle_cmd(self, args: list[str]):
        if len(args) == 0:
            self.ext.send_to_server(HPacket('RoomDimmerChangeState'))
        else:
            arg = args[0].lower()
            if arg == 'settings':
                self.ext.send_to_server(HPacket('RoomDimmerGetPresets'))
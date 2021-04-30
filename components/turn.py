from g_python.hpacket import HPacket

from component import Component

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

class TurnComponent(Component):
    def init(self):
        self.ext.register_cmd('turn', self.on_cmd)
    
    def on_cmd(self, args: list[str]):
        if len(args) == 0:
            return
        dir = args[0].lower()
        if dir in DIRECTIONS:
            index = DIRECTIONS.index(dir)
            vector = VECTORS[index]
            self.ext.send_to_server(HPacket('LookTo', vector[0], vector[1]))

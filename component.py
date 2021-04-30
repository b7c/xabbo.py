import abc
from xabbo import XabboExt
from options import Options

class Component(metaclass=abc.ABCMeta):
    ext: XabboExt
    opts: Options

    @abc.abstractmethod
    def init(self):
        """Initialize the component"""
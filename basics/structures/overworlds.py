# 473 -> a/1/2/6 -> overworlds
from . import *

class Overworlds(Structure):
    def __init__(self, raw:bytearray):
        narc = ndspy.narc.NARC(raw)
        self.worlds:typing.List[Overworlds.Overworld] = []
        for file in narc.files:
            if all(byte == 0 for byte in file):
                break
            self.worlds.append(Overworlds.Overworld(file))

    def __getitem__(self, index:int):
        return self.worlds[index]
    
    def __len__(self):
        return len(self.worlds)

    class Overworld():
        def __init__(self, raw:bytearray):
            self.data = Util.byte_to_int_array(raw)
            self.header = self.data[:8]
            #print('# furniture: %d' % self.header[4])
            #print('# npc: %d' % self.header[5])
            #print('# warp: %d' % self.header[6])
            #print('# trigger: %d' % self.header[7])
            start = 8
            self.furniture = list(( Overworlds.Furniture(self.data[start+i*0x14:start+(i+1)*0x14]) for i in range(self.header[4]) ))
            start += self.header[4] * 0x14
            self.npc = list(( Overworlds.NPC(self.data[start+i*0x24:start+(i+1)*0x24]) for i in range(self.header[5]) ))
            start += self.header[5] * 0x24
            self.warp = list(( Overworlds.Warp(self.data[start+i*0x14:start+(i+1)*0x14]) for i in range(self.header[6]) ))
            start += self.header[6] * 0x14
            self.trigger = list(( Overworlds.Trigger(self.data[start+i*0x16:start+(i+1)*0x16]) for i in range(self.header[7]) ))
            start += self.header[7] * 0x16
            self.extra = self.data[start:] # Not really sure about this
    
    class Furniture():
        def __init__(self, raw:bytearray):
            assert len(raw) == 0x14
            self.data = Util.byte_to_int_array(raw)
    
    class NPC():
        def __init__(self, raw:bytearray):
            assert len(raw) == 0x24
            self.data = Util.byte_to_int_array(raw)
    
    class Warp():
        def __init__(self, raw:bytearray):
            assert len(raw) == 0x14
            self.data = Util.byte_to_int_array(raw)
    
    class Trigger():
        def __init__(self, raw:bytearray):
            assert len(raw) == 0x16
            self.data = Util.byte_to_int_array(raw)

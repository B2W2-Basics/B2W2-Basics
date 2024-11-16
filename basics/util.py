from . import *

class Util:
    def byte_to_int_array(raw:bytearray) -> typing.List[int]:
        raw_hex = bytes(raw).hex()
        return list([ int(raw_hex[i:i+2], 16) for i in range(0, len(raw_hex), 2) ])

    def load_rom(path:str = 'W2ROM.nds') -> ndspy.rom.NintendoDSRom:
        assert os.path.isfile(path)
        return ndspy.rom.NintendoDSRom.fromFile(path)

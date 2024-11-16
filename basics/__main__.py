from . import *

class Basics:
    def __init__(self, rom_path:str):
        self.rom:ndspy.rom.NintendoDSRom = Util.load_rom(rom_path)

        # Parsed internal files
        self.files:typing.List[typing.Optional[Structure]] = [None]*len(self.rom.files)

        # Initialize handlers
        self.structures:typing.List[typing.Optional[Structure]] = [None]*len(self.rom.files)
        for key in handler_index:
            self.structures[handler_index[key]] = globals()[key]

        # Index ROM
        self.index_rom()

        # Convenience handlers
        for key in handler_index:
            self.__dict__[key] = self.files[handler_index[key]]

    def index_rom(self) -> None:
        for i, handler in enumerate(self.structures):
            if handler is not None:
                self.files[i] = handler(self.rom.files[i])
        
    #ctx.expand_rom(r'.\EXPANDED_ROM')
    def expand_rom(self, target_path:str):
        path = os.path.abspath(target_path)
        if not os.path.exists(path): os.makedirs(path)

        def cycle(folder:ndspy.fnt.Folder, parent:list = []) -> list:
            L = []
            for i, fileName in enumerate(folder.files):
                L.append((folder.firstID + i, '/'.join(parent + [fileName])))

            for folderName, folder in folder.folders:
                L.extend(cycle(folder, parent + [folderName]))

            return L

        for id, loc in cycle(self.rom.filenames):
            loc = loc.split('/')
            folder = os.path.abspath(os.path.join(path, '/'.join(loc[:-1])))
            file = os.path.join(folder, loc[-1])
            if not os.path.exists(folder):
                os.makedirs(folder)
            try:
                narc = ndspy.narc.NARC(self.rom.files[id])
                os.makedirs(file)
                with open(os.path.join(file, '.narc'), 'w+') as fd:
                    fd.write('%d' % id)
                for i, data in enumerate(narc.files):
                    with open(os.path.join(file, '{}.bin'.format(i)), 'wb+') as fd:
                        fd.write(data)
            except:
                with open(file, 'wb+') as fd:
                    #print(file) # These files are not NARCs
                    fd.write(self.rom.files[id])

        print('File successfully expanded!')

def main() -> None:
    ctx = Basics(r'.\W2ROM.nds')

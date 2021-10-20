import logging

class WorldMap:
    def __init__(self, level):
        logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
        self._level = level
    
    def set_map_level(self, level):
        self._level = level

    def get_map_level(self):
        return self._level
    
    def load_map(self):
        if int(self._level) > 1 and int(self._level) < 5:
            logging.info(f'Selecionado a região de "Tarant" para o level ({self._level}) do personagem')
            return ['BanditLair', 'StoneCircle', 'Coast', 'Cave']
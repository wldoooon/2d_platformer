import pygame

NEIGHBOR_OFFSET = [
    (-1, 0), (-1, -1), (0, -1), (1,-1), (1, 0), (0, 0), (-1, 1), (0, 1), (1,1)
]

PHYSICS_TILE = {'grass', 'stone'}

class Tilemap:
    def __init__(self,game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

        for i in range(100):
            self.tilemap[str(14+i) + ';8'] = {'type' : 'stone', 'variant' : 1, 'pos' : (14+i, 8)}
            self.tilemap[str(14+i) + ';9'] = {'type' : 'stone', 'variant' : 1, 'pos' : (14+i, 9)}
        for i in range(20):
            self.tilemap[str(3+i) + ';10'] = {'type' : 'stone', 'variant' : 1, 'pos' : (i+3, 10)}
            self.tilemap['14;' + str(i)] = {'type' : 'stone', 'variant' : 1, 'pos': (14, i)}

    def tile_around(self, pos, size):
        tile = []
        tile_loc = (int(pos[0] // self.tile_size), int((pos[1] + size[1]) // self.tile_size))
        for offset in NEIGHBOR_OFFSET:
            check_loc = f"{tile_loc[0] + offset[0]};{tile_loc[1] + offset[1]}"
            if check_loc in self.tilemap:
                tile.append(self.tilemap[check_loc])
        return tile

    def rec_around(self, pos, size):
        rec = []
        for tile in self.tile_around(pos, size):
            if tile['type'] in PHYSICS_TILE:
                rec.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rec

    def draw_grid(self, serf):
        for  x in range(0, serf.get_width(), 16):
            pygame.draw.line(serf, (255,255,255), (x, 0), (x, serf.get_height()))
        for y in range(0, serf.get_height(), 16):
            pygame.draw.line(serf, (255, 255, 255), (0, y), (serf.get_width(), y))

    def render(self, surf, offset=(0, 0)):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surf.blit(self.game.assets[tile['type']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))

        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))


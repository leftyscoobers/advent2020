"""
https://adventofcode.com/2020/day/20
"""

import numpy as np

# PART 1: Match the tile edges and return the tile numbers of the edges, multiplied together.
# BUT ultimately... these tiles make an image will we will probably want to reconstruct. Attempt to do both in P1.

# Parse input - tiles with "image" represented as . and # pixels
raw = {}
for line in open('20_input.txt', 'r').readlines():
    strip = line.strip()
    if len(strip) == 0:
        continue
    digits = ''.join([d for d in list(strip) if d.isdigit()])
    if len(digits) > 0:
        tile = digits
        raw[tile] = []
    if '#' in strip or '.' in strip:
        raw[tile].append(strip)


class Tile:
    def __init__(self, tid, tile):
        self.tile = tile
        self.tid = tid
        self.size = len(self.tile)

    # Convert list of strings to matrix
    def convert_to_matrix(self):
        return [list(row) for row in self.tile]

    # Vertical and horizontal flips
    def flip_vertical(self):
        return Tile(self.tid, self.tile[::-1])

    def flip_horizontal(self):
        return Tile(self.tid, [''.join(list(row)[::-1]) for row in self.tile])

    # Rotate tile
    def rotate_90(self, increments=1):
        mat = self.convert_to_matrix()
        i = 0
        while i < increments:
            new_tile = []
            for j in range(self.size):
                cur_values = [row[j] for row in mat]  # Get column values
                cur_values.reverse()
                new_tile.append(cur_values)  # Make column into row
            i += 1
            mat = new_tile
        return Tile(self.tid, [''.join(row) for row in new_tile])

    def get_edges(self):
        max_i = self.size - 1
        top = self.tile[0]
        bottom = self.tile[-1]
        mat = self.convert_to_matrix()
        right = ''.join([row[max_i] for row in self.tile])
        left = ''.join([row[0] for row in self.tile])
        return [top, right, bottom, left]

    def remove_edges(self):
        mat = self.convert_to_matrix()
        trim_sides = [''.join(row[1:(self.size - 1)]) for row in mat]
        return trim_sides[1:(self.size - 1)]


def get_flipped_edges(tile):
    return set(tile.flip_vertical().get_edges() + tile.flip_horizontal().get_edges())


all_tiles = [Tile(tid, tile) for tid, tile in raw.items()]

matches = {}
for t1 in all_tiles:
    matches[t1.tid] = []
    t1_flipped_edges = get_flipped_edges(t1)
    for t2 in all_tiles:
        if t2 == t1:
            continue
        t2_flipped_edges = get_flipped_edges(t2)
        matched_edges = t1_flipped_edges.intersection(t2_flipped_edges)
        if len(matched_edges) > 0:
            matches[t1.tid].append(t2.tid)

corners = [tid for tid, match_list in matches.items() if len(match_list) == 2]
print(f"PART 1: Corner Tile ID product = {np.prod([int(i) for i in corners])}")

# PART 2: Ultimately, find sea monsters. But first, assemble the image.
# Start with one corner and figure out it's orientation as the top left corner for now.
# Gonna be sloppy. Oh well.
t1 = Tile(corners[0], raw[corners[0]])
t1_edge = t1.flip_vertical().get_edges()  # Only flip one way - flip potential matches both ways

t1_matches = matches[t1.tid]
t1_edge_index = []
for m in t1_matches:
    mt = Tile(m, raw[m])
    mte = get_flipped_edges(mt)
    intersect = set(t1_edge).intersection(mte)
    if len(intersect) > 0:
        index = t1_edge.index(list(intersect)[0])
        t1_edge_index.append(index)

t1_rotation = min(t1_edge_index) + 1

# Now track both which tile goes where like an image key and build the image (no edges)
def get_match(tile_id, edge):
    global matches, raw
    match_ids = matches[tile_id]
    for m in match_ids:
        m_tile = Tile(m, raw[m])
        m_h = m_tile.flip_horizontal().get_edges()
        m_v = m_tile.flip_vertical().get_edges()
        if edge in m_h:
            return 'horizontal', m_h.index(edge)
        elif edge in m_v:
            return 'vertical', m_v.index(edge)
        else:
            print("No match found")
            return None

image_key = np.array([['0000'] * 12] * 12)
image_key[0, 0] = t1.tid

used_tiles = {t1.tid: t1.flip_vertical().rotate_90(increments=t1_rotation)}
image = used_tiles[t1.tid].remove_edges()

# Fill in first column by matching lowest tile "bottom", fill in rest of cols by matching to the right sides
dim = int(len(raw) ** 0.5)
for c in range(dim):
    for r in range(dim):
        if image_key[r, c] != '0000':
            break
        if c == 0:
            match_to_tile_id = image_key[(r - 1), c]
            match_to_tile = used_tiles[match_to_tile_id]
            match_edge = match_to_tile.get_edges()[2]
            orientation = 0
        else:
            match_to_tile_id = image_key[r, (c-1)]
            match_to_tile = used_tiles[match_to_tile_id]
            match_edge = match_to_tile.get_edges()[1]
            orientation = 3

        for m in matches[match_to_tile_id]:
            m_tile = Tile(m, raw[m])
            check_match = get_match(m, match_edge)
            if check_match is not None:
                print(f"Match: {m}")
                if check_match[0] == 'horizontal':
                    flipped = m_tile.flip_horizontal()
                    rotated = flipped.rotate_90(increments=(4 - abs(orientation - check_match[1])))
                else:
                    flipped = m_tile.flip_vertical()
                    rotated = flipped.rotate_90(increments=(4 - abs(orientation - check_match[1])))

                used_tiles[m] = rotated
                image_key[r, c] = m
                print(image_key)
                de_edged = flipped.remove_edges()
                if c == 0:
                    image += de_edged
                else:
                    image_rows_affected = [r * 8 + i for i in range(len(de_edged))]
                    for t_i, i_i in enumerate(image_rows_affected):
                        image[i_i] += de_edged[t_i]
                break

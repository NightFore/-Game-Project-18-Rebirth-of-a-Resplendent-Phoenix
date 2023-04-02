from Head import *

class Cursor:
    def __init__(self, game, key):
        # Global
        data = cursor_dict

        # Class
        self.game, self.main = game, game.main
        self.data, self.key = data, key
        self.dict = copy.deepcopy(self.data[self.key])

        # Rect
        self.size = self.dict["cursor_size"]
        self.size_border = self.dict["cursor_size_border"]
        self.color = self.dict["cursor_color"]
        self.color_border = self.dict["cursor_color_border"]
        self.align = self.dict["cursor_align"]

        self.init()

    def init(self, pos=None, size_scaled=None, offset=None, pos_limit=None):
        self.init_args(pos, size_scaled, offset, pos_limit)
        self.init_rect()
        self.init_path()

    def init_args(self, pos, size_scaled, offset, pos_limit):
        self.pos = [0, 0]
        if pos is not None:
            self.pos = pos

        self.size_scaled = self.size
        if size_scaled is not None:
            self.size_scaled = size_scaled

        self.offset = [0, 0]
        if offset is not None:
            self.offset = offset

        self.pos_limit = pos_limit

    def init_rect(self):
        rect = pygame.Rect(0, 0, self.size[0], self.size[1])
        self.surface_active = compute_surface(rect, self.color, self.size_border, self.color_border, self.align)
        self.surface_inactive = compute_surface(rect, None, self.size_border, self.color_border, self.align)
        self.surface = self.surface_inactive
        self.compute_rect()

    def init_path(self, follow=None):
        self.path_out = False
        self.current_follow = follow

        # Unfollow
        if self.current_follow is None:
            self.path = []
            self.surface = self.surface_inactive

        # Follow
        else:
            self.path = [self.pos.copy()]
            self.surface = self.surface_active
            self.current_graphic = self.current_follow.graphic
            self.map_pos = self.current_follow.map_move
            self.map_path = self.current_follow.map_path

    def compute_pos_scaled(self, x, y):
        pos_x = int(x * self.size_scaled[0] + self.offset[0])
        pos_y = int(y * self.size_scaled[1] + self.offset[1])
        return pos_x, pos_y

    def compute_rect(self):
        pos = self.compute_pos_scaled(self.pos[0], self.pos[1])
        self.rect = align_surface(self.surface, pos, self.align)

    def compute_new_path(self):
        # Return the first possible path to cursor position
        for map_path in self.map_path:
            if self.pos == map_path[-1]:
                return map_path.copy()

    def compute_short_path(self):
        # Find all the shortest paths
        all_short_paths = []
        short_path = self.compute_new_path()
        for map_path in self.map_path:
            if map_path[-1] == self.pos and len(short_path) == len(map_path):
                all_short_paths.append(map_path)

        # Find the longest similar path
        index_max = 0
        for new_path in all_short_paths:
            index_new = 0
            # While both paths are the same, increment index
            for index_pos in range(len(new_path)):
                if index_pos >= len(self.path) or self.path[index_pos] != new_path[index_pos]:
                    break
                else:
                    index_new += 1

            # New short path
            if index_new > index_max:
                index_max = index_new
                short_path = new_path

        return short_path.copy()

    def compute_pos(self, dx=0, dy=0):
        # Check: Minimum and maximum position
        if self.pos_limit is not None:
            limit_check = 0 <= self.pos[0] + dx <= self.pos_limit[0] - 1 and 0 <= self.pos[1] + dy <= self.pos_limit[1] - 1
        else:
            limit_check = True

        # Check: Move
        moved = limit_check and (dx, dy) != (0, 0)
        if moved:
            self.pos[0] += dx
            self.pos[1] += dy
            self.compute_rect()

        # Check: Path
        if moved and self.current_follow:
            # Inside
            if self.pos in self.map_pos:
                # Reset
                if self.path_out:
                    self.path_out = False

                    # Find a new shortest and similar path
                    if self.pos != self.path[-1] or self.pos not in self.path:
                        self.path = self.compute_short_path()

                # Add
                elif self.pos not in self.path:
                    self.path.append(self.pos.copy())

                    # Check: Shortest path
                    if len(self.compute_new_path()) < len(self.path):
                        self.path = self.compute_short_path()

                # Remove
                else:
                    end_index = self.path.index(self.pos)
                    self.path = self.path[0:end_index+1]

            # Outside
            else:
                self.path_out = True

        # Unit movement
        if moved:
            if len(self.path) == 1:
                self.current_follow.compute_movement(self.path[0][0], self.path[0][1])

            elif len(self.path) > 1:
                self.current_follow.compute_movement(self.path[-1][0], self.path[-1][1])
                dx = self.path[-1][0] - self.path[-2][0]
                dy = self.path[-1][1] - self.path[-2][1]

                # Down
                if dy == 1:
                    self.current_graphic.compute_index_images(0)
                # Left
                if dx == -1:
                    self.current_graphic.compute_index_images(1)
                # Right
                if dx == 1:
                    self.current_graphic.compute_index_images(2)
                # Up
                if dy == -1:
                    self.current_graphic.compute_index_images(3)


    def compute_movement_legacy(self):
        # Graphic: update index
        if len(self.path) > 1:
            dx = self.path[1][0] - self.path[0][0]
            dy = self.path[1][1] - self.path[0][1]

            # Down
            if dy == 1:
                self.current_graphic.compute_index_images(0)
            # Left
            if dx == -1:
                self.current_graphic.compute_index_images(1)
            # Right
            if dx == 1:
                self.current_graphic.compute_index_images(2)
            # Up
            if dy == -1:
                self.current_graphic.compute_index_images(3)

    def update(self):
        pass

    def draw(self):
        # Path
        for x, y in self.path:
            pos_x, pos_y = self.compute_pos_scaled(x, y)
            rect = pygame.Rect(pos_x, pos_y, self.size_scaled[0], self.size_scaled[1])
            pygame.draw.rect(self.game.gameDisplay, CYAN, rect, 1)

        # Cursor
        self.game.gameDisplay.blit(self.surface, self.game.compute_camera_offset(self.rect))

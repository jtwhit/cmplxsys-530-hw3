import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Tile:
    def __init__(self, position):
        self.color = 'white'
        self.patch = patches.Rectangle(position, 1, 1, linewidth=0, facecolor=self.color)
        self.patch.set_zorder(1)
        self.patch.set_animated(True)

    def set_color(self, color):
        self.color = color
        self.redraw()

    def redraw(self):
        self.patch.set_color(self.color)

class Ant:
    def __init__(self):
        # 0 north, 1 east, 2 south, 3 west
        self.direction = 1
        self.x = 0
        self.y = 0
        self.patch = patches.FancyArrowPatch((0, 0), (0, 0), linewidth=0, mutation_scale=50, facecolor='r')
        self.patch.set_zorder(2)
        self.patch.set_animated(True)

    def turn(self, tile):
        if tile.color == 'black':
            turn_dir = 1
        else:
            turn_dir = -1
        
        self.direction = (self.direction + turn_dir) % 4
        self.redraw()

    def recolor_tile(self, tile):
        if tile.color == 'black':
            tile.set_color('white')
        else:
            tile.set_color('black')

    def move(self):
        if self.direction == 0:
            self.y += 1
        elif self.direction == 1:
            self.x += 1
        elif self.direction == 2:
            self.y -= 1
        else:
            self.x -= 1
        
        self.redraw()

    def zoom(self, amount):
        self.patch.set_mutation_scale(250 / amount)

    def redraw(self):
        if self.direction == 0:
            start = (self.x + 0.5, self.y + 0.5)
            end = (self.x + 0.5, self.y + 0.9)
        elif self.direction == 1:
            start = (self.x + 0.5, self.y + 0.5)
            end = (self.x + 0.9, self.y + 0.5)
        elif self.direction == 2:
            start = (self.x + 0.5, self.y + 0.5)
            end = (self.x + 0.5, self.y + 0.1)
        else:
            start = (self.x + 0.5, self.y + 0.5)
            end = (self.x + 0.1, self.y + 0.5)
        
        self.patch.set_positions(start, end)

def get_tile(axes, tiles, position):
    if position in tiles:
        return tiles[position]
    
    new_tile = Tile(position)
    axes.add_patch(new_tile.patch)
    tiles[position] = new_tile
    return new_tile

def zoom(max, axes, ant):
    axes.set_xlim([-max, max])
    axes.set_ylim([-max, max])
    ant.zoom(max)

def redraw_all(figure, ant, tiles):
    figure.canvas.draw()

    for _, tile in tiles.items():
        tile.patch.draw(figure.canvas.get_renderer())
    ant.patch.draw(figure.canvas.get_renderer())

def main():
    matplotlib.rcParams['toolbar'] = 'None'
    figure = plt.figure(1, figsize=(5, 5))
    figure.canvas.set_window_title('Langton\'s Ant')

    axes = figure.add_axes([0, 0, 1, 1])
    axes.set_axis_off()

    current_max = 5

    text_figure = plt.figure(2, figsize=(1, 0.3))
    text_figure.canvas.set_window_title('Ticks')
    text_axes = text_figure.add_axes([0, 0, 1, 1])
    text_axes.set_axis_off()
    text = plt.text(0.5, 0.5, '', horizontalalignment='center', verticalalignment='center')

    plt.show(block=False)

    figure.canvas.draw()

    tiles = {}

    ant = Ant()
    axes.add_patch(ant.patch)
    zoom(current_max, axes, ant)

    ticks = 0
    while (len(plt.get_fignums()) == 2):
        text.set_text('Ticks: %d' % ticks)
        text_figure.canvas.draw()

        max_pos = max(abs(ant.x), abs(ant.y))
        if max_pos >= current_max:
            current_max *= 2
            zoom(current_max, axes, ant)
            redraw_all(figure, ant, tiles)

        tile = get_tile(axes, tiles, (ant.x, ant.y))
        ant.turn(tile)
        ant.recolor_tile(tile)
        ant.move()
        axes.draw_artist(tile.patch)
        axes.draw_artist(ant.patch)

        figure.canvas.blit(axes.bbox)
        figure.canvas.flush_events()

        ticks += 1

    return

if __name__ == '__main__':
    main()

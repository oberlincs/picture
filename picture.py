"""
Create and display simple pictures. Supported color names can be found
at the bottom of
https://pillow.readthedocs.io/en/stable/_modules/PIL/ImageColor.html

Example usage:
import picture

picture.new_picture(400, 300)  # Create a blank, 800x600 picture
picture.draw_text(200, 20, "A fun little picture!", 16)
picture.set_fill_color("burlywood")
picture.set_outline_color("dark red")
picture.set_pen_width(8)

picture.fill_rectangle(10, 30, 100, 200)
picture.set_outline_color("green")
picture.draw_square(20, 40, 100)
picture.display()
picture.delay(2000)  # Wait for 2000 ms = 2 seconds

picture.set_position(100, 150)
picture.set_outline_color("purple")
picture.set_direction(0)
picture.draw_forward(100)
picture.rotate(30)
picture.draw_forward(75)
picture.rotate(30)
picture.draw_forward(50)
picture.rotate(30)
picture.draw_forward(25)
picture.rotate(30)
picture.draw_forward(12)

picture.set_pen_width(2)
picture.set_outline_color("aquamarine")
picture.draw_polygon([(200, 100), (250, 100), (225, 150)])

picture.save_picture("example.png") # Save it to a file
picture.display()
"""

# pylint: disable=invalid-name,global-statement,too-few-public-methods
import math
import tkinter

from PIL import Image, ImageColor, ImageDraw, ImageFont, ImageTk

__all__ = [
    "blank_image",
    "change_picture_size",
    "delay",
    "display",
    "draw_arc",
    "draw_chord",
    "draw_circle",
    "draw_forward",
    "draw_image",
    "draw_line",
    "draw_oval",
    "draw_polygon",
    "draw_rectangle",
    "draw_square",
    "draw_text",
    "fill_chord",
    "fill_circle",
    "fill_oval",
    "fill_polygon",
    "fill_rectangle",
    "fill_square",
    "get_blue",
    "get_direction",
    "get_fill_color",
    "get_green",
    "get_outline_color",
    "get_pen_width",
    "get_pixel",
    "get_position",
    "get_red",
    "image_height",
    "image_width",
    "load_image",
    "new_picture",
    "parse_color",
    "rotate",
    "run",
    "save_image",
    "save_picture",
    "set_blue",
    "set_direction",
    "set_fill_color",
    "set_green",
    "set_outline_color",
    "set_pen_width",
    "set_pen_x",
    "set_pen_y",
    "set_pixel",
    "set_position",
    "set_red",
]


def parse_color(*color):
    """
    Parses the various ways colors may be specified and returns a
    (red, green, blue) tuple.
    Examples:
        picture.parse_color("aquamarine")    # returns (127, 255, 212)
        picture.parse_color((245, 245, 220)) # "beige"; returns (245, 245, 220)
        picture.parse_color(95, 158, 160)    # "CadetBlue"; returns (95, 158, 160)
        picture.parse_color("#FF802A")       # returns (255, 128, 42)
    """
    if len(color) == 1 and isinstance(color[0], str):
        return ImageColor.getrgb(color[0])
    if len(color) == 1 \
       and isinstance(color, tuple) \
       and all(isinstance(channel, int) for channel in color[0]):
        rgb = color[0]
    elif len(color) == 3 \
            and all(isinstance(channel, int) for channel in color):
        rgb = tuple(channel for channel in color)
    else:
        raise TypeError("Expected a string naming a color, 3 ints, or a tuple "
                        "containing 3 ints")
    if any(channel < 0 or channel > 255 for channel in rgb):
        raise ValueError("Invalid color component.\n"
                         "Color components must be between 0 and 255 but given"
                         " {}".format(repr(rgb)))
    return rgb


ROOT = None
FRAME = None
CANVAS = None
IMAGE = None
DRAW = None
TK_IMAGE = None

OUTLINE_COLOR = parse_color("black")
FILL_COLOR = parse_color("white")
PEN_WIDTH = 1
PEN_POSITION = (0, 0)
PEN_ROTATION = 0


def new_picture(width, height):
    """
    Create a new picture with the given width and height, clearing the existing
    one.
    Examples:
        picture.new_picture(800, 600) # Creates an 800 x 600 blank picture
    """
    global ROOT, FRAME, CANVAS, IMAGE, DRAW

    if ROOT is None:
        ROOT = tkinter.Tk()
        FRAME = tkinter.Frame(ROOT, None, borderwidth=0)
        FRAME.grid()

    if CANVAS is None:
        CANVAS = tkinter.Canvas(ROOT, width=width, height=height,
                                background="white", bd=0,
                                highlightthickness=0)
        CANVAS.grid()
    else:
        CANVAS.delete('all')
        change_picture_size(width, height)
    IMAGE = Image.new("RGB", (width, height), color=(255, 255, 255))
    DRAW = ImageDraw.Draw(IMAGE)


def save_picture(path):
    """
    Save the current picture to a file.
    WARNING: This _will_ overwrite existing files so be CAREFUL!
    Example:
        picture.new_picture(100, 100)
        picture.draw_rectangle(10, 10, 50, 50)
        picture.save_picture("rectangle.png")
    """
    IMAGE.save(path)


def change_picture_size(width, height):
    """
    Change the size of the picture to be width and height.
    """
    CANVAS.config(width=width, height=height)


def set_position(*position):
    """
    Set the current drawing position.
    Examples:
        picture.set_position(10, 20)
        picture.set_position((10, 20))
    """
    global PEN_POSITION
    if len(position) == 1 \
       and isinstance(position[0], tuple) \
       and all(isinstance(coord, int) for coord in position[0]):
        PEN_POSITION = position[0]
    elif len(position) == 2 \
            and all(isinstance(coord, int) for coord in position):
        PEN_POSITION = (position[0], position[1])
    else:
        raise TypeError("set_position() expected either a single pair of ints "
                        "or two intarguments")


def get_position():
    """
    Returns the current drawing position.
    Example:
        pos = picture.get_position()
        picture.set_position(10, 20)
        # Perform some drawing at (10, 20)
        picture.set_position(pos)
    """
    return PEN_POSITION


def set_pen_x(x):
    """
    Set the x-coordinate of the pen's position.
    Example:
        picture.set_pen_x(10)
    """
    global PEN_POSITION
    PEN_POSITION = (x, PEN_POSITION[1])


def set_pen_y(y):
    """
    Set the y-coordinate of the pen's position.
    Example:
        picture.set_pen_y(20)
    """
    global PEN_POSITION
    PEN_POSITION = (PEN_POSITION[0], y)


def set_pen_width(width):
    """
    Set the width of the pen.
    Example:
        picture.set_pen_width(10)
        picture.draw_forward(10)
    """
    global PEN_WIDTH
    PEN_WIDTH = width


def get_pen_width():
    """
    Returns the current pen width.
    Example:
        width = picture.get_pen_width()
    """
    return PEN_WIDTH


def rotate(theta):
    """
    Rotate the current drawing direction by theta degrees.
    Example:
        picture.rotate(45)
        picture.draw_forward(10)
        picture.rotate(-45)
        picture.draw_forward(10)
    """
    global PEN_ROTATION
    PEN_ROTATION += theta
    PEN_ROTATION %= 360


def set_direction(theta):
    """
    Set the current drawing direction to theta degrees.
    Example:
        picture.set_direction(45)
        picture.draw_forward(20)
    """
    global PEN_ROTATION
    PEN_ROTATION = theta
    PEN_ROTATION %= 360


def get_direction():
    """
    Return the current drawing direction.
    Example:
        theta = picture.get_direction()
        picture.set_direction(180)
        picture.draw_forward(10)
        picture.set_direction(theta)
    """
    return PEN_ROTATION


def draw_forward(distance):
    """
    Draw a line starting from the current pen position in the current direction
    the given distance.
    Example:
        picture.set_direction(0)
        picture.set_position(100, 100)
        picture.draw_forward(10)
        picture.rotate(90)
        picture.draw_forward(10)
        picture.rotate(90)
        picture.draw_forward(10)
    """
    global PEN_POSITION
    radian = math.radians(PEN_ROTATION)
    start_x = PEN_POSITION[0]
    start_y = PEN_POSITION[1]
    end_x = start_x + math.cos(radian) * distance
    end_y = start_y + math.sin(radian) * distance
    PEN_POSITION = (end_x, end_y)
    draw_line(start_x, start_y, end_x, end_y)


def set_fill_color(*color):
    """
    Set the fill color. The arguments are one of a string naming the color,
    a (red, green, blue) tuple, or three arguments specifying red, green, and
    blue.
    Examples:
        picture.set_fill_color("aquamarine")
        picture.set_fill_color((245, 245, 220)) # "beige"
        picture.set_fill_color(95, 158, 160) # "CadetBlue"
    """
    global FILL_COLOR
    FILL_COLOR = parse_color(*color)


def get_fill_color():
    """
    Returns the current fill color.
    Example:
        current_color = picture.get_fill_color()
        picture.set_fill_color("red")
        # Do some drawing in red.
        picture.set_fill_color(current_color)
    """
    return FILL_COLOR


def set_outline_color(*color):
    """
    Set the outline color. The arguments are one of a string naming the color,
    a (red, green, blue) tuple, or three arguments specifying red, green, and
    blue.
    Examples:
        picture.set_outline_color("aquamarine")
        picture.set_outline_color((245, 245, 220)) # "beige"
        picture.set_outline_color(95, 158, 160) # "CadetBlue"
    """
    global OUTLINE_COLOR
    OUTLINE_COLOR = parse_color(*color)


def get_outline_color():
    """
    Returns the current outline color as a (red, green, blue) triple.
    Example:
        current_color = picture.get_outline_color()
        picture.set_outline_color("red")
        # Do some drawing in red outline.
        picture.set_outline_color(current_color)
    """
    return OUTLINE_COLOR


def display():
    """
    Draw the current picture.
    Example:
        picture.display()
    """
    global TK_IMAGE
    TK_IMAGE = ImageTk.PhotoImage(IMAGE)
    CANVAS.delete('all')
    CANVAS.create_image(0, 0, image=TK_IMAGE, anchor="nw")
    CANVAS.update()


def delay(milliseconds):
    """
    Pause for the given number of milliseconds
    Example:
        picture.delay(500) # Half a second
    """
    CANVAS.after(milliseconds)


def draw_oval(x, y, hrad, vrad):
    """
    Draw an oval centered at (x, y) with horizantal radius hrad and vertical
    radius vrad
    in the current outline color.
    Example:
        picture.draw_oval(100, 200, 10, 20)
    """
    DRAW.ellipse([(x - hrad, y - vrad), (x + hrad, y + vrad)],
                 outline=OUTLINE_COLOR, width=PEN_WIDTH)


def fill_oval(x, y, hrad, vrad):
    """
    Fill an oval centered at (x, y) with horizantal radius hrad and vertical
    radius vrad with the current fill color.
    Example:
        picture.fill_oval(100, 200, 10, 20)
    """
    DRAW.ellipse([(x - hrad, y - vrad), (x + hrad, y + vrad)],
                 fill=FILL_COLOR,
                 outline=OUTLINE_COLOR,
                 width=PEN_WIDTH)

def draw_circle(x, y, r):
    """
    Draw a circle centered at (x, y) with radius r in the current outline
    color.
    Example:
        picture.draw_circle(100, 200, 10)
    """
    draw_oval(x, y, r, r)


def fill_circle(x, y, r):
    """
    Fill a circle centered at (x, y) radius r with the current fill color.
    Example:
        picture.fill_circle(100, 200, 10)
    """
    fill_oval(x, y, r, r)


def draw_arc(x, y, radius, start, end):
    """
    Draw an arc (a portion of a circle). The circle is centered at (x, y) and
    has the given radius. The portion drawn starts at the start angle
    and ends at the end angle.
    Example:
        picture.draw_arc(100, 100, 25, 45, 90) # 45 degrees to 90 degrees
    """
    DRAW.arc([(x - radius, y - radius), (x + radius, y + radius)],
             start,
             end,
             fill=OUTLINE_COLOR,
             width=PEN_WIDTH)

def draw_chord(x, y, radius, start, end):
    """
    Draw an arc (a portion of a circle) and connect the two end points with a
    line. The circle is centered at (x, y) and has the given radius. The
    portion drawn starts at the start angle and ends at the end angle.
    Example:
        picture.draw_chord(100, 100, 25, 45, 90) # 45 degrees to 90 degrees
    """
    DRAW.chord([(x - radius, y - radius), (x + radius, y + radius)],
               start,
               end,
               outline=OUTLINE_COLOR,
               width=PEN_WIDTH)

def fill_chord(x, y, radius, start, end):
    """
    Fill an arc (a portion of a circle) with connected end points in the fill
    color. The circle is centered at (x, y) and has the given radius. The
    portion drawn starts at the start angle and ends at the end angle.
    Example:
        picture.fill_chord(100, 100, 25, 45, 90) # 45 degrees to 90 degrees
    """
    DRAW.chord([(x - radius, y - radius), (x + radius, y + radius)],
               start,
               end,
               outline=OUTLINE_COLOR,
               fill=FILL_COLOR,
               width=PEN_WIDTH)

def draw_rectangle(x, y, w, h):
    """
    Draw a rectangle with corners (x, y), (x+w, y), (x, y+h), and (x+w, y+h) in
    the current outline color.
    Example:
        picture.draw_rectangle(10, 20, 100, 50)
    """
    DRAW.rectangle([(x, y), (x + w, y + h)],
                   outline=OUTLINE_COLOR,
                   width=PEN_WIDTH)


def fill_rectangle(x, y, w, h):
    """
    Fill a rectangle with corners (x, y), (x+w, y), (x, y+h), and (x+w, y+h)
    with the current fill color.
    Example:
        picture.fill_rectangle(10, 20, 100, 50)
    """
    DRAW.rectangle([(x, y), (x + w, y + h)],
                   fill=FILL_COLOR,
                   outline=OUTLINE_COLOR,
                   width=PEN_WIDTH)


def draw_square(x, y, side):
    """
    Draw a square with corners (x, y), (x+side, y), (x, y+side), and
    (x+side, y+side) in the current outline color.
    Example:
        picture.draw_square(10, 20, 100, 50)
    """
    draw_rectangle(x, y, side, side)


def fill_square(x, y, side):
    """
    Fill a square with corners (x, y), (x+side, y), (x, y+side), and
    (x+side, y+side) with the current fill color.
    Example:
        picture.fill_square(10, 20, 100)
    """
    fill_rectangle(x, y, side, side)


def draw_polygon(vertices):
    """
    Draw a polygon defined by a list of vertices in the current outline color.
    Example:
        picture.draw_polygon([(10, 10), (20, 10), (15, 20)])
    """
    DRAW.line(vertices + [vertices[0]],
              fill=OUTLINE_COLOR,
              width=PEN_WIDTH)


def fill_polygon(vertices):
    """
    Fill a polygon defined by a list of vertices in the current outline color.
    Example:
        picture.fill_polygon([(10, 10), (20, 10), (15, 20)])
    """
    DRAW.polygon(vertices,
                 fill=FILL_COLOR,
                 outline=None)
    DRAW.line(vertices + [vertices[0]],
              fill=OUTLINE_COLOR,
              width=PEN_WIDTH)


def draw_line(x1, y1, x2, y2):
    """
    Draws a line from (x1, y1) to (x2, y2) using the current outline color and
    pen width.
    Example:
        picture.draw_line(10, 20, 100, 100)
    """
    DRAW.line([(x1, y1), (x2, y2)],
              fill=OUTLINE_COLOR,
              width=PEN_WIDTH)

def draw_text(x, y, text, font_size):
    """
    Draws the text at (x, y) using the font_size in the current outline color.
    Example:
        picture.draw_text(10, 20, "Hello!", 16)
    """
    try:
        font = ImageFont.truetype("Arial.ttf", font_size)
    except OSError:
        font = ImageFont.truetype('FreeSans.ttf', font_size)

    DRAW.text((x, y),
              text,
              font=font,
              fill=OUTLINE_COLOR,
              width=PEN_WIDTH)


class Picture():
    """
    This class holds an PIL.Image as well as a PixelAccess for the image.
    """

    def __init__(self, image):
        """
        Create a new picture from a PIL.Image.
        """
        self.image = image
        self.px = image.load()


def blank_image(width, height):
    """
    Returns a blank image with the given width and height.
    Example:
        image = picture.blank_image(200, 300)
        for y in range (image_height(image)):
            for x in range(image_width(image)):
                picture.set_pixel(image, x, y, (255, 0, 0))
        picture.draw_image(100, 100, image)
    """
    return Picture(Image.new("RGB", (width, height), color=(255, 255, 255)))


def load_image(path):
    """
    Create an image by loading it from the file system at the given path.
    Example:
        image = picture.load_image("pretty_image.png")
        picture.draw_image(100, 100, image) # Draws the image at (100, 100).
    """
    image = Image.open(path)
    if image.mode == "RGB":
        pass
    elif image.mode == "RGBA":
        # Code adapted from http://stackoverflow.com/a/9459208/284318
        image.load()  # needed for split()
        new_image = Image.new('RGB', image.size, color=(255, 255, 255))
        new_image.paste(image, mask=image.split()[3])  # 3 is the alpha channel
        image = new_image
    else:
        image = image.convert("RGB")
    return Picture(image)


def save_image(image, path):
    """
    Save an image by writing it to the file system.
    WARNING: This _will_ overwrite existing files so be CAREFUL!
    Example:
        image = picture.blank_image(200, 200)
        for idx in range(200):
            picture.set_pixel(image, idx, idx, (25, 183, 200))
        picture.save_image("fancy.png")
    """
    image.image.save(path)


def image_width(image):
    """
    Returns the number of pixels in each row of the image.
    Example:
        image = picture.load_image("pretty_image.png")
        width = picture.image_width(image)
        height = picture.image_height(image)
    """
    return image.image.width


def image_height(image):
    """
    Returns the number of pixels in each column of the image.
    Example:
        image = picture.load_image("pretty_image.png")
        width = picture.image_width(image)
        height = picture.image_height(image)
    """
    return image.image.height


def get_pixel(image, x, y):
    """
    Returns the pixel at (x, y) as a (red, green, blue) tuple.
    Example:
        image = picture.load_image("pretty_image.png")
        color = picture.get_pixel(image, 0, 0) # Top left pixel
    """
    return image.px[(x, y)]


def get_red(image, x, y):
    """
    Returns the red value for the pixel at (x, y).
    Example:
        image = picture.load_image("pretty_image.png")
        red_val = picture.get_red(image, 0, 0) # Top left pixel
    """
    return image.px[(x, y)][0]


def get_green(image, x, y):
    """
    Returns the green value for the pixel at (x, y).
    Example:
        image = picture.load_image("pretty_image.png")
        green_val = picture.get_green(image, 0, 0) # Top left pixel
    """
    return image.px[(x, y)][1]


def get_blue(image, x, y):
    """
    Returns the blue value for the pixel at (x, y).
    Example:
        image = picture.load_image("pretty_image.png")
        green_val = picture.get_blue(image, 0, 0) # Top left pixel
    """
    return image.px[(x, y)][2]


def set_red(image, x, y, val):
    """
    Sets the red value for the pixel at (x, y) to val.
    Example:
        picture.set_red(image, 10, 10, 255) #All the way red
    """
    red, green, blue = image.px[(x, y)]
    image.px[(x, y)] = (val, green, blue)


def set_green(image, x, y, val):
    """
    Sets the green value for the pixel at (x, y) to val.
    Example:
        picture.set_green(image, 10, 10, 255) #All the way green
    """
    red, green, blue = image.px[(x, y)]
    image.px[(x, y)] = (red, val, blue)


def set_blue(image, x, y, val):
    """
    Sets the blue value for the pixel at (x, y) to val.
    Example:
        picture.set_blue(image, 10, 10, 255) #All the way blue
    """
    red, green, blue = image.px[(x, y)]
    image.px[(x, y)] = (red, green, val)


def set_pixel(image, x, y, *color):
    """
    Sets the pixel at location (x, y) in image to be color.
    Examples:
        picture.set_pixel(image, 10, 10, "red")
        picture.set_pixel(image, 20, 15, (123, 255, 0))
        picture.set_pixel(image, 100, 10, 0, 0, 0) # black
    """
    image.px[(x, y)] = parse_color(*color)


def draw_image(x, y, image):
    """
    Draws the image at (x, y).
    Example:
        image = picture.load_image("pretty_image.png")
        width = picture.image_width(image)
        height = picture.image_height(image)
        picture.new_picture(width, height)
        picture.draw_image(0, 0, image)
    """
    IMAGE.paste(image.image, box=(x, y))


def run():
    """
    Runs the program until the window is closed.
    Example:
        picture.new_picture(800, 600)
        picture.draw_rectangle(100, 100, 50, 50)
        picture.run()
    """
    display()
    ROOT.mainloop()

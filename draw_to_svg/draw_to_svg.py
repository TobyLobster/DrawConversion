#! /usr/bin/env python3

"""draw_to_svg.py

Converts Draw files to SVG files.

It is a command line tool written in Python. It aims to be as accurate and comprehensive as
possible, while still being easy to use. If you find issues, please let me know, preferably with an
example file.

Requirements:
There is only one dependency required, the Python Image Library ('Pillow'):
        https://pillow.readthedocs.io/en/latest/installation.html

TobyLobster, 2023
"""

from PIL import Image
from PIL import ImageFont
from pathlib import Path
from configparser import ConfigParser
import argparse
import base64
import io
import math
import os
import re
import struct
import sys
import copy

# Just for fun, use colour names where possible
colour_names = {
    0xF0F8FF : "AliceBlue",
    0xFAEBD7 : "AntiqueWhite",
    0x00FFFF : "Aqua",
    0x7FFFD4 : "Aquamarine",
    0xF0FFFF : "Azure",
    0xF5F5DC : "Beige",
    0xFFE4C4 : "Bisque",
    0x000000 : "Black",
    0xFFEBCD : "BlanchedAlmond",
    0x0000FF : "Blue",
    0x8A2BE2 : "BlueViolet",
    0xA52A2A : "Brown",
    0xDEB887 : "BurlyWood",
    0x5F9EA0 : "CadetBlue",
    0x7FFF00 : "Chartreuse",
    0xD2691E : "Chocolate",
    0xFF7F50 : "Coral",
    0x6495ED : "CornflowerBlue",
    0xFFF8DC : "Cornsilk",
    0xDC143C : "Crimson",
    0x00FFFF : "Cyan",
    0x00008B : "DarkBlue",
    0x008B8B : "DarkCyan",
    0xB8860B : "DarkGoldenRod",
    0xA9A9A9 : "DarkGray",
    0xA9A9A9 : "DarkGrey",
    0x006400 : "DarkGreen",
    0xBDB76B : "DarkKhaki",
    0x8B008B : "DarkMagenta",
    0x556B2F : "DarkOliveGreen",
    0xFF8C00 : "DarkOrange",
    0x9932CC : "DarkOrchid",
    0x8B0000 : "DarkRed",
    0xE9967A : "DarkSalmon",
    0x8FBC8F : "DarkSeaGreen",
    0x483D8B : "DarkSlateBlue",
    0x2F4F4F : "DarkSlateGray",
    0x2F4F4F : "DarkSlateGrey",
    0x00CED1 : "DarkTurquoise",
    0x9400D3 : "DarkViolet",
    0xFF1493 : "DeepPink",
    0x00BFFF : "DeepSkyBlue",
    0x696969 : "DimGray",
    0x696969 : "DimGrey",
    0x1E90FF : "DodgerBlue",
    0xB22222 : "FireBrick",
    0xFFFAF0 : "FloralWhite",
    0x228B22 : "ForestGreen",
    0xFF00FF : "Fuchsia",
    0xDCDCDC : "Gainsboro",
    0xF8F8FF : "GhostWhite",
    0xFFD700 : "Gold",
    0xDAA520 : "GoldenRod",
    0x808080 : "Gray",
    0x808080 : "Grey",
    0x008000 : "Green",
    0xADFF2F : "GreenYellow",
    0xF0FFF0 : "HoneyDew",
    0xFF69B4 : "HotPink",
    0xCD5C5C : "IndianRed",
    0x4B0082 : "Indigo",
    0xFFFFF0 : "Ivory",
    0xF0E68C : "Khaki",
    0xE6E6FA : "Lavender",
    0xFFF0F5 : "LavenderBlush",
    0x7CFC00 : "LawnGreen",
    0xFFFACD : "LemonChiffon",
    0xADD8E6 : "LightBlue",
    0xF08080 : "LightCoral",
    0xE0FFFF : "LightCyan",
    0xFAFAD2 : "LightGoldenRodYellow",
    0xD3D3D3 : "LightGray",
    0xD3D3D3 : "LightGrey",
    0x90EE90 : "LightGreen",
    0xFFB6C1 : "LightPink",
    0xFFA07A : "LightSalmon",
    0x20B2AA : "LightSeaGreen",
    0x87CEFA : "LightSkyBlue",
    0x778899 : "LightSlateGray",
    0x778899 : "LightSlateGrey",
    0xB0C4DE : "LightSteelBlue",
    0xFFFFE0 : "LightYellow",
    0x00FF00 : "Lime",
    0x32CD32 : "LimeGreen",
    0xFAF0E6 : "Linen",
    0xFF00FF : "Magenta",
    0x800000 : "Maroon",
    0x66CDAA : "MediumAquaMarine",
    0x0000CD : "MediumBlue",
    0xBA55D3 : "MediumOrchid",
    0x9370DB : "MediumPurple",
    0x3CB371 : "MediumSeaGreen",
    0x7B68EE : "MediumSlateBlue",
    0x00FA9A : "MediumSpringGreen",
    0x48D1CC : "MediumTurquoise",
    0xC71585 : "MediumVioletRed",
    0x191970 : "MidnightBlue",
    0xF5FFFA : "MintCream",
    0xFFE4E1 : "MistyRose",
    0xFFE4B5 : "Moccasin",
    0xFFDEAD : "NavajoWhite",
    0x000080 : "Navy",
    0xFDF5E6 : "OldLace",
    0x808000 : "Olive",
    0x6B8E23 : "OliveDrab",
    0xFFA500 : "Orange",
    0xFF4500 : "OrangeRed",
    0xDA70D6 : "Orchid",
    0xEEE8AA : "PaleGoldenRod",
    0x98FB98 : "PaleGreen",
    0xAFEEEE : "PaleTurquoise",
    0xDB7093 : "PaleVioletRed",
    0xFFEFD5 : "PapayaWhip",
    0xFFDAB9 : "PeachPuff",
    0xCD853F : "Peru",
    0xFFC0CB : "Pink",
    0xDDA0DD : "Plum",
    0xB0E0E6 : "PowderBlue",
    0x800080 : "Purple",
    0x663399 : "RebeccaPurple",
    0xFF0000 : "Red",
    0xBC8F8F : "RosyBrown",
    0x4169E1 : "RoyalBlue",
    0x8B4513 : "SaddleBrown",
    0xFA8072 : "Salmon",
    0xF4A460 : "SandyBrown",
    0x2E8B57 : "SeaGreen",
    0xFFF5EE : "SeaShell",
    0xA0522D : "Sienna",
    0xC0C0C0 : "Silver",
    0x87CEEB : "SkyBlue",
    0x6A5ACD : "SlateBlue",
    0x708090 : "SlateGray",
    0x708090 : "SlateGrey",
    0xFFFAFA : "Snow",
    0x00FF7F : "SpringGreen",
    0x4682B4 : "SteelBlue",
    0xD2B48C : "Tan",
    0x008080 : "Teal",
    0xD8BFD8 : "Thistle",
    0xFF6347 : "Tomato",
    0x40E0D0 : "Turquoise",
    0xEE82EE : "Violet",
    0xF5DEB3 : "Wheat",
    0xFFFFFF : "White",
    0xF5F5F5 : "WhiteSmoke",
    0xFFFF00 : "Yellow",
    0x9ACD32 : "YellowGreen",
}

debug = 0
debug_index = 0
epsilon = 0.0001        # shortest distance we care about, to avoid division by zero (in SVG points)

def is_debug_active():
    global debug_index

    #return(debug_index == 342)
    return(True)

# Utility messaging functions
def error(message):
    print("ERROR:", message, file=sys.stderr)

def warning(message):
    print("WARNING:", message, file=sys.stderr)

def message(verbose_level, message, end="\n"):
    global convertor
    if is_debug_active():
        if convertor.config.verbose_level >= verbose_level:
            print(message, end=end)

# Maths routines
def lerp(x1: float, x2: float, t: float):
    """Perform linear interpolation between x1 and x2"""
    return x1 * (1-t) + x2 * t

def bezier(a, b, c, d, t):
    t2 = t * t
    t3 = t2 * t
    mt = 1-t
    mt2 = mt * mt
    mt3 = mt2 * mt
    return a*mt3 + b*mt2*t*3 + c*mt*t2*3 + d*t3

class Point:
    """Represents a 2D point"""

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Point(self.x * other, self.y * other)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y

    def __imul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            self.x *= other
            self.y *= other

    def lerp(self, other, t):
        return Point(lerp(self.x, other.x, t), lerp(self.y, other.y, t))

    def dist(self, other):
        return math.sqrt((other.x - self.x)*(other.x - self.x) +
                         (other.y - self.y)*(other.y - self.y))

    def __repr__(self):
        return "({0},{1})".format("{0:.4f}".format(self.x), "{0:.4f}".format(self.y))

class Mat:
    """Represents a 3x3 matrix of the form:
        (a, c, e)
        (b, d, f)
        (0, 0, 1)"""

    def __init__(self, a = 1, b = 0, c = 0, d = 1, e = 0, f = 0):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f

    def matmat(self,m):
        """Matrix multiplication"""

        return Mat(self.a * m.a + self.b * m.b,
                   self.b * m.a + self.d * m.b,
                   self.a * m.c + self.c * m.d,
                   self.b * m.c + self.d * m.d,
                   self.a * m.e + self.c * m.f + self.e,
                   self.b * m.e + self.d * m.f + self.f)

    def matpoint(self, point):
        """Transform a point from one coordinate space to another"""

        return Point(self.a * point.x + self.c * point.y + self.e,
                     self.b * point.x + self.d * point.y + self.f)

    # Decompose matrix. See https://math.stackexchange.com/a/13165
    # https://math.stackexchange.com/questions/13150/extracting-rotation-scale-values-from-2d-transformation-matrix
    def decompose(self):
        delta = self.a * self.d - self.b * self.c

        # Default values
        translation = Point(self.e, self.f)
        rotation = 0
        scale = Point(0,0)
        skew = Point(0,0)

        # Apply the QR-like decomposition.
        r = math.sqrt(self.a * self.a + self.b * self.b)

        if (r != 0):
            scale = Point(r, delta / r)
        elif (s != 0):
            s = math.sqrt(self.c * self.c + self.d * self.d)
            scale = Point(delta / s, s)

        rotation = math.atan2(self.b, self.a);
        skew.x = math.atan2(self.c, self.d) + rotation;
        skew.y = 0;

        # Reverse the rotation angles (due to the reflection when converting from Draw coordinate space to SVG coordinate space)
        rotation = -rotation
        skew.x = -skew.x

        return (translation, rotation, skew, scale)

    def __repr__(self):
        return "({0},{1},{2}\n{3},{4},{5}\n0, 0, 1)".format(self.a, self.c, self.e, self.b, self.d, self.f)


class CoordinateConversion:
    """Functions to help conversion from Draw to SVG coordinate space"""

    def __init__(self, dpsx, dpsy, spsx, spsy):
        # Page sizes
        self.dpsx = dpsx
        self.dpsy = dpsy
        self.spsx = spsx
        self.spsy = spsy

        self.draw_to_svg_mat = Mat(spsx/dpsx, 0, 0, -spsy/dpsy, 0, spsy)

    def draw_to_svg_width(self, width):
        return width * self.spsx / self.dpsx

    def draw_to_svg_size(self, size):
        return Point(size.x * self.spsx / self.dpsx,
                     size.y * self.spsy / self.dpsy)

    def draw_to_svg_point(self, point):
        return self.draw_to_svg_mat.matpoint(point)

    def draw_to_svg_matrix(self, draw_matrix):
        def converttransunits(unit):
           return unit / (1<<16)

        svg_point = self.draw_to_svg_point(Convertor.Coords(draw_matrix.e, draw_matrix.f))

        return Mat(converttransunits(draw_matrix.a),
                   converttransunits(draw_matrix.b),
                   converttransunits(draw_matrix.c),
                   converttransunits(draw_matrix.d),
                   svg_point.x,
                   svg_point.y)

    def pt_to_px(v):
        return v * 4.0/3.0

    def px_to_pt(v):
        return v * 0.75

class Convertor:
    """Converts a draw file into an SVG file"""

    # Constants
    PATH_END         = 0
    PATH_MOVE        = 2
    PATH_CLOSE_SUB   = 5
    PATH_BEZIER      = 6
    PATH_DRAW        = 8

    # The set of standard objects.
    # We don't know the details of any third party objects, so we ignore them (see https://www.riscosopen.org/forum/forums/11/topics/1556)
    OBJECT_FONTTABLE   = 0
    OBJECT_TEXT        = 1
    OBJECT_PATH        = 2
    OBJECT_SPRITE      = 5
    OBJECT_GROUP       = 6
    OBJECT_TAGGED      = 7
    OBJECT_TEXTAREA    = 9
    OBJECT_TEXTCOLUMN  = 10
    OBJECT_OPTIONS     = 11
    OBJECT_TRANSTEXT   = 12
    OBJECT_TRANSSPRITE = 13
    OBJECT_JPEG        = 16

    objectnames = {
        0 : "Font Table",
        1 : "Text",
        2 : "Path",
        5 : "Sprite",
        6 : "Group",
        7 : "Tagged",
        9 : "Text Area",
        10 : "Text Column",
        11 : "Options",
        12 : "Transformed Text",
        13 : "Transformed Sprite",
        16 : "JPEG",
    }

    # Limits
    MAX_FONTS = 255

    # Paper sizes in mm
    paper_sizes = {
        0xb00  : (26, 37)    ,   # A10
        0xa00  : (37, 52)    ,   # A9
        0x900  : (52, 74)    ,   # A8
        0x800  : (74, 105)   ,   # A7
        0x700  : (105, 148)  ,   # A6
        0x600  : (148, 210)  ,   # A5
        0x500  : (210, 297)  ,   # A4
        0x400  : (297, 420)  ,   # A3
        0x300  : (420, 594)  ,   # A2
        0x200  : (594, 841)  ,   # A1
        0x100  : (841, 1189) ,   # A0
        0x000  : (1189, 1682),   # 2A0
    }
    a4_and_up = [0x500, 0x400, 0x300, 0x200, 0x100, 0x000]

    # Uses web-safe fonts available in all major browsers:
    # See https://developer.mozilla.org/en-US/docs/Learn/CSS/Styling_text/Fundamentals#web_safe_fonts
    # These can be overridden by using an external font configuration file.
    default_font_replacements = {
        "_default":   'Arial,Helvetica,Verdana,sans-serif',
        "corpus":     'Corpus,"Courier New",Courier,"Lucida Console",monospace',
        "homerton":   'Homerton,Arial,Helvetica,Verdana,sans-serif',
        "newhall":    'NewHall,Century,"Century Schoolbook",serif',
        "swiss":      'Swiss,Arial,Helvetica,Verdana,sans-serif',
        "trinity":    'Trinity,TimesNewRoman,"Times New Roman",Times,Times-Roman,Baskerville,Georgia,serif',
        "sassoon":    'Sassoon,Lexend,"Comic Sans MS","Comic Sans",sans-serif',
        "selwyn":     'Selwyn,"Zapf Dingbats",ZapfDingbats,sans-serif',
        "sidney":     'Symbol,sans-serif',
        "system":     'System,VT323,"Courier New",Courier,"Lucida Console",monospace',
        "wimpsymbol": 'WimpSymbol,"Zapf Dingbats",ZapfDingbats,sans-serif',
    }

    # Debug functions
    def debug_show(charset):
        global und

        n = 16
        for i in range(0, len(charset)):
            if charset[i] == und:
                print(" ", end="")
            else:
                print(charset[i], end="")
            if (i & 15) == 15:
                print()
        print()

    def debug_print_definition(alphabet):
        result = []
        for i in range(32, 256):
            #by.append(i)
            try:
                c = bytes([i]).decode(alphabet)
                c = hex(ord(c))[2:]
            except:
                c = 'und'
            result.append(c)

        first = True
        for i in range(0xa0-32, 256-32):
            if result[i] == 'und':
                v = '     und'
            else:
                v = "'\\u" + "{0}'".format(result[i]).rjust(5, '0')
            if first:
                print(alphabet+"_to_utf8 = replace(latin1_to_utf8, 0xa0,\n      [" + v, end="")
                first = False
            elif (i & 15) != 0:
                print(', ' + v, end="")
            else:
                print(",\n       " + v, end="")

        print("])\n")

    def debug_print_slashu_codes(to_utf8):
        first = True
        i = 0
        for c in to_utf8:
            if c == und:
                v = '     und'
            else:
                num = hex(ord(c))[2:]
                if (len(num) <= 4):
                    num = num.rjust(4, '0')
                    v = "'\\u" + num + "'"
                else:
                    num = num.rjust(8, '0')
                    v = "'\\U" + num + "'"
            if first:
                print("      [" + v, end="")
                first = False
            elif (i & 15) != 0:
                print(', ' + v, end="")
            else:
                print(",\n       " + v, end="")
            i += 1
        print("]")

    # Starting from the base ISO defined base character sets, we define Acorn alphabets.
    # These are defined as mappings from the different encodings to UTF-8.

    # Character to display when character is undefined, e.g:
    #       und = '\u2009'        # Thin space
    #       und = ' '             # Space
    #       und = '\ufffd'        # Undefined
    global und
    und = '\u2009'

    # Utility functions to manipulate the mappings
    def replace(char_set, range_start, replacement):
        result = char_set[:]
        result[range_start:range_start+len(replacement)] = replacement
        return result

    def remove(char_set, range_start, remove_mask):
        global und

        result = char_set[:]
        i = range_start
        for c in remove_mask:
            if c == 'X':
                result[i] = und
            i += 1
        return result

    # Base character sets (these are the ISO Standards, ISO 8859-1 etc)
    # Latin 1 (ISO/IEC 8859-1):  Americas, Western Europe, Oceania, and much of Africa
    latin1_to_utf8 = [
        und, und, und, und,  und, und, und, und,  und, und, und, und,  und, und, und, und,
        und, und, und, und,  und, und, und, und,  und, und, und, und,  und, und, und, und,
        ' ', '!', '"', '#',  '$', '%', '&', "'",  '(', ')', '*', '+',  ',', '-', '.', '/',
        '0', '1', '2', '3',  '4', '5', '6', '7',  '8', '9', ':', ';',  '<', '=', '>', '?',

        '@', 'A', 'B', 'C',  'D', 'E', 'F', 'G',  'H', 'I', 'J', 'K',  'L', 'M', 'N', 'O',
        'P', 'Q', 'R', 'S',  'T', 'U', 'V', 'W',  'X', 'Y', 'Z', '[', '\\', ']', '^', '_',
        '`', 'a', 'b', 'c',  'd', 'e', 'f', 'g',  'h', 'i', 'j', 'k',  'l', 'm', 'n', 'o',
        'p', 'q', 'r', 's',  't', 'u', 'v', 'w',  'x', 'y', 'z', '{',  '|', '}', '~', und,

        und, und, und, und,  und, und, und, und,  und, und, und, und,  und, und, und, und,
        und, und, und, und,  und, und, und, und,  und, und, und, und,  und, und, und, und,
       '\u00a0', '\u00a1', '\u00a2', '\u00a3', '\u00a4', '\u00a5', '\u00a6', '\u00a7', '\u00a8', '\u00a9', '\u00aa', '\u00ab', '\u00ac', '\u00ad', '\u00ae', '\u00af',
       '\u00b0', '\u00b1', '\u00b2', '\u00b3', '\u00b4', '\u00b5', '\u00b6', '\u00b7', '\u00b8', '\u00b9', '\u00ba', '\u00bb', '\u00bc', '\u00bd', '\u00be', '\u00bf',
       '\u00c0', '\u00c1', '\u00c2', '\u00c3', '\u00c4', '\u00c5', '\u00c6', '\u00c7', '\u00c8', '\u00c9', '\u00ca', '\u00cb', '\u00cc', '\u00cd', '\u00ce', '\u00cf',
       '\u00d0', '\u00d1', '\u00d2', '\u00d3', '\u00d4', '\u00d5', '\u00d6', '\u00d7', '\u00d8', '\u00d9', '\u00da', '\u00db', '\u00dc', '\u00dd', '\u00de', '\u00df',
       '\u00e0', '\u00e1', '\u00e2', '\u00e3', '\u00e4', '\u00e5', '\u00e6', '\u00e7', '\u00e8', '\u00e9', '\u00ea', '\u00eb', '\u00ec', '\u00ed', '\u00ee', '\u00ef',
       '\u00f0', '\u00f1', '\u00f2', '\u00f3', '\u00f4', '\u00f5', '\u00f6', '\u00f7', '\u00f8', '\u00f9', '\u00fa', '\u00fb', '\u00fc', '\u00fd', '\u00fe', '\u00ff']

    # Latin 2 (ISO/IEC 8859-2): Central and Eastern European languages
    latin2_to_utf8 = replace(latin1_to_utf8, 0xa0,
      ['\u00a0', '\u0104', '\u02d8', '\u0141', '\u00a4', '\u013d', '\u015a', '\u00a7', '\u00a8', '\u0160', '\u015e', '\u0164', '\u0179', '\u00ad', '\u017d', '\u017b',
       '\u00b0', '\u0105', '\u02db', '\u0142', '\u00b4', '\u013e', '\u015b', '\u02c7', '\u00b8', '\u0161', '\u015f', '\u0165', '\u017a', '\u02dd', '\u017e', '\u017c',
       '\u0154', '\u00c1', '\u00c2', '\u0102', '\u00c4', '\u0139', '\u0106', '\u00c7', '\u010c', '\u00c9', '\u0118', '\u00cb', '\u011a', '\u00cd', '\u00ce', '\u010e',
       '\u0110', '\u0143', '\u0147', '\u00d3', '\u00d4', '\u0150', '\u00d6', '\u00d7', '\u0158', '\u016e', '\u00da', '\u0170', '\u00dc', '\u00dd', '\u0162', '\u00df',
       '\u0155', '\u00e1', '\u00e2', '\u0103', '\u00e4', '\u013a', '\u0107', '\u00e7', '\u010d', '\u00e9', '\u0119', '\u00eb', '\u011b', '\u00ed', '\u00ee', '\u010f',
       '\u0111', '\u0144', '\u0148', '\u00f3', '\u00f4', '\u0151', '\u00f6', '\u00f7', '\u0159', '\u016f', '\u00fa', '\u0171', '\u00fc', '\u00fd', '\u0163', '\u02d9'])

    # Latin 3 (ISO/IEC 8859-3): South European (Turkish, Maltese and Esperanto)
    latin3_to_utf8 = replace(latin1_to_utf8, 0xa0,
      ['\u00a0', '\u0126', '\u02d8', '\u00a3', '\u00a4',      und, '\u0124', '\u00a7', '\u00a8', '\u0130', '\u015e', '\u011e', '\u0134', '\u00ad',      und, '\u017b',
       '\u00b0', '\u0127', '\u00b2', '\u00b3', '\u00b4', '\u00b5', '\u0125', '\u00b7', '\u00b8', '\u0131', '\u015f', '\u011f', '\u0135', '\u00bd',      und, '\u017c',
       '\u00c0', '\u00c1', '\u00c2',      und, '\u00c4', '\u010a', '\u0108', '\u00c7', '\u00c8', '\u00c9', '\u00ca', '\u00cb', '\u00cc', '\u00cd', '\u00ce', '\u00cf',
            und, '\u00d1', '\u00d2', '\u00d3', '\u00d4', '\u0120', '\u00d6', '\u00d7', '\u011c', '\u00d9', '\u00da', '\u00db', '\u00dc', '\u016c', '\u015c', '\u00df',
       '\u00e0', '\u00e1', '\u00e2',      und, '\u00e4', '\u010b', '\u0109', '\u00e7', '\u00e8', '\u00e9', '\u00ea', '\u00eb', '\u00ec', '\u00ed', '\u00ee', '\u00ef',
            und, '\u00f1', '\u00f2', '\u00f3', '\u00f4', '\u0121', '\u00f6', '\u00f7', '\u011d', '\u00f9', '\u00fa', '\u00fb', '\u00fc', '\u016d', '\u015d', '\u02d9'])

    # Latin 4: (ISO/IEC 8859-4) North European (Estonian, Latvian, Lithuanian, Greenlandic, and Sámi)
    latin4_to_utf8 = replace(latin1_to_utf8, 0xa0,
      ['\u00a0', '\u0104', '\u0138', '\u0156', '\u00a4', '\u0128', '\u013b', '\u00a7', '\u00a8', '\u0160', '\u0112', '\u0122', '\u0166', '\u00ad', '\u017d', '\u00af',
       '\u00b0', '\u0105', '\u02db', '\u0157', '\u00b4', '\u0129', '\u013c', '\u02c7', '\u00b8', '\u0161', '\u0113', '\u0123', '\u0167', '\u014a', '\u017e', '\u014b',
       '\u0100', '\u00c1', '\u00c2', '\u00c3', '\u00c4', '\u00c5', '\u00c6', '\u012e', '\u010c', '\u00c9', '\u0118', '\u00cb', '\u0116', '\u00cd', '\u00ce', '\u012a',
       '\u0110', '\u0145', '\u014c', '\u0136', '\u00d4', '\u00d5', '\u00d6', '\u00d7', '\u00d8', '\u0172', '\u00da', '\u00db', '\u00dc', '\u0168', '\u016a', '\u00df',
       '\u0101', '\u00e1', '\u00e2', '\u00e3', '\u00e4', '\u00e5', '\u00e6', '\u012f', '\u010d', '\u00e9', '\u0119', '\u00eb', '\u0117', '\u00ed', '\u00ee', '\u012b',
       '\u0111', '\u0146', '\u014d', '\u0137', '\u00f4', '\u00f5', '\u00f6', '\u00f7', '\u00f8', '\u0173', '\u00fa', '\u00fb', '\u00fc', '\u0169', '\u016b', '\u02d9'])

    # Latin 5 (ISO/IEC 8859-9): Turkish
    latin5_to_utf8 = replace(latin1_to_utf8, 0xa0,
      ['\u00a0', '\u00a1', '\u00a2', '\u00a3', '\u00a4', '\u00a5', '\u00a6', '\u00a7', '\u00a8', '\u00a9', '\u00aa', '\u00ab', '\u00ac', '\u00ad', '\u00ae', '\u00af',
       '\u00b0', '\u00b1', '\u00b2', '\u00b3', '\u00b4', '\u00b5', '\u00b6', '\u00b7', '\u00b8', '\u00b9', '\u00ba', '\u00bb', '\u00bc', '\u00bd', '\u00be', '\u00bf',
       '\u00c0', '\u00c1', '\u00c2', '\u00c3', '\u00c4', '\u00c5', '\u00c6', '\u00c7', '\u00c8', '\u00c9', '\u00ca', '\u00cb', '\u00cc', '\u00cd', '\u00ce', '\u00cf',
       '\u011e', '\u00d1', '\u00d2', '\u00d3', '\u00d4', '\u00d5', '\u00d6', '\u00d7', '\u00d8', '\u00d9', '\u00da', '\u00db', '\u00dc', '\u0130', '\u015e', '\u00df',
       '\u00e0', '\u00e1', '\u00e2', '\u00e3', '\u00e4', '\u00e5', '\u00e6', '\u00e7', '\u00e8', '\u00e9', '\u00ea', '\u00eb', '\u00ec', '\u00ed', '\u00ee', '\u00ef',
       '\u011f', '\u00f1', '\u00f2', '\u00f3', '\u00f4', '\u00f5', '\u00f6', '\u00f7', '\u00f8', '\u00f9', '\u00fa', '\u00fb', '\u00fc', '\u0131', '\u015f', '\u00ff'])

    # Latin 6 (ISO/IEC 8859-10): Nordic languages
    latin6_to_utf8 = replace(latin1_to_utf8, 0xa0,
      ['\u00a0', '\u0104', '\u0112', '\u0122', '\u012a', '\u0128', '\u0136', '\u00a7', '\u013b', '\u0110', '\u0160', '\u0166', '\u017d', '\u00ad', '\u016a', '\u014a',
       '\u00b0', '\u0105', '\u0113', '\u0123', '\u012b', '\u0129', '\u0137', '\u00b7', '\u013c', '\u0111', '\u0161', '\u0167', '\u017e', '\u2015', '\u016b', '\u014b',
       '\u0100', '\u00c1', '\u00c2', '\u00c3', '\u00c4', '\u00c5', '\u00c6', '\u012e', '\u010c', '\u00c9', '\u0118', '\u00cb', '\u0116', '\u00cd', '\u00ce', '\u00cf',
       '\u00d0', '\u0145', '\u014c', '\u00d3', '\u00d4', '\u00d5', '\u00d6', '\u0168', '\u00d8', '\u0172', '\u00da', '\u00db', '\u00dc', '\u00dd', '\u00de', '\u00df',
       '\u0101', '\u00e1', '\u00e2', '\u00e3', '\u00e4', '\u00e5', '\u00e6', '\u012f', '\u010d', '\u00e9', '\u0119', '\u00eb', '\u0117', '\u00ed', '\u00ee', '\u00ef',
       '\u00f0', '\u0146', '\u014d', '\u00f3', '\u00f4', '\u00f5', '\u00f6', '\u0169', '\u00f8', '\u0173', '\u00fa', '\u00fb', '\u00fc', '\u00fd', '\u00fe', '\u0138'])

    # Latin 7 (ISO/IEC 8859-13): Baltic languages
    latin7_to_utf8 = replace(latin1_to_utf8, 0xa0,
      ['\u00a0', '\u201d', '\u00a2', '\u00a3', '\u00a4', '\u201e', '\u00a6', '\u00a7', '\u00d8', '\u00a9', '\u0156', '\u00ab', '\u00ac', '\u00ad', '\u00ae', '\u00c6',
       '\u00b0', '\u00b1', '\u00b2', '\u00b3', '\u201c', '\u00b5', '\u00b6', '\u00b7', '\u00f8', '\u00b9', '\u0157', '\u00bb', '\u00bc', '\u00bd', '\u00be', '\u00e6',
       '\u0104', '\u012e', '\u0100', '\u0106', '\u00c4', '\u00c5', '\u0118', '\u0112', '\u010c', '\u00c9', '\u0179', '\u0116', '\u0122', '\u0136', '\u012a', '\u013b',
       '\u0160', '\u0143', '\u0145', '\u00d3', '\u014c', '\u00d5', '\u00d6', '\u00d7', '\u0172', '\u0141', '\u015a', '\u016a', '\u00dc', '\u017b', '\u017d', '\u00df',
       '\u0105', '\u012f', '\u0101', '\u0107', '\u00e4', '\u00e5', '\u0119', '\u0113', '\u010d', '\u00e9', '\u017a', '\u0117', '\u0123', '\u0137', '\u012b', '\u013c',
       '\u0161', '\u0144', '\u0146', '\u00f3', '\u014d', '\u00f5', '\u00f6', '\u00f7', '\u0173', '\u0142', '\u015b', '\u016b', '\u00fc', '\u017c', '\u017e', '\u2019'])

    # Latin 8 (ISO/IEC 8859-14): Celtic languages
    latin8_to_utf8 = replace(latin1_to_utf8, 0xa0,
      ['\u00a0', '\u1e02', '\u1e03', '\u00a3', '\u010a', '\u010b', '\u1e0a', '\u00a7', '\u1e80', '\u00a9', '\u1e82', '\u1e0b', '\u1ef2', '\u00ad', '\u00ae', '\u0178',
       '\u1e1e', '\u1e1f', '\u0120', '\u0121', '\u1e40', '\u1e41', '\u00b6', '\u1e56', '\u1e81', '\u1e57', '\u1e83', '\u1e60', '\u1ef3', '\u1e84', '\u1e85', '\u1e61',
       '\u00c0', '\u00c1', '\u00c2', '\u00c3', '\u00c4', '\u00c5', '\u00c6', '\u00c7', '\u00c8', '\u00c9', '\u00ca', '\u00cb', '\u00cc', '\u00cd', '\u00ce', '\u00cf',
       '\u0174', '\u00d1', '\u00d2', '\u00d3', '\u00d4', '\u00d5', '\u00d6', '\u1e6a', '\u00d8', '\u00d9', '\u00da', '\u00db', '\u00dc', '\u00dd', '\u0176', '\u00df',
       '\u00e0', '\u00e1', '\u00e2', '\u00e3', '\u00e4', '\u00e5', '\u00e6', '\u00e7', '\u00e8', '\u00e9', '\u00ea', '\u00eb', '\u00ec', '\u00ed', '\u00ee', '\u00ef',
       '\u0175', '\u00f1', '\u00f2', '\u00f3', '\u00f4', '\u00f5', '\u00f6', '\u1e6b', '\u00f8', '\u00f9', '\u00fa', '\u00fb', '\u00fc', '\u00fd', '\u0177', '\u00ff'])

    # Latin 9 (ISO/IEC 8859-15): Western Europe
    latin9_to_utf8 = replace(latin1_to_utf8, 0xa0,
      ['\u00a0', '\u00a1', '\u00a2', '\u00a3', '\u20ac', '\u00a5', '\u0160', '\u00a7', '\u0161', '\u00a9', '\u00aa', '\u00ab', '\u00ac', '\u00ad', '\u00ae', '\u00af',
       '\u00b0', '\u00b1', '\u00b2', '\u00b3', '\u017d', '\u00b5', '\u00b6', '\u00b7', '\u017e', '\u00b9', '\u00ba', '\u00bb', '\u0152', '\u0153', '\u0178', '\u00bf',
       '\u00c0', '\u00c1', '\u00c2', '\u00c3', '\u00c4', '\u00c5', '\u00c6', '\u00c7', '\u00c8', '\u00c9', '\u00ca', '\u00cb', '\u00cc', '\u00cd', '\u00ce', '\u00cf',
       '\u00d0', '\u00d1', '\u00d2', '\u00d3', '\u00d4', '\u00d5', '\u00d6', '\u00d7', '\u00d8', '\u00d9', '\u00da', '\u00db', '\u00dc', '\u00dd', '\u00de', '\u00df',
       '\u00e0', '\u00e1', '\u00e2', '\u00e3', '\u00e4', '\u00e5', '\u00e6', '\u00e7', '\u00e8', '\u00e9', '\u00ea', '\u00eb', '\u00ec', '\u00ed', '\u00ee', '\u00ef',
       '\u00f0', '\u00f1', '\u00f2', '\u00f3', '\u00f4', '\u00f5', '\u00f6', '\u00f7', '\u00f8', '\u00f9', '\u00fa', '\u00fb', '\u00fc', '\u00fd', '\u00fe', '\u00ff'])

    # Latin 10 (ISO/IEC 8859-16): South-Eastern Europe
    latin10_to_utf8 = replace(latin1_to_utf8, 0xa0,
      ['\u00a0', '\u0104', '\u0105', '\u0141', '\u20ac', '\u201e', '\u0160', '\u00a7', '\u0161', '\u00a9', '\u0218', '\u00ab', '\u0179', '\u00ad', '\u017a', '\u017b',
       '\u00b0', '\u00b1', '\u010c', '\u0142', '\u017d', '\u201d', '\u00b6', '\u00b7', '\u017e', '\u010d', '\u0219', '\u00bb', '\u0152', '\u0153', '\u0178', '\u017c',
       '\u00c0', '\u00c1', '\u00c2', '\u0102', '\u00c4', '\u0106', '\u00c6', '\u00c7', '\u00c8', '\u00c9', '\u00ca', '\u00cb', '\u00cc', '\u00cd', '\u00ce', '\u00cf',
       '\u0110', '\u0143', '\u00d2', '\u00d3', '\u00d4', '\u0150', '\u00d6', '\u015a', '\u0170', '\u00d9', '\u00da', '\u00db', '\u00dc', '\u0118', '\u021a', '\u00df',
       '\u00e0', '\u00e1', '\u00e2', '\u0103', '\u00e4', '\u0107', '\u00e6', '\u00e7', '\u00e8', '\u00e9', '\u00ea', '\u00eb', '\u00ec', '\u00ed', '\u00ee', '\u00ef',
       '\u0111', '\u0144', '\u00f2', '\u00f3', '\u00f4', '\u0151', '\u00f6', '\u015b', '\u0171', '\u00f9', '\u00fa', '\u00fb', '\u00fc', '\u0119', '\u021b', '\u00ff'])

    # Welsh (ISO IR-182):
    welsh_to_utf8 = replace(latin1_to_utf8, 0xa0,
      ['\u00a0', '\u00a1', '\u00a2', '\u00a3', '\u00a4', '\u00a5', '\u00a6', '\u00a7', '\u1e80', '\u00a9', '\u1e82', '\u00ab', '\u1ef2', '\u00ad', '\u00ae', '\u0178',
       '\u00b0', '\u00b1', '\u00b2', '\u00b3', '\u00b4', '\u00b5', '\u00b6', '\u00b7', '\u1e81', '\u00b9', '\u1e83', '\u00bb', '\u1ef3', '\u1e84', '\u1e85', '\u00bf',
       '\u00c0', '\u00c1', '\u00c2', '\u00c3', '\u00c4', '\u00c5', '\u00c6', '\u00c7', '\u00c8', '\u00c9', '\u00ca', '\u00cb', '\u00cc', '\u00cd', '\u00ce', '\u00cf',
       '\u0174', '\u00d1', '\u00d2', '\u00d3', '\u00d4', '\u00d5', '\u00d6', '\u0078', '\u00d8', '\u00d9', '\u00da', '\u00db', '\u00dc', '\u00dd', '\u0176', '\u00df',
       '\u00e0', '\u00e1', '\u00e2', '\u00e3', '\u00e4', '\u00e5', '\u00e6', '\u00e7', '\u00e8', '\u00e9', '\u00ea', '\u00eb', '\u00ec', '\u00ed', '\u00ee', '\u00ef',
       '\u0175', '\u00f1', '\u00f2', '\u00f3', '\u00f4', '\u00f5', '\u00f6', '\u00f7', '\u00f8', '\u00f9', '\u00fa', '\u00fb', '\u00fc', '\u00fd', '\u0177', '\u00ff'])


    # Hebrew (ISO/IEC 8859-8):
    hebrew_to_utf8 = replace(latin1_to_utf8, 0xa0,
      ['\u00a0',      und, '\u00a2', '\u00a3', '\u00a4', '\u00a5', '\u00a6', '\u00a7', '\u00a8', '\u00a9', '\u00d7', '\u00ab', '\u00ac', '\u00ad', '\u00ae', '\u00af',
       '\u00b0', '\u00b1', '\u00b2', '\u00b3', '\u00b4', '\u00b5', '\u00b6', '\u00b7', '\u00b8', '\u00b9', '\u00f7', '\u00bb', '\u00bc', '\u00bd', '\u00be',      und,
            und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,
            und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und, '\u2017',
       '\u05d0', '\u05d1', '\u05d2', '\u05d3', '\u05d4', '\u05d5', '\u05d6', '\u05d7', '\u05d8', '\u05d9', '\u05da', '\u05db', '\u05dc', '\u05dd', '\u05de', '\u05df',
       '\u05e0', '\u05e1', '\u05e2', '\u05e3', '\u05e4', '\u05e5', '\u05e6', '\u05e7', '\u05e8', '\u05e9', '\u05ea',      und,      und, '\u200e', '\u200f',      und])

    # Cyrillic (ISO/IEC 8859-5):
    cyrillic_to_utf8 = replace(latin1_to_utf8, 0xa0,
      ['\u00a0', '\u0401', '\u0402', '\u0403', '\u0404', '\u0405', '\u0406', '\u0407', '\u0408', '\u0409', '\u040a', '\u040b', '\u040c', '\u00ad', '\u040e', '\u040f',
       '\u0410', '\u0411', '\u0412', '\u0413', '\u0414', '\u0415', '\u0416', '\u0417', '\u0418', '\u0419', '\u041a', '\u041b', '\u041c', '\u041d', '\u041e', '\u041f',
       '\u0420', '\u0421', '\u0422', '\u0423', '\u0424', '\u0425', '\u0426', '\u0427', '\u0428', '\u0429', '\u042a', '\u042b', '\u042c', '\u042d', '\u042e', '\u042f',
       '\u0430', '\u0431', '\u0432', '\u0433', '\u0434', '\u0435', '\u0436', '\u0437', '\u0438', '\u0439', '\u043a', '\u043b', '\u043c', '\u043d', '\u043e', '\u043f',
       '\u0440', '\u0441', '\u0442', '\u0443', '\u0444', '\u0445', '\u0446', '\u0447', '\u0448', '\u0449', '\u044a', '\u044b', '\u044c', '\u044d', '\u044e', '\u044f',
       '\u2116', '\u0451', '\u0452', '\u0453', '\u0454', '\u0455', '\u0456', '\u0457', '\u0458', '\u0459', '\u045a', '\u045b', '\u045c', '\u00a7', '\u045e', '\u045f'])

    # Greek (ISO/IEC_8859-7):
    greek_to_utf8 = replace(latin1_to_utf8, 0xa0,
      ['\u00a0', '\u2018', '\u2019', '\u00a3', '\u20ac', '\u20af', '\u00a6', '\u00a7', '\u00a8', '\u00a9', '\u037a', '\u00ab', '\u00ac', '\u00ad',      und, '\u2015',
       '\u00b0', '\u00b1', '\u00b2', '\u00b3', '\u0384', '\u0385', '\u0386', '\u00b7', '\u0388', '\u0389', '\u038a', '\u00bb', '\u038c', '\u00bd', '\u038e', '\u038f',
       '\u0390', '\u0391', '\u0392', '\u0393', '\u0394', '\u0395', '\u0396', '\u0397', '\u0398', '\u0399', '\u039a', '\u039b', '\u039c', '\u039d', '\u039e', '\u039f',
       '\u03a0', '\u03a1',      und, '\u03a3', '\u03a4', '\u03a5', '\u03a6', '\u03a7', '\u03a8', '\u03a9', '\u03aa', '\u03ab', '\u03ac', '\u03ad', '\u03ae', '\u03af',
       '\u03b0', '\u03b1', '\u03b2', '\u03b3', '\u03b4', '\u03b5', '\u03b6', '\u03b7', '\u03b8', '\u03b9', '\u03ba', '\u03bb', '\u03bc', '\u03bd', '\u03be', '\u03bf',
       '\u03c0', '\u03c1', '\u03c2', '\u03c3', '\u03c4', '\u03c5', '\u03c6', '\u03c7', '\u03c8', '\u03c9', '\u03ca', '\u03cb', '\u03cc', '\u03cd', '\u03ce',      und])


    # These are the characters Acorn commonly adds to the standards:
    acorn_c1 = [ '\u20ac', '\u0174', '\u0175',      und,      und, '\u0176', '\u0177',      und,      und,      und,      und,      und, '\u2026', '\u2122', '\u2030', '\u2022',
                 '\u2018', '\u2019', '\u2039', '\u203a', '\u201c', '\u201d', '\u201e', '\u2013', '\u2014', '\u2212', '\u0152', '\u0153', '\u2020', '\u2021', '\ufb01', '\ufb02' ]

    riscos_latin1_to_utf8  = replace(latin1_to_utf8,  0x80, acorn_c1)
    riscos_latin2_to_utf8  = replace(latin2_to_utf8,  0x80, remove(acorn_c1, 0, " XXXXXX"))
    riscos_latin2_to_utf8[0x9a] = '\u00ab'  # Left-Pointing Double Angle Quotation Mark
    riscos_latin2_to_utf8[0x9b] = '\u00bb'  # Right-Pointing Double Angle Quotation Mark
    riscos_latin3_to_utf8  = replace(latin3_to_utf8,  0x80, remove(acorn_c1, 0, " XXXXXX"))
    riscos_latin4_to_utf8  = replace(latin4_to_utf8,  0x80, remove(acorn_c1, 0, " XXXXXX"))
    riscos_latin5_to_utf8  = replace(latin5_to_utf8,  0x80, remove(acorn_c1, 0, " XXXXXX"))
    riscos_latin6_to_utf8  = replace(latin6_to_utf8,  0x80, remove(acorn_c1, 0, " XXXXXX         "
                                                                                "        X       "))
    riscos_latin7_to_utf8  = replace(latin7_to_utf8,  0x80, remove(acorn_c1, 0, " XXXXXX         "
                                                                                " X  XXX         "))
    riscos_latin8_to_utf8  = replace(latin8_to_utf8,  0x80, remove(acorn_c1, 0, " XXXXXX"))
    riscos_latin9_to_utf8  = replace(latin9_to_utf8,  0x80, remove(acorn_c1, 0, "X               "
                                                                                "          XX    "))
    riscos_latin10_to_utf8 = replace(latin10_to_utf8, 0x80, remove(acorn_c1, 0, "XXXXXXXXXXXX    "
                                                                                "     XX         "))
    riscos_latin10_to_utf8[0x9a] = '\u00ab'  # Left-Pointing Double Angle Quotation Mark
    riscos_latin10_to_utf8[0x9b] = '\u00bb'  # Right-Pointing Double Angle Quotation Mark

    riscos_welsh_to_utf8   = replace(welsh_to_utf8,   0x80, remove(acorn_c1, 0, " XXXXXX"))


    # Some characters are omitted from alphabets
    riscos_hebrew_to_utf8  = remove(hebrew_to_utf8, 0xa0, " X             X"
                                                          "               X"
                                                          "XXXXXXXXXXXXXXXX"
                                                          "XXXXXXXXXXXXXXXX"
                                                          "XXXXXXXXXXXXXXXX"
                                                          "XXXXXXXXXXXXXXXX")
    riscos_cyrillic_to_utf8 = remove(cyrillic_to_utf8, 0xa0, " XXXXXXXXXXXXX X"
                                                             "XXXXXXXXXXXXXXXX"
                                                             "XXXXXXXXXXXXXXXX"
                                                             "XXXXXXXXXXXXXXXX"
                                                             "XXXXXXXXXXXXXXXX"
                                                             "XXXXXXXXXXXXX XX")
    # A RISC OS invention:
    riscos_cyrillic_to_utf8[0xae] = '-'

    riscos_greek_to_utf8 = remove(greek_to_utf8, 0xa0, "     X    X   XX"
                                                       "    XXXXXXX X XX"
                                                       "XXXXXXXXXXXXXXXX"
                                                       "XXXXXXXXXXXXXXXX"
                                                       "XXXXXXXXXXXX XXX"
                                                       "XXXXXXXXXXXXXXXX")

    # NewHall
    newhall_with_breve_to_utf8 = replace(riscos_latin1_to_utf8, 0x80,
      [      und, '\u02d8',      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und, '\u2022' ])
    newhall_to_utf8 = newhall_with_breve_to_utf8[:]
    newhall_to_utf8[0x81] = und

    newhall_latin2_to_utf8 = remove(riscos_latin2_to_utf8, 0x80, "XXXXXXXXXXXXXXX "
                                                                 "                "
                                                                 " XXX XX  XXXX XX"
                                                                 " XXX XXX XXXXXXX"
                                                                 "X  X XX X X X  X"
                                                                 "XXX  X  XX X  X "
                                                                 "X  X XX X X X  X"
                                                                 "XXX  X  XX X  XX")
    newhall_latin3_to_utf8 = remove(riscos_latin3_to_utf8, 0x80, "XXXXXXXXXXXXXXX "
                                                                 "                "
                                                                 " XX  XX  XXXX XX"
                                                                 " X    X  XXXX XX"
                                                                 "   X XX         "
                                                                 "X    X  X    XX "
                                                                 "   X XX         "
                                                                 "X    X  X    XXX")
    newhall_latin4_to_utf8 = remove(riscos_latin4_to_utf8, 0x80, "XXXXXXXXXXXXXXX "
                                                                 "                "
                                                                 " XXX XX  XXXX X "
                                                                 " XXX XXX XXXXXXX"
                                                                 "X      XX X X  X"
                                                                 "XXXX     X   XX "
                                                                 "X      XX X X  X"
                                                                 "XXXX     X   XXX")
    newhall_latin5_to_utf8 = remove(riscos_latin5_to_utf8, 0x80, "XXXXXXXXXXXXXXX "
                                                                 "                "
                                                                 "                "
                                                                 "                "
                                                                 "                "
                                                                 "X            XX "
                                                                 "                "
                                                                 "X            XX ")
    newhall_latin6_to_utf8 = remove(riscos_latin6_to_utf8, 0x80, "XXXXXXXXXXXXXXX "
                                                                 "        X       "
                                                                 " XXXXXX XXXXX XX"
                                                                 " XXXXXX XXXXX XX"
                                                                 "X      XX X X   "
                                                                 " XX    X X      "
                                                                 "X      XX X X   "
                                                                 " XX    X X     X")
    newhall_latin7_to_utf8 = remove(riscos_latin7_to_utf8, 0x80, "XXXXXXXXXXXXXXX "
                                                                 " X  XXX         "
                                                                 "          X     "
                                                                 "          X     "
                                                                 "XXXX  XXX XXXXXX"
                                                                 "XXX X   XXXX XX "
                                                                 "XXXX  XXX XXXXXX"
                                                                 "XXX X   XXXX XX ")
    newhall_latin8_to_utf8 = remove(riscos_latin8_to_utf8, 0x80, "XXXXXXXXXXXXXXX "
                                                                 "                "
                                                                 " XX XXX X XXX  X"
                                                                 "XXXXXX XXXXXXXXX"
                                                                 "                "
                                                                 "X      X      X "
                                                                 "                "
                                                                 "X      X      X ")
    newhall_latin9_to_utf8 = remove(riscos_latin9_to_utf8, 0x80, "XXXXXXXXXXXXXXX "
                                                                 "          XX    "
                                                                 "    X X X       "
                                                                 "    X   X     X ")

    newhall_latin9_with_breve_to_utf8 = newhall_latin9_to_utf8[:]
    newhall_latin9_with_breve_to_utf8[0x81] = '\u02d8'       # Breve

    newhall_latin10_to_utf8 = remove(riscos_latin10_to_utf8, 0x80, "XXXXXXXXXXXXXXX "
                                                                  "     XX         "
                                                                  " XXXX X X X X XX"
                                                                  "  XXX   XXX   XX"
                                                                  "   X X          "
                                                                  "XX   X XX    XX "
                                                                  "   X X          "
                                                                  "XX   X XX    XX ")
    newhall_welsh_to_utf8 = remove(riscos_welsh_to_utf8, 0x80, "XXXXXXXXXXXXXXX "
                                                               "                "
                                                               "        X X X  X"
                                                               "        X X XXX "
                                                               "                "
                                                               "X             X "
                                                               "                "
                                                               "X             X ")
    newhall_greek_to_utf8 = remove(riscos_greek_to_utf8, 0xa0, "    X")

    corpus_medium_greek_to_utf8 = riscos_greek_to_utf8[:]
    # A RISC OS invention:
    corpus_medium_greek_to_utf8[0xaf] = '\u2092'

    # Swiss
    swiss_to_utf8 = replace(riscos_latin1_to_utf8, 0x80,
      [ '\u0174', '\u0176', '\u1e82', '\u0031', '\u0175', '\u0177', '\u1e83', '\u2026',      und, '\u2074', '\u2122', '\U0001d7e3', '\u2215', '\U0001d453', '\u2030', '\u2022'])

    swiss_c1 = riscos_latin2_to_utf8[0x80:0xa0]     # With chevrons
    swiss_c1a = riscos_latin1_to_utf8[0x80:0xa0]    # With OE oe instead of chevrons

    swiss_latin1_to_utf8  = replace(riscos_latin1_to_utf8, 0x80, remove(acorn_c1, 0, "X"))
    swiss_latin2_to_utf8  = replace(riscos_latin2_to_utf8, 0x80, remove(swiss_c1, 0, "XXXXXXX"))
    swiss_latin2_to_utf8  = remove(swiss_latin2_to_utf8, 0xa0, " XXX XX  XXXX XX"
                                                               " XXX XX  XXXXXXX"
                                                               "X  X XX X X X  X"
                                                               "XXX  X  XX X  X "
                                                               "X  X XX X X X  X"
                                                               "XXX  X  XX X  XX")

    swiss_latin3_to_utf8  = replace(riscos_latin3_to_utf8, 0x80, remove(acorn_c1, 0, "XXXXXXX"))
    swiss_latin3_to_utf8  = remove(swiss_latin3_to_utf8, 0xa0, " XX   X  XXXX  X"
                                                               " X    X   XXX  X"
                                                               "     XX         "
                                                               "     X  X    XX "
                                                               "     XX         "
                                                               "     X  X    XXX" )

    swiss_latin4_to_utf8  = replace(riscos_latin4_to_utf8, 0x80, remove(swiss_c1a, 0, "XXXXXXX"))
    swiss_latin4_to_utf8 = remove(swiss_latin4_to_utf8, 0xa0, " XXX XX  XXXX X "
                                                              " XXX XX  XXXXXXX"
                                                              "X      XX X X  X"
                                                              "XXXX     X   XX "
                                                              "X      XX X X  X"
                                                              "XXXX     X   XXX")
    swiss_latin5_to_utf8  = replace(riscos_latin5_to_utf8, 0x80, remove(swiss_c1a, 0, "XXXXXXX"))
    swiss_latin5_to_utf8  = remove(swiss_latin5_to_utf8, 0xd0, "X            XX "
                                                               "                "
                                                               "X             X ")
    swiss_latin6_to_utf8  = replace(riscos_latin6_to_utf8, 0x80, remove(swiss_c1a, 0, "XXXXXXX         "
                                                                                      "        X       "))
    swiss_latin6_to_utf8  = remove(swiss_latin6_to_utf8, 0xa0, " XXXXXX XXXXX XX"
                                                               " XXXXXX XXXXX XX"
                                                               "X      XX X X   "
                                                               " XX    X X      "
                                                               "X      XX X X   "
                                                               " XX    X X     X")

    swiss_latin7_to_utf8  = replace(riscos_latin7_to_utf8, 0x80, remove(swiss_c1a, 0, "XXXXXXX         "
                                                                                      " X  XXX         "))
    swiss_latin7_to_utf8  = remove(swiss_latin7_to_utf8, 0xa0, "          X     "
                                                               "          X     "
                                                               "XXXX  XXX XXXXXX"
                                                               "XXX X   XXXX XX "
                                                               "XXXX  XXX XXXXXX"
                                                               "XXX X   XXXX XX ")
    swiss_latin8_to_utf8  = replace(riscos_latin8_to_utf8, 0x80, remove(swiss_c1a, 0, "XXXXXXX"))
    swiss_latin8_to_utf8  = remove(swiss_latin8_to_utf8, 0xa0, " XX XXX X  XX  X"
                                                               "XXXXXX XXX XXXXX"
                                                               "                "
                                                               "       X        "
                                                               "                "
                                                               "       X        ")

    swiss_latin9_to_utf8  = replace(riscos_latin9_to_utf8, 0x80, remove(swiss_c1a, 0, "X               "
                                                                                      "          XX    "))
    swiss_latin9_to_utf8  = remove(swiss_latin9_to_utf8, 0xa0, "    X X X       "
                                                               "    X   X     X ")
    swiss_latin10_to_utf8 = replace(riscos_latin10_to_utf8, 0x80, remove(swiss_c1,  0, "XXXXXXX         "
                                                                                       "     XX         "))
    swiss_latin10_to_utf8 = remove(swiss_latin10_to_utf8, 0xa0, " XXXX X X X X XX"
                                                                "  XXX   XXX   XX"
                                                                "   X X          "
                                                                "XX   X XX    XX "
                                                                "   X X          "
                                                                "XX   X XX    XX ")
    swiss_welsh_to_utf8   = replace(riscos_welsh_to_utf8,  0x80, remove(swiss_c1a, 0,  "XXXXXXX"))
    swiss_welsh_to_utf8 = remove(swiss_welsh_to_utf8, 0xa0, "        X   X  X"
                                                            "        X   XXX ")

    swiss_greek_to_utf8   = remove(riscos_greek_to_utf8, 0xa0, "    X")

    # Sassoon
    sassoon_c1 = [      und, '\u0174', '\u0175',      und,      und, '\u0176', '\u0177', '\u0026', '\u0071', '\u0047', '\u0049', '\u004a', '\u2026', '\u2122', '\U0001d453', '\u2022',
                   '\u2018', '\u2019', '\u2039', '\u203a', '\u201c', '\u201d', '\u201e', '\u2013', '\u2014', '\u2212', '\u0152', '\u0153', '\u0034', '\u006b',     '\ufb01', '\ufb02' ]
    sassoon_c1a = [      und, '\u0174', '\u0175',      und,      und, '\u0176', '\u0177', '\u0026', '\u0071', '\u0047', '\u0049', '\u004a', '\u2026', '\u2122', '\U0001d453', '\u2022',
                   '\u2018', '\u2019', '\u2039', '\u203a', '\u201c', '\u201d', '\u201e', '\u2013', '\u2014', '\u2212', '\u00ab', '\u00bb', '\u0034', '\u006b',     '\ufb01', '\ufb02' ]
    sassoon_to_utf8 = replace(latin1_to_utf8, 0x80, sassoon_c1)

    sassoon_latin2_to_utf8  = replace(riscos_latin2_to_utf8, 0x80, remove(sassoon_c1a, 0, " XXXXXX"))
    sassoon_latin2_to_utf8[0xd0] = und

    sassoon_latin3_to_utf8  = replace(riscos_latin3_to_utf8, 0x80, remove(sassoon_c1, 0, " XXXXXX"))
    sassoon_latin4_to_utf8  = replace(riscos_latin4_to_utf8, 0x80, remove(sassoon_c1, 0, " XXXXXX         "))
    sassoon_latin4_to_utf8 = remove(sassoon_latin4_to_utf8, 0xb0, "             X X"
                                                                  "                "
                                                                  "X")

    sassoon_latin5_to_utf8  = replace(riscos_latin5_to_utf8, 0x80, remove(sassoon_c1, 0, " XXXXXX"))
    sassoon_latin6_to_utf8  = replace(riscos_latin6_to_utf8, 0x80, remove(sassoon_c1, 0, " XXXXXX         "
                                                                                         "        X       "))
    sassoon_latin6_to_utf8  = remove(sassoon_latin6_to_utf8, 0xa0, "         X     X"
                                                                   "               X"
                                                                   )
    sassoon_latin7_to_utf8  = replace(riscos_latin7_to_utf8, 0x80, remove(sassoon_c1, 0, " XXXXXX         "
                                                                                         " X  XXX         "))
    sassoon_latin8_to_utf8  = replace(riscos_latin8_to_utf8, 0x80, remove(sassoon_c1, 0, " XXXXXX"))
    sassoon_latin8_to_utf8  = remove(sassoon_latin8_to_utf8, 0xa0, "XXX   X X  X    "
                                                                   "XX  XX XXX X XXX"
                                                                   "                "
                                                                   "       X        "
                                                                   "                "
                                                                   "       X        ")

    sassoon_latin9_to_utf8  = replace(riscos_latin9_to_utf8, 0x80, remove(sassoon_c1, 0, "   XX           "
                                                                                         "          XX    "))
    sassoon_latin9_to_utf8  = remove(sassoon_latin9_to_utf8, 0x80, "   XX           "
                                                                   "          XX    "
                                                                   "    X           ")
    sassoon_latin10_to_utf8 = replace(riscos_latin10_to_utf8, 0x80, remove(sassoon_c1, 0, " XXXXXX         "
                                                                                          "     XX         "))
    sassoon_latin10_to_utf8[0x9a] = sassoon_latin10_to_utf8[0xab]
    sassoon_latin10_to_utf8[0x9b] = sassoon_latin10_to_utf8[0xbb]
    sassoon_latin10_to_utf8 = remove(sassoon_latin10_to_utf8, 0xa0, "    X     X     "
                                                                    "          X     "
                                                                    "                "
                                                                    "X             X "
                                                                    "                "
                                                                    "              X ")
    sassoon_welsh_to_utf8   = replace(riscos_welsh_to_utf8, 0x80, remove(sassoon_c1, 0, " XXXXXX"))
    sassoon_welsh_to_utf8 = remove(sassoon_welsh_to_utf8, 0xa0, "        X       "
                                                                "        X    XX ")
    # The Welsh ISO standard has Y and y with grave accents, but RISC OS Sassoon has E and e with tilde:
    sassoon_welsh_to_utf8[0xac] = '\u1ebc'
    sassoon_welsh_to_utf8[0xbc] = '\u1ebd'

    sassoon_hebrew_to_utf8 = riscos_hebrew_to_utf8[:]
    # Sassoon has 'EFF' in small letters at position af instead of MACRON. We approximate this with 'EFF' in smallcaps.
    sassoon_hebrew_to_utf8[0xaf] = '\u1D07\ua730\ua730'

    sassoon_greek_to_utf8 = remove(riscos_greek_to_utf8, 0xa0, "    X")

    # Symbols
    selwyn_to_utf8 = [
        und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,
        und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,
        und,      '\u2701', '\u2702', '\u2703', '\u2704', '\u2741', '\u2706', '\u2707', '\u2708', '\u2709', '\u261b', '\u261e', '\u270c', '\u270d', '\u270e', '\u270f',
        '\u2710', '\u2711', '\u2712', '\u2713', '\u2742', '\u2715', '\u2716', '\u2717', '\u2743', '\u2719', '\u271a', '\u271b', '\u271c', '\u271d', '\u271e', '\u271f',

        '\u2720', '\u2721', '\u2722', '\u2723', '\u2724', '\u2725', '\u2726', '\u2727', '\u2745', '\u2729', '\u272a', '\u272b', '\u272c', '\u272d', '\u272e', '\u272f',
        '\u2730', '\u2731', '\u2732', '\u2733', '\u2734', '\u2735', '\u2736', '\u2737', '\u2738', '\u2739', '\u273a', '\u273b', '\u273c', '\u2746', '\u273e', '\u273f',
        '\u2740', '\u260e', '\u2714', '\u2718', '\u2744', '\u2605', '\u273b', '\u2750', '\u2751', '\u2752', '\u25c6', '\u27a7', '\u25cf', '\u274d', '\u25a0', '\u274f',
        '\u2747', '\u2748', '\u2749', '\u25b2', '\u25bc', '\u274a', '\u2756', '\u25d7', '\u2758', '\u2759', '\u275a', '\u275b', '\u275c', '\u275d', '\u275e', und,

        und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,
        und,      und,      '\u276c', '\u2771', '\u2770', '\u276a', '\u2768', '\u2773', '\u276e', '\u276f', '\u2772', '\u276d', '\u2769', '\u276b', '\u2774', '\u2775',
        '\u00a0', '\u2761', '\u2762', '\u2763', '\u2764', '\u2765', '\u2766', '\u2767', '\u2663', '\u2666', '\u2665', '\u2660', '\u2460', '\u2461', '\u2462', '\u2463',
        '\u2464', '\u2465', '\u2466', '\u2467', '\u2468', '\u2469', '\u2776', '\u2777', '\u2778', '\u2779', '\u277a', '\u277b', '\u277c', '\u277d', '\u277e', '\u277f',
        '\u2780', '\u2781', '\u2782', '\u2783', '\u2784', '\u2785', '\u2786', '\u2787', '\u2788', '\u2789', '\u278a', '\u278b', '\u278c', '\u278d', '\u278e', '\u278f',
        '\u2790', '\u2791', '\u2792', '\u2793', '\u279e', '\u2192', '\u2194', '\u2195', '\u2798', '\u2799', '\u279a', '\u279b', '\u279c', '\u279d', '\u279e', '\u279f',

        '\u27a0', '\u27a1', '\u27a2', '\u27a3', '\u27a4', '\u27a5', '\u27a6', '\u274a', '\u27a8', '\u27a9', '\u27aa', '\u27ab', '\u27ac', '\u27ad', '\u27ae', '\u27af',
        und,      '\u27b1', '\u27b2', '\u27b3', '\u27b4', '\u27b5', '\u27b6', '\u27b7', '\u27b8', '\u27b9', '\u27ba', '\u27bb', '\u27bc', '\u27bd', '\u27be', und
    ]

    # Maths notation
    sidney_to_utf8 = [
        und,      und,          und,      und,          und,      und,      und,      und,      und,      und,      und,      und,       und,      und,      und,      und,
        und,      und,          und,      und,          und,      und,      und,      und,      und,      und,      und,      und,       und,      und,      und,      und,
        ' ',      '!',          '\u2200', '#',          '\u2203', '%',      '&',      '\u220b', '(',      ')',      '*',      '+',       ',',      '-',      '.',      '/',
        '0',      '1',          '2',      '3',          '4',      '5',      '6',      '7',      '8',      '9',      ':',      ';',       '<',      '=',      '>',      '?',

        '\u2245',   '\u0391',   '\u0392', '\u03a7',     '\u0394', '\u0395', '\u03a6', '\u0393', '\u0397', '\u0399', '\u03d1', '\u039a',  '\u039b', '\u039c', '\u039d', '\u039f',
        '\u1d28',   '\u0398',   '\u03a1', '\u03a3',     '\u03a4', '\u03a5', '\u03c2', '\u03a9', '\u039e', '\u03a8', '\u0396', '[',       '\u2234', ']',      '\u22a5', '_',
        'OVERLINE', '\u03b1',   '\u03b2', '\u03c7',     '\u03b4', '\u03b5', '\u03d5', '\u03b3', '\u03b7', '\u03b9', '\u03c6', '\u03ba',  '\u03bb', '\u03bc', '\u03bd', '\u03bf',
        '\u03c0',   '\u03b8',   '\u03f1', '\u03c3',     '\u03c4', '\u03c5', '\u03d6', '\u03c9', '\u03be', '\u03c8', '\u03b6', '{',       '|',      '}',      '~',      und,

        und,      und,          und,      und,          und,      und,      und,       und,     und,      und,      und,      und,       und,      und,      und,      und,
        und,      und,          und,      und,          und,      und,      und,       und,     und,      und,      und,      und,       und,      und,      und,      und,
        '\u00a0', '\u03d2',     '\u2032', '\u2264',     '\u2215', '\u221e', '\u2a0d', '\u2663', '\u2666', '\u2665', '\u2660', '\u2194',  '\u2190', '\u2191', '\u2192', '\u2193',
        '\u00b0', '\u00b1',     '\u2033', '\u2265',     '\u00D7', '\u221d', '\u2202', '\u2981', '\u00F7', '\u2260', '\u2263', '\u2248',  '\u2026', '\u23d0', '\u23af', '\u21b2',

        '\u2135', '\U0001d50d', '\u211c', '\U0001d513', '\u2297', '\u2295', '\u2298', '\u22c2', '\u22c3', '\u2283', '\u2287', '\u2284',  '\u2282', '\u2286', '\u2208', '\u2209',
        '\u2220', '\u2207',     '\u00ae', '\u00a9',     '\u2122', '\u03a0', '\u23b7', '.',      '\u00ac', '\u2227', '\u2228', '\u21d4',  '\u21d0', '\u21d1', '\u21d2', '\u21d3',
        '\u25c7', '\u27e8',     '\u00ae', '\u00a9',     '\u2122', '\u03a3', '\u239b', '\u239c', '\u239d', '\u23a1', '\u23a2', '\u23a3',  '\u23a7', '\u23a8', '\u23a9', '\u23aa',
        '\u20ac', '\u27e9',     '\u222b', '\u2320',     '\u23ae', '\u2321', '\u239e', '\u239f', '\u23a0', '\u23a4', '\u23a5', '\u23a6',  '\u23ab', '\u23ac', '\u23ad', und
    ]

    sidney_latin1_to_utf8 = replace(sidney_to_utf8, 0x80, acorn_c1)
    sidney_latin1_to_utf8 = remove(sidney_latin1_to_utf8, 0x20, "X X X  X  X  X  "
                                                                "                "
                                                                "XXXXXXXXXXXXXXXX"
                                                                "XXXXXXXXXXX X X "
                                                                "XXXXXXXXXXXXXXXX"
                                                                "XXXXXXXXXXX   XX"

                                                                " XXXXXXXXXXX XX "
                                                                "XXXXXXXXX XXXXXX"
                                                                " XXXXXXXXXXX XXX"
                                                                "  XXX XXXXXXXXXX"
                                                                "XXXXXXXXXXXXXXXX"
                                                                "XXXXXXX XXXXXXXX"
                                                                "XXXXXXXXXXXXXXXX"
                                                                "XXXXXXX XXXXXXXX")

    sidney_latin8_to_utf8 = remove(sidney_latin1_to_utf8, 0xb0, "XX")
    sidney_latin8_to_utf8 = sidney_latin8_to_utf8[0:0xa0]
    sidney_latin8_to_utf8.extend([
        und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,     und,      und,
        und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,     und,      und,
        und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,     und,      und,
        und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,     und,      und,
        und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,     und,      und,
        und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,     und,      und,
    ])

    sidney_latin1_to_utf8[0xac] = '\u00ac'  # not
    sidney_latin1_to_utf8[0xb5] = '\u03bc'  # mu

    sidney_latin1_to_utf8[0xd7] = '\u00d7'  # multiplication
    sidney_latin1_to_utf8[0xf7] = '\u00f7'  # division

    sidney_latin7_to_utf8 = sidney_latin1_to_utf8[:]

    sidney_latin2_to_utf8 = sidney_latin1_to_utf8[:]
    sidney_latin2_to_utf8[0xac] = und
    sidney_latin2_to_utf8[0xb1] = und
    sidney_latin2_to_utf8[0xb5] = und

    sidney_latin3_to_utf8 = sidney_latin1_to_utf8[:]
    sidney_latin3_to_utf8[0xac] = und
    sidney_latin3_to_utf8[0xb1] = und

    sidney_latin4_to_utf8 = sidney_latin2_to_utf8[:]
    sidney_latin5_to_utf8 = sidney_latin1_to_utf8[:]

    sidney_latin6_to_utf8 = sidney_latin2_to_utf8[:]
    sidney_latin6_to_utf8[0xd7] = und
    sidney_latin6_to_utf8[0xf7] = und

    sidney_latin9_to_utf8 = sidney_latin1_to_utf8[:]
    sidney_latin9_to_utf8[0x80] = und       # remove Euro
    sidney_latin9_to_utf8[0xa4] = '\u20ac'  # Add Euro

    sidney_latin10_to_utf8 = sidney_latin9_to_utf8[:]
    sidney_latin10_to_utf8[0xac] = und
    sidney_latin10_to_utf8[0xb5] = und
    sidney_latin10_to_utf8[0xd7] = und
    sidney_latin10_to_utf8[0xf7] = und

    sidney_welsh_to_utf8 = sidney_latin5_to_utf8[:]
    sidney_welsh_to_utf8[0xac] = und

    sidney_hebrew_to_utf8 = sidney_latin1_to_utf8[0:0x80]
    sidney_hebrew_to_utf8.extend(
      [
           und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,     und,      und,
           und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,     und,      und,
           und,      und,      und,      und,      und,      und,      und,      und,      und,      und, '\u00d7',      und, '\u00ac',      und,     und,      und,
      '\u00b0', '\u00b1',      und,      und,      und, '\u00b5',      und,      und,      und,      und, '\u00f7',      und,      und,      und,     und,      und,
           und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,     und,      und,
           und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,     und,      und,
           und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,     und,      und,
           und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,     und,      und,
      ])

    sidney_cyrillic_to_utf8 = remove(sidney_latin1_to_utf8, 0x80, "XXXXXXXXXXXXXXXX"
                                                                  "XXXXXXXXXXXXXXXX"
                                                                  " XXXXXXXXXXXX XX"
                                                                  "XXXXXXXXXXXXXXXX"
                                                                  "XXXXXXXXXXXXXXXX"
                                                                  "XXXXXXXXXXXXXXXX"
                                                                  "XXXXXXXXXXXXXXXX"
                                                                  "XXXXXXXXXXXXXXXX")
    sidney_greek_to_utf8 = sidney_latin9_to_utf8[:]
    sidney_greek_to_utf8 = remove(sidney_greek_to_utf8, 0x80, "            X  X"
                                                              "         X      ")
    sidney_greek_to_utf8 = replace(sidney_greek_to_utf8, 0xb0,
    [
        '\u00b0', '\u00b1',      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,      und,     und,      und,
             und, '\u0391', '\u0392', '\u0393', '\u0394', '\u0395', '\u0396', '\u0397', '\u0398', '\u0399', '\u039a', '\u039b', '\u039c', '\u039d', '\u039e', '\u039f',
        '\u1d28', '\u03a1',      und, '\u03a3', '\u03a4', '\u03a5', '\u03a6', '\u03a7', '\u03a8', '\u03a9',      und,      und,      und,      und,     und,      und,
             und, '\u03b1', '\u03b2', '\u03b3', '\u03b4', '\u03b5', '\u03b6', '\u03b7', '\u03b8', '\u03b9', '\u03ba', '\u03bb', '\u03bc', '\u03bd', '\u03be', '\u03bf',
        '\u03c0', '\u03c1', '\u03c2', '\u03c3', '\u03c4', '\u03c5', '\u03c6', '\u03c7', '\u03c8', '\u03c9',      und,      und,      und,      und,     und,      und
    ])

    # Tick, Cross, Arrows in four directions.
    wimpsymbol_to_utf8 = replace([und]*256, 0x80,
        ['\u2714', und,      und,      und,      '\u2718', und,      und,      und,      '\u21d0', '\u21d2', '\u21d3', '\u21d1', und,      und,      und,      und])

    system_to_utf8 = replace(riscos_latin1_to_utf8, 0x80,
      [ '\u20ac', '\u0174', '\u0175', '\u25F0', '\U0001FBC0', '\u0176', '\u0177', '\u2088\u2077', '\u21E6', '\u21E8', '\u21E9', '\u21E7', '\u2026', '\u2122', '\u2030', '\u2022' ])

    system_fixed_to_utf8 = remove(riscos_latin1_to_utf8, 0x80, "XXXXXXXXXXXX    ")
    system_fixed_latin2_to_utf8 = remove(riscos_latin2_to_utf8, 0x80, "XXXXXXXXXXXX    "
                                                                      "                "
                                                                      "XXXX XX  XXXX XX"
                                                                      " XXX XXX XXXXXXX"
                                                                      "X  X XX X X X  X"
                                                                      "XXX  X  XX X  X "
                                                                      "X  X XX X X X  X"
                                                                      "XXX  X  XX X  XX")
    system_fixed_latin3_to_utf8 = remove(riscos_latin3_to_utf8, 0xa0, " XX   X  XXXX  X"
                                                                      " X    X  XXXX  X"
                                                                      "     XX         "
                                                                      "     X  X    XX "
                                                                      "     XX         "
                                                                      "     X  X    XXX" )
    system_fixed_latin3_to_utf8[0x80] = und
    system_fixed_latin4_to_utf8 = remove(riscos_latin4_to_utf8, 0xa0, " XXX XX  XXXX X "
                                                                      " XXX XXX XXXXXXX"
                                                                      "X      XX X X  X"
                                                                      "XXXX     X   XX "
                                                                      "X      XX X X  X"
                                                                      "XXXX     X   XXX")
    system_fixed_latin4_to_utf8[0x80] = und
    system_fixed_latin5_to_utf8 = remove(riscos_latin5_to_utf8, 0xd0, "X            XX "
                                                                      "                "
                                                                      "X            XX ")
    system_fixed_latin5_to_utf8[0x80] = und
    system_fixed_latin6_to_utf8 = remove(riscos_latin6_to_utf8, 0xa0, " XXXXXX XXXXX XX"
                                                                      " XXXXXX XXXXX XX"
                                                                      "X      XX X X   "
                                                                      " XX    X X      "
                                                                      "X      XX X X   "
                                                                      " XX    X X     X")
    system_fixed_latin6_to_utf8[0x80] = und
    system_fixed_latin7_to_utf8 = remove(riscos_latin7_to_utf8, 0xa0, "          X     "
                                                                      "          X     "
                                                                      "XXXX  XXX XXXXXX"
                                                                      "XXX X   XXXX XX "
                                                                      "XXXX  XXX XXXXXX"
                                                                      "XXX X   XXXX XX ")
    system_fixed_latin7_to_utf8[0x80] = und
    system_fixed_latin8_to_utf8 = remove(riscos_latin8_to_utf8, 0xa0, " XX XXX X XXX  X"
                                                                      "XXXXXX XXXXXXXXX"
                                                                      "                "
                                                                      "X      X      X "
                                                                      "                "
                                                                      "X      X      X ")
    system_fixed_latin8_to_utf8[0x80] = und
    system_fixed_latin9_to_utf8 = remove(riscos_latin9_to_utf8, 0x80, "XXXXXXXXXXXX    "
                                                                      "          XX    "
                                                                      "    X X X       "
                                                                      "    X   X     X ")
    system_fixed_latin9_to_utf8[0x80] = und
    system_fixed_latin10_to_utf8 = remove(riscos_latin10_to_utf8, 0xa0, " XXXX X X X X XX"
                                                                        "  XXX   XXX   XX"
                                                                        "   X X          "
                                                                        "XX   X XX    XX "
                                                                        "   X X          "
                                                                        "XX   X XX    XX ")
    system_fixed_latin10_to_utf8[0x80] = und
    system_fixed_welsh_to_utf8 = remove(riscos_welsh_to_utf8, 0xa0, "        X X X  X"
                                                                    "        X X XXX "
                                                                    "                "
                                                                    "X             X "
                                                                    "                "
                                                                    "X             X ")
    system_fixed_welsh_to_utf8[0x80] = und

    system_fixed_greek_to_utf8 = remove(riscos_greek_to_utf8, 0xa0, "    X")

    #debug_show(sassoon_to_utf8)
    #debug_print_slashu_codes(riscos_latin2_to_utf8)

    # Define each font in each alphabet
    fonts = {
        # default to fall back on if nothing else fits
               "":       {             "": riscos_latin1_to_utf8,
                                 "latin1": riscos_latin1_to_utf8,
                                 "latin2": riscos_latin2_to_utf8,
                                 "latin3": riscos_latin3_to_utf8,
                                 "latin4": riscos_latin4_to_utf8,
                                 "latin5": riscos_latin5_to_utf8,
                                 "latin6": riscos_latin6_to_utf8,
                                 "latin7": riscos_latin7_to_utf8,
                                 "latin8": riscos_latin8_to_utf8,
                                 "latin9": riscos_latin9_to_utf8,
                                "latin10": riscos_latin10_to_utf8,
                                  "welsh": riscos_welsh_to_utf8,
                                 "hebrew": riscos_hebrew_to_utf8,
                               "cyrillic": riscos_cyrillic_to_utf8,
                                  "greek": riscos_greek_to_utf8,
                         },
        "corpus.medium.oblique": {             "": riscos_latin1_to_utf8,
                                         "latin1": riscos_latin1_to_utf8,
                                         "latin2": riscos_latin2_to_utf8,
                                         "latin3": riscos_latin3_to_utf8,
                                         "latin4": riscos_latin4_to_utf8,
                                         "latin5": riscos_latin5_to_utf8,
                                         "latin6": riscos_latin6_to_utf8,
                                         "latin7": riscos_latin7_to_utf8,
                                         "latin8": riscos_latin8_to_utf8,
                                         "latin9": riscos_latin9_to_utf8,
                                        "latin10": riscos_latin10_to_utf8,
                                          "welsh": riscos_welsh_to_utf8,
                                         "hebrew": riscos_hebrew_to_utf8,
                                       "cyrillic": riscos_cyrillic_to_utf8,
                                          "greek": corpus_medium_greek_to_utf8,
                         },
        "corpus.medium": {             "": riscos_latin1_to_utf8,
                                 "latin1": riscos_latin1_to_utf8,
                                 "latin2": riscos_latin2_to_utf8,
                                 "latin3": riscos_latin3_to_utf8,
                                 "latin4": riscos_latin4_to_utf8,
                                 "latin5": riscos_latin5_to_utf8,
                                 "latin6": riscos_latin6_to_utf8,
                                 "latin7": riscos_latin7_to_utf8,
                                 "latin8": riscos_latin8_to_utf8,
                                 "latin9": riscos_latin9_to_utf8,
                                "latin10": riscos_latin10_to_utf8,
                                  "welsh": riscos_welsh_to_utf8,
                                 "hebrew": riscos_hebrew_to_utf8,
                               "cyrillic": riscos_cyrillic_to_utf8,
                                  "greek": corpus_medium_greek_to_utf8,
                         },
        "corpus*":       {             "": riscos_latin1_to_utf8,
                                 "latin1": riscos_latin1_to_utf8,
                                 "latin2": riscos_latin2_to_utf8,
                                 "latin3": riscos_latin3_to_utf8,
                                 "latin4": riscos_latin4_to_utf8,
                                 "latin5": riscos_latin5_to_utf8,
                                 "latin6": riscos_latin6_to_utf8,
                                 "latin7": riscos_latin7_to_utf8,
                                 "latin8": riscos_latin8_to_utf8,
                                 "latin9": riscos_latin9_to_utf8,
                                "latin10": riscos_latin10_to_utf8,
                                  "welsh": riscos_welsh_to_utf8,
                                 "hebrew": riscos_hebrew_to_utf8,
                               "cyrillic": riscos_cyrillic_to_utf8,
                                  "greek": riscos_greek_to_utf8,
                         },
        "homerton*":     {             "": riscos_latin1_to_utf8,
                                 "latin1": riscos_latin1_to_utf8,
                                 "latin2": riscos_latin2_to_utf8,
                                 "latin3": riscos_latin3_to_utf8,
                                 "latin4": riscos_latin4_to_utf8,
                                 "latin5": riscos_latin5_to_utf8,
                                 "latin6": riscos_latin6_to_utf8,
                                 "latin7": riscos_latin7_to_utf8,
                                 "latin8": riscos_latin8_to_utf8,
                                 "latin9": riscos_latin9_to_utf8,
                                "latin10": riscos_latin10_to_utf8,
                                  "welsh": riscos_welsh_to_utf8,
                                 "hebrew": riscos_hebrew_to_utf8,
                               "cyrillic": riscos_cyrillic_to_utf8,
                                  "greek": riscos_greek_to_utf8,
                         },
        "newhall.medium.italic":{              "": newhall_to_utf8,
                                         "latin1": newhall_to_utf8,
                                         "latin2": newhall_latin2_to_utf8,
                                         "latin3": newhall_latin3_to_utf8,
                                         "latin4": newhall_latin4_to_utf8,
                                         "latin5": newhall_latin5_to_utf8,
                                         "latin6": newhall_latin6_to_utf8,
                                         "latin7": newhall_latin7_to_utf8,
                                         "latin8": newhall_latin8_to_utf8,
                                         "latin9": newhall_latin9_with_breve_to_utf8,
                                        "latin10": newhall_latin10_to_utf8,
                                          "welsh": newhall_welsh_to_utf8,
                                         "hebrew": riscos_hebrew_to_utf8,
                                       "cyrillic": riscos_cyrillic_to_utf8,
                                          "greek": newhall_greek_to_utf8,
                         },
        "newhall.medium":{             "": newhall_with_breve_to_utf8,
                                 "latin1": newhall_with_breve_to_utf8,
                                 "latin2": newhall_latin2_to_utf8,
                                 "latin3": newhall_latin3_to_utf8,
                                 "latin4": newhall_latin4_to_utf8,
                                 "latin5": newhall_latin5_to_utf8,
                                 "latin6": newhall_latin6_to_utf8,
                                 "latin7": newhall_latin7_to_utf8,
                                 "latin8": newhall_latin8_to_utf8,
                                 "latin9": newhall_latin9_with_breve_to_utf8,
                                "latin10": newhall_latin10_to_utf8,
                                  "welsh": newhall_welsh_to_utf8,
                                 "hebrew": riscos_hebrew_to_utf8,
                               "cyrillic": riscos_cyrillic_to_utf8,
                                  "greek": newhall_greek_to_utf8,
                         },
        "newhall*":      {             "": newhall_to_utf8,
                                 "latin1": newhall_to_utf8,
                                 "latin2": newhall_latin2_to_utf8,
                                 "latin3": newhall_latin3_to_utf8,
                                 "latin4": newhall_latin4_to_utf8,
                                 "latin5": newhall_latin5_to_utf8,
                                 "latin6": newhall_latin6_to_utf8,
                                 "latin7": newhall_latin7_to_utf8,
                                 "latin8": newhall_latin8_to_utf8,
                                 "latin9": newhall_latin9_to_utf8,
                                "latin10": newhall_latin10_to_utf8,
                                  "welsh": newhall_welsh_to_utf8,
                                 "hebrew": riscos_hebrew_to_utf8,
                               "cyrillic": riscos_cyrillic_to_utf8,
                                  "greek": newhall_greek_to_utf8,
                         },
        "sassoon*":      {             "": sassoon_to_utf8,
                                 "latin1": sassoon_to_utf8,
                                 "latin2": sassoon_latin2_to_utf8,
                                 "latin3": sassoon_latin3_to_utf8,
                                 "latin4": sassoon_latin4_to_utf8,
                                 "latin5": sassoon_latin5_to_utf8,
                                 "latin6": sassoon_latin6_to_utf8,
                                 "latin7": sassoon_latin7_to_utf8,
                                 "latin8": sassoon_latin8_to_utf8,
                                 "latin9": sassoon_latin9_to_utf8,
                                "latin10": sassoon_latin10_to_utf8,
                                  "welsh": sassoon_welsh_to_utf8,
                                 "hebrew": sassoon_hebrew_to_utf8,
                               "cyrillic": riscos_cyrillic_to_utf8,
                                  "greek": sassoon_greek_to_utf8,
                         },
        "sidney":        {             "": sidney_to_utf8,
                                 "latin1": sidney_latin1_to_utf8,
                                 "latin2": sidney_latin2_to_utf8,
                                 "latin3": sidney_latin3_to_utf8,
                                 "latin4": sidney_latin4_to_utf8,
                                 "latin5": sidney_latin5_to_utf8,
                                 "latin6": sidney_latin6_to_utf8,
                                 "latin7": sidney_latin7_to_utf8,
                                 "latin8": sidney_latin8_to_utf8,
                                 "latin9": sidney_latin9_to_utf8,
                                "latin10": sidney_latin10_to_utf8,
                                  "welsh": sidney_welsh_to_utf8,
                                 "hebrew": sidney_hebrew_to_utf8,
                               "cyrillic": sidney_cyrillic_to_utf8,
                                  "greek": sidney_greek_to_utf8,
                         },
        "system":        {             "": system_to_utf8,
                                 "latin1": system_to_utf8,
                                 "latin2": system_to_utf8,
                                 "latin3": system_to_utf8,
                                 "latin4": system_to_utf8,
                                 "latin5": system_to_utf8,
                                 "latin6": system_to_utf8,
                                 "latin7": system_to_utf8,
                                 "latin8": system_to_utf8,
                                 "latin9": system_to_utf8,
                                "latin10": system_to_utf8,
                                  "welsh": system_to_utf8,
                                 "hebrew": system_to_utf8,
                               "cyrillic": system_to_utf8,
                                  "greek": system_to_utf8,
                         },
        "trinity*":      {             "": riscos_latin1_to_utf8,
                                 "latin1": riscos_latin1_to_utf8,
                                 "latin2": riscos_latin2_to_utf8,
                                 "latin3": riscos_latin3_to_utf8,
                                 "latin4": riscos_latin4_to_utf8,
                                 "latin5": riscos_latin5_to_utf8,
                                 "latin6": riscos_latin6_to_utf8,
                                 "latin7": riscos_latin7_to_utf8,
                                 "latin8": riscos_latin8_to_utf8,
                                 "latin9": riscos_latin9_to_utf8,
                                "latin10": riscos_latin10_to_utf8,
                                  "welsh": riscos_welsh_to_utf8,
                                 "hebrew": riscos_hebrew_to_utf8,
                               "cyrillic": riscos_cyrillic_to_utf8,
                                  "greek": riscos_greek_to_utf8,
                         },
        "selwyn":        {             "": selwyn_to_utf8,                # Only defined for 'no alphabet'
                         },
        "swiss*":        {             "": swiss_to_utf8,
                                 "latin1": swiss_latin1_to_utf8,
                                 "latin2": swiss_latin2_to_utf8,
                                 "latin3": swiss_latin3_to_utf8,
                                 "latin4": swiss_latin4_to_utf8,
                                 "latin5": swiss_latin5_to_utf8,
                                 "latin6": swiss_latin6_to_utf8,
                                 "latin7": swiss_latin7_to_utf8,
                                 "latin8": swiss_latin8_to_utf8,
                                 "latin9": swiss_latin9_to_utf8,
                                "latin10": swiss_latin10_to_utf8,
                                  "welsh": swiss_welsh_to_utf8,
                                 "hebrew": riscos_hebrew_to_utf8,
                               "cyrillic": riscos_cyrillic_to_utf8,
                                  "greek": swiss_greek_to_utf8,
                         },
        "system.fixed":  {             "": system_fixed_to_utf8,
                                 "latin1": system_fixed_to_utf8,
                                 "latin2": system_fixed_latin2_to_utf8,
                                 "latin3": system_fixed_latin3_to_utf8,
                                 "latin4": system_fixed_latin4_to_utf8,
                                 "latin5": system_fixed_latin5_to_utf8,
                                 "latin6": system_fixed_latin6_to_utf8,
                                 "latin7": system_fixed_latin7_to_utf8,
                                 "latin8": system_fixed_latin8_to_utf8,
                                 "latin9": system_fixed_latin9_to_utf8,
                                "latin10": system_fixed_latin10_to_utf8,
                                  "welsh": system_fixed_welsh_to_utf8,
                                 "hebrew": riscos_hebrew_to_utf8,
                               "cyrillic": riscos_cyrillic_to_utf8,
                                  "greek": system_fixed_greek_to_utf8,
                         },
        "system.medium": {             "": system_fixed_to_utf8,
                                 "latin1": system_fixed_to_utf8,
                                 "latin2": system_fixed_latin2_to_utf8,
                                 "latin3": system_fixed_latin3_to_utf8,
                                 "latin4": system_fixed_latin4_to_utf8,
                                 "latin5": system_fixed_latin5_to_utf8,
                                 "latin6": system_fixed_latin6_to_utf8,
                                 "latin7": system_fixed_latin7_to_utf8,
                                 "latin8": system_fixed_latin8_to_utf8,
                                 "latin9": system_fixed_latin9_to_utf8,
                                "latin10": system_fixed_latin10_to_utf8,
                                  "welsh": system_fixed_welsh_to_utf8,
                                 "hebrew": riscos_hebrew_to_utf8,
                               "cyrillic": riscos_cyrillic_to_utf8,
                                  "greek": system_fixed_greek_to_utf8,
                         },
        "wimpsymbol":    {             "": wimpsymbol_to_utf8,            # Only defined for 'no alphabet'
                         },

    }

    # Define palettes (used when converting sprites)

    # 4bpp (16 colours)
    colpal16 = [255,255,255, 255] + [221,221,221, 255] + [187,187,187, 255] + [153,153,153, 255] + \
               [119,119,119, 255] + [85,85,85, 255]    + [51,51,51, 255]    + [0,0,0, 255]       + \
               [0,68,153, 255]    + [238,238,0, 255]   + [0,204,0, 255]     + [221,0,0, 255]     + \
               [238,238,187, 255] + [85,136,0, 255]    + [255,187,0, 255]   + [0,187,255, 255]

    # 2bpp (4 colours)
    colpal4  = [0,0,0, 255]       + [96,96,96, 255]    + [192,192,192, 255] + [255,255,255, 255]

    # 1bpp (2 colours)
    colpal2  = [255,255,255, 255] + [0,0,0, 255]

    class Mode:
        def __init__(self, mode, bpp, xf, yf):
            self.mode = mode
            self.bpp = bpp

            # Scale factors (double width or double height)
            self.xf = xf
            self.yf = yf

    # RISC OS Mode number information
    modes = {
        0: Mode(0, 1, 1, 2),
        1: Mode(1, 2, 2, 2),
        2: Mode(2, 4, 3, 2),
                                  # MODE 3 is text only
        4: Mode(4, 1, 2, 2),
        5: Mode(5, 2, 3, 2),
                                  # MODE 6 is text only
                                  # MODE 7 is teletext
        8: Mode(8, 2, 1, 2),
        9: Mode(9, 4, 2, 2),
        10: Mode(10, 8, 3, 2),
        11: Mode(11, 2, 1, 2),
        12: Mode(12, 4, 1, 2),
        13: Mode(13, 8, 2, 2),
        14: Mode(14, 4, 1, 2),
        15: Mode(15, 8, 1, 2),
        16: Mode(16, 4, 0, 2),
        17: Mode(17, 4, 0, 2),
        18: Mode(18, 1, 1, 1),
        19: Mode(19, 2, 1, 1),
        20: Mode(20, 4, 1, 1),
        21: Mode(21, 8, 1, 1),
        22: Mode(22, 4, 1, 2),
        23: Mode(23, 1, 1, 1),
        24: Mode(24, 8, 0, 2),
        25: Mode(25, 1, 1, 1),
        26: Mode(26, 2, 1, 1),
        27: Mode(27, 4, 1, 1),
        28: Mode(28, 8, 1, 1),
        29: Mode(29, 1, 1, 1),
        30: Mode(30, 2, 1, 1),
        31: Mode(31, 4, 1, 1),
        32: Mode(32, 8, 1, 1),
        33: Mode(33, 1, 1, 2),
        34: Mode(34, 2, 1, 2),
        35: Mode(35, 4, 1, 2),
        36: Mode(36, 8, 1, 2),
        37: Mode(37, 1, 1, 2),
        38: Mode(38, 2, 1, 2),
        39: Mode(39, 4, 1, 2),
        40: Mode(40, 8, 1, 2),
        41: Mode(41, 1, 1, 2),
        42: Mode(42, 2, 1, 2),
        43: Mode(43, 4, 1, 2),
        44: Mode(44, 1, 1, 2),
        45: Mode(45, 2, 1, 2),
        46: Mode(46, 4, 1, 2),
        47: Mode(47, 8, 2, 2),
        48: Mode(48, 4, 2, 1),
        49: Mode(49, 8, 2, 1)
    }

    # Mode Flags
    ModeFlag_NonGraphic             = 1<<0
    ModeFlag_Teletext               = 1<<1
    ModeFlag_GapMode                = 1<<2
    ModeFlag_BBCGapMode             = 1<<3
    ModeFlag_HiResMono              = 1<<4
    ModeFlag_DoubleVertical         = 1<<5
    ModeFlag_HardScrollDisabled     = 1<<6      # set when outputting to a sprite, or driver doesn't support VIDC style scrolling
    ModeFlag_FullPalette            = 1<<7      # set when palette is not brain damaged
    ModeFlag_64k                    = ModeFlag_FullPalette
                                                # Used with log2bpp==4 to indicate 565 RGB/BGR mode
    ModeFlag_InterlacedMode         = 1<<8      # set when interlaced mode with hardware using two seperate framebuffers
    ModeFlag_GreyscalePalette       = 1<<9      # all entries greyscale, but no defined order
    ModeFlag_ChromaSubsampleMode    = ModeFlag_GreyscalePalette
                                                # Used with log2bpp==7 to indicate chroma mode
                                                # bits 10-11 reserved
    ModeFlag_DataFormat_Mask        = 0xF<<12
    ModeFlag_DataFormatFamily_Mask  = 3<<12     # 0=RGB, 1=misc (CMYK), 2=YCbCr, 3=reserved
    ModeFlag_DataFormatFamily_RGB   = 0<<12
    ModeFlag_DataFormatFamily_Misc  = 1<<12
    ModeFlag_DataFormatFamily_YCbCr = 2<<12
    ModeFlag_DataFormatSub_Mask     = 0xC<<12   # RGB: b14 = RGB order (0=&ABGR, 1=&ARGB)
                                                #      b15 = alpha mode (0=transfer/supremacy, 1=alpha)
                                                # misc: 2_00 = &KYMC
                                                # YCbCr: b14 = range (0=full, 1=video)
                                                #        b15 = standard (0=ITU-R BT.601, 1=ITU-R BT.709)
    ModeFlag_DataFormatSub_RGB      = 4<<12     # 0=&xBGR, 1=&xRGB
    ModeFlag_DataFormatSub_Alpha    = 8<<12     # 0=transfer/supremacy, 1=alpha
    ModeFlag_DataFormatSub_Video    = 4<<12     # 0=full range, 1=video range
    ModeFlag_DataFormatSub_709      = 8<<12     # 0=ITU-R BT.601, 1=ITU-R BT.709
    ModeFlag_Transform_Mask         = 7<<16
    ModeFlag_Transform_Rotate90     = 1<<16
    ModeFlag_Transform_Rotate180    = 2<<16
    ModeFlag_Transform_VFlip        = 4<<16


    # [ncolour, modeflags, log2bpp]
    pixelformats = [
        [1,0,0],
        [3,0,1],
        [15,0,2],
        [255,ModeFlag_FullPalette,3],
        [65535,0,4],
        [-1,0,5],
        # RISC OS 6 64K
        [65535,  ModeFlag_64k,         4],
        # Red/blue swapped
        [65535,  ModeFlag_DataFormatSub_RGB,              4],
        [-1,     ModeFlag_DataFormatSub_RGB,              5],
        [65535,  ModeFlag_DataFormatSub_RGB+ModeFlag_64k, 4],
        # 4K
        [4095,   0,                                       4],
        [4095,   ModeFlag_DataFormatSub_RGB,              4],
        # Alpha
        [65535,  ModeFlag_DataFormatSub_Alpha,                                         4],
        [-1,     ModeFlag_DataFormatSub_Alpha,                                         5],
        [65535,  ModeFlag_DataFormatSub_Alpha+ModeFlag_64k,                            4],
        [65535,  ModeFlag_DataFormatSub_Alpha+ModeFlag_DataFormatSub_RGB,              4],
        [-1,     ModeFlag_DataFormatSub_Alpha+ModeFlag_DataFormatSub_RGB,              5],
        [65535,  ModeFlag_DataFormatSub_Alpha+ModeFlag_DataFormatSub_RGB+ModeFlag_64k, 4],
        [4095,   ModeFlag_DataFormatSub_Alpha,                                         4],
        [4095,   ModeFlag_DataFormatSub_Alpha+ModeFlag_DataFormatSub_RGB,              4],
    ]

    # Classes to hold data as read from a Draw file
    class Coords:
        """Stores an (x,y) integer position in Draw coordinates"""

        def __init__(self, x=0, y=0):
            self.x = x
            self.y = y

        def size():
            # returns size in bytes in binary draw file
            return 8

        def read(self, f):
            self.x = Convertor.read_int(f)
            self.y = Convertor.read_int(f)

        def __repr__(self):
            return "({0},{1})".format(self.x, self.y)


    class ColourType:
        def __init__(self, red = 0, green = 0, blue = 0):
            self.reserved = 0
            self.red      = Convertor.clamp(red, 0, 255)
            self.green    = Convertor.clamp(green, 0, 255)
            self.blue     = Convertor.clamp(blue, 0, 255)

        def size():
            # returns size in bytes in binary draw file
            return 4

        def read(self, f):
            self.reserved = Convertor.read_uint(f,1)
            self.red      = Convertor.read_uint(f,1)
            self.green    = Convertor.read_uint(f,1)
            self.blue     = Convertor.read_uint(f,1)

        def __repr__(self):
            return "#{0:02X}{1:02X}{2:02X}".format(self.red, self.green, self.blue)

    class Options:
        """Options for the Draw file"""

        def __init__(self):
            self.paper_size             = 0x100     # Defaults to A0
            self.paper_limits           = 0         # Portrait

            # The remainder are variables only used when editing in !Draw.
            # We store the information but do not use it.

            # The grid is a visual guide when editing in !Draw.
            self.grid_spacing           = 0.0
            self.grid_division          = 0
            self.grid_type              = 0
            self.grid_auto_adjustment   = 0
            self.grid_shown             = 0
            self.grid_locking           = 0
            self.grid_units             = 0

            # The zoom is the current scale when editing in !Draw.
            self.zoom_multiplier        = 0
            self.zoom_divider           = 0
            self.zoom_locking           = 0

            self.toolbox_presence       = 0
            self.initial_entry_mode     = 0
            self.undo_buffer_size       = 0

        def size():
            return 64

        def paper_size_mm(self):
            """Converts the paper size in the Draw file Options into millimetres."""

            if self.paper_size in Convertor.paper_sizes:
                result = Convertor.paper_sizes[self.paper_size]
                if (self.paper_limits & 16) != 0:
                    # Landscape, swap the dimensions
                    result = (result[1], result[0])
                return result

            error("Unknown paper size {0}".format(self.paper_size))
            exit(1)

        def read(self, f):
            """Read the Options from the draw file"""

            self.paper_size           = Convertor.read_int(f)
            self.paper_limits         = Convertor.read_int(f)
            self.grid_spacing         = Convertor.read_float(f)
            self.grid_division        = Convertor.read_int(f)
            self.grid_type            = Convertor.read_int(f)
            self.grid_auto_adjustment = Convertor.read_int(f)
            self.grid_shown           = Convertor.read_int(f)
            self.grid_locking         = Convertor.read_int(f)
            self.grid_units           = Convertor.read_int(f)
            self.zoom_multiplier      = Convertor.read_int(f)
            self.zoom_divider         = Convertor.read_int(f)
            self.zoom_locking         = Convertor.read_int(f)
            self.toolbox_presence     = Convertor.read_int(f)
            self.initial_entry_mode   = Convertor.read_int(f)
            self.undo_buffer_size     = Convertor.read_int(f)

    class TextHeader:
        """Header information for regular text objects in the Draw file"""

        def __init__(self):
            self.colour = Convertor.ColourType()
            self.bgcolourhint = Convertor.ColourType()
            self.style = 0
            self.xsize = 0              # in 1/640 point
            self.ysize = 0              # in 1/640 point
            self.baseline = Convertor.Coords()

        def size():
            # returns size in bytes in binary draw file
            return 16 + Convertor.ColourType.size() + Convertor.Coords.size()

        def read(self, f):
            self.colour.read(f)
            self.bgcolourhint.read(f)
            self.style = Convertor.read_uint(f)
            self.xsize = Convertor.read_uint(f)
            self.ysize = Convertor.read_uint(f)
            self.baseline.read(f)

    class PathStyleType:
        def __init__(self):
            self.joinstyle = 0
            self.endcapstyle = 0
            self.startcapstyle = 0
            self.winding = 0
            self.dash = 0
            self.reserved = 0
            self.tricapwidth = 0        # in 1/16ths of outline width
            self.tricaplength = 0       # in 1/16ths of outline width

        def size():
            # returns size in bytes in binary draw file
            return 4

        def read(self, f):
            byte1 = Convertor.read_uint(f, 1)
            self.joinstyle     = byte1 & 3
            self.endcapstyle   = (byte1 >> 2) & 3
            self.startcapstyle = (byte1 >> 4) & 3
            self.winding       = (byte1 >> 6) & 1
            self.dash          = (byte1 >> 7) & 1
            self.reserved      = Convertor.read_uint(f, 1)
            self.tricapwidth   = Convertor.read_uint(f, 1)
            self.tricaplength  = Convertor.read_uint(f, 1)

    class PathHeader:
        def __init__(self):
            self.fillcolour    = Convertor.ColourType()
            self.outlinecolour = Convertor.ColourType()
            self.outlinewidth  = 0      # Draw units
            self.style         = Convertor.PathStyleType()

        def size():
            # returns size in bytes in binary draw file
            return 2*Convertor.ColourType.size() + 4  + Convertor.PathStyleType.size()

        def read(self, f):
            self.fillcolour.read(f)
            self.outlinecolour.read(f)
            self.outlinewidth = Convertor.read_uint(f)
            self.style.read(f)

    class DrawMatrix:
        # a-d are fixed point '16.16' values
        # e-f are the translation (in draw units)
        def __init__(self):
            self.a = 0x10000
            self.b = 0
            self.c = 0
            self.d = 0x10000
            self.e = 0
            self.f = 0

        def size():
            # returns size in bytes in binary draw file
            return 24

        def read(self, f):
            self.a = Convertor.read_int(f)
            self.b = Convertor.read_int(f)
            self.c = Convertor.read_int(f)
            self.d = Convertor.read_int(f)
            self.e = Convertor.read_int(f)
            self.f = Convertor.read_int(f)

        def __repr__(matrix):
            return("   {0}    {1}    {2}\n"
                   "   {3}    {4}    {5}\n"
                   "   0    0    1".format(matrix.a, matrix.c, matrix.e, matrix.b, matrix.d, matrix.f))


    class JpegHeader:
        # JPEG object header format: See http://www.riscos.com/support/developers/prm/fileformat.html
        def __init__(self):
            self.width  = 0     # in draw units
            self.height = 0     # in draw units
            self.x_dpi  = 0     # pixels per inch
            self.y_dpi  = 0     # pixels per inch
            self.transform = Convertor.DrawMatrix()
            self.length = 0

        def size():
            # returns size in bytes in binary draw file
            return 44

        def read(self, f):
            self.width  = Convertor.read_uint(f)
            self.height = Convertor.read_uint(f)
            self.x_dpi  = Convertor.read_uint(f)
            self.y_dpi  = Convertor.read_uint(f)
            self.transform.read(f)
            self.length = Convertor.read_uint(f)

    class SpriteCtrlBlock:
        def __init__(self):
            self.nextsprite = 0
            self.name       = ""
            self.width      = 0
            self.height     = 0
            self.firstbit   = 0
            self.lastbit    = 0
            self.image      = 0
            self.mask       = 0
            self.mode       = 0

        def size():
            # returns size in bytes in binary draw file
            return 44

        def read(self, f):
            self.nextsprite = Convertor.read_uint(f)
            self.name       = Convertor.read_name_string(f, 12).strip()
            self.width      = Convertor.read_uint(f)
            self.height     = Convertor.read_uint(f)
            self.firstbit   = Convertor.read_uint(f)
            self.lastbit    = Convertor.read_uint(f)
            self.image      = Convertor.read_uint(f)     # Offset to image
            self.mask       = Convertor.read_uint(f)     # Offset to mask
            self.mode       = Convertor.read_uint(f)

        def __repr__(self):
            return "NextSprite:{0}\nname:{1}\nwidth:{2}\nheight{3}\nfirstbit:{4}\nlastbit:{5}\nimage:{6}\nmask:{7}\nmode:{8}\n".format(
                    self.nextsprite,self.name,self.width,self.height,self.firstbit,self.lastbit,hex(self.image),hex(self.mask),self.mode)

    class Configure:
        """Stores the tool's configuration in one handy class"""

        def __init__(self):
            # Defaults for all configuration values
            self.verbose_level                  = 0
            self.utf8                           = False
            self.use_tspans                     = False
            self.show_debug_index               = False
            self.show_bounding_boxes            = False
            self.basic_underlines               = False
            self.use_bbox                       = True
            self.fonts_ini                      = None
            self.fit_border                     = None
            self.one_byte_types                 = False

    def __init__(self):
        # Calculate default 256 colour palette, stored in RGBA order
        def makecolpal256(colpal256):
            # palette indices are %bggrbrtt (PRM 3-339)
            for i in range(256):
                tint = i&3
                r = ((i&16)>>3) | ((i&4)>>2)
                g = (i&0x60) >> 5
                b = ((i&128)>>6) | ((i&8)>>3)

                colpal256[4*i+0] = ((r*4+tint)*0x11)
                colpal256[4*i+1] = ((g*4+tint)*0x11)
                colpal256[4*i+2] = ((b*4+tint)*0x11)
                colpal256[4*i+3] = 255

        # 8bpp (256 colours)
        Convertor.colpal256 = [0 for x in range(256*4)]
        makecolpal256(Convertor.colpal256)

        self.fonts = {}

        # Add system font
        self.fonts[0] = Convertor.FontDesc("system", 24, 24, Convertor.default_font_replacements)

        # Variables
        self.cc = None                          # A Coordinate Conversion object.
        self.options = None                     # One Draw options object per file. Optional.
        self.config = Convertor.Configure()     # Current tool configuration.

    # Utility functions (class methods) for reading from Draw file
    def eof(f, size):
        return f.tell() == size

    def read_int(f, num_bytes = 4):
        if num_bytes == 4:
            return struct.unpack('<i',f.read(4))[0]
        if num_bytes == 2:
            return struct.unpack('<h',f.read(2))[0]
        if num_bytes == 1:
            return struct.unpack('<b',f.read(1))[0]
        raise ValueError('Trying to read {0} bytes when reading an integer, which is unsupported.'.format(num_bytes))
        return 0

    def read_uint(f, num_bytes = 4):
        if num_bytes == 4:
            return struct.unpack('<I',f.read(4))[0]
        if num_bytes == 2:
            return struct.unpack('<H',f.read(2))[0]
        if num_bytes == 1:
            return struct.unpack('<B',f.read(1))[0]
        raise ValueError('Trying to read {0} bytes when reading an unsigned integer, which is unsupported.'.format(num_bytes))
        return 0

    def peek_uint(f, num_bytes = 4):
        pos = f.tell()
        result = Convertor.read_uint(f, num_bytes)
        f.seek(pos)
        return result

    def read_name_string(f, length, utf8=False):
        """Reads exactly 'length' bytes, and decodes into a string."""
        raw_text = f.read(length).split(b'\x00')[0]

        if utf8:
            return raw_text.decode('utf-8')

        # Convert bytes to UTF-8, based on the standard character set
        result = ""
        for i in raw_text:
            # Decode using the standard character set.
            result += Convertor.riscos_latin1_to_utf8[i]
        return result

    def read_bytes_until_zero(f):
        result = b''
        while True:
            raw_byte = f.read(1)
            if raw_byte == b'\x00':
                break
            result += raw_byte
        return result


    def decode_bytes_to_utf8(text, font_name, alphabet):
        font_name = font_name.lower()
        alphabet = alphabet.lower()
        result = ""
        append_next = ""
        if font_name in Convertor.fonts:
            key = font_name
        elif font_name + "*" in Convertor.fonts:
            key = font_name + "*"
        elif font_name.split(".")[0] in Convertor.fonts:
            key = font_name.split(".")[0]
        elif font_name.split(".")[0] + "*" in Convertor.fonts:
            key = font_name.split(".")[0] + "*"
        else:
            key = ""

        alphabet_dict = Convertor.fonts[key]
        if alphabet in alphabet_dict:
            character_set = alphabet_dict[alphabet]
        elif alphabet == "utf8":
            character_set = [chr(x) for x in range(256)]
        else:
            character_set = [und] * 256

        for i in text:
            if i == 10:
                result += '\n'
                append_next = ""
            else:
                c = character_set[i]

                if c == "OVERLINE":
                    append_next = "\u0305"
                    result += " "
                else:
                    result += c + append_next
                    append_next = ""

        # Replace any final soft hyphen with an actual hyphen
        if len(result) > 0:
            if result[-1] == '\u00ad':  # soft-hyphen
                result = result[0:-1] + '-'

        # If an overline character is left hanging at the end, include it
        if append_next != "":
            result += " " + append_next
        return result


    def read_string(f, length=0, font="", alphabet="", utf8=False):
        """Reads a string until 'length' bytes or a zero byte are read."""
        result = []
        font = font.lower()

        append_next = ""
        while True:
            raw_byte = f.read(1)
            if raw_byte == b'\x00':
                break
            length -= 1
            if length == 0:
                break

            # Remember each byte in an array, to decode at the end
            result += raw_byte

        if utf8:
            # decode byte array into a UTF-8 string
            return bytes(result).decode('utf-8')

        return Convertor.decode_bytes_to_utf8(result, font, alphabet)

    def read_float(f):
        return f.read(8)

    def skip_to_word_boundary(fin):
        while (fin.tell() & 3) != 0:
            fin.read(1)

    # Other utility functions
    def clamp(n, smallest, largest):
        return max(smallest, min(n, largest))

    def latin1_to_utf8(originalname):
        result = ""
        for i in originalname:
            # The default character set is based on latin-1, but it's not
            # precisely latin-1, since it has extra glyphs added.
            result += Convertor.riscos_latin1_to_utf8[i]
        return result

    # Utility functions to be used when writing to SVG
    def escape( str_xml: str ):
        # See https://stackoverflow.com/a/28703510
        str_xml = str_xml.replace("&", "&amp;")
        str_xml = str_xml.replace("<", "&lt;")
        str_xml = str_xml.replace(">", "&gt;")
        str_xml = str_xml.replace('"', "&quot;")
        str_xml = str_xml.replace("'", "&apos;")
        return str_xml

    # Functions for looking up font information
    def findfontname(self, text_style):
        if text_style in self.fonts:
            return self.fonts[text_style].name
        return ""

    def findoriginalfullfontname(self, text_style):
        if text_style in self.fonts:
            return self.fonts[text_style].originalfullname
        return ""

    def findoriginalfontname(self, text_style):
        if text_style in self.fonts:
            return self.fonts[text_style].originalname
        return ""

    def findalphabet(self, text_style):
        if text_style in self.fonts:
            return self.fonts[text_style].alphabet
        return ""

    def findfontweight(self, text_style):
        if text_style in self.fonts:
            return self.fonts[text_style].weight
        return ""

    def findfontstyle(self, text_style):
        if text_style in self.fonts:
            return self.fonts[text_style].style
        return ""

    def formatfontsize(self, svg_fontsize_pts, text_style):
        # HACK: Make the BBC Micro style font larger than regular fonts
        if self.findoriginalfontname(text_style).lower() == "system":
            return self.dp(svg_fontsize_pts.x * 4/3)
        return self.dp(svg_fontsize_pts.x)


    class FontDesc:
        def __init__(self, originalname, size, width, font_replacements):
            self.height_pts = size       # font height in pts
            self.width_pts  = width      # font width in pts (default is equal to height_pts)
            self.font = None
            self.font_replacements = font_replacements
            alphabet = ""

            if isinstance(originalname, (bytes, bytearray)):
                originalname = Convertor.latin1_to_utf8(originalname)

            # Look for e.g. "\FCorpus.Medium\ELatin3" format string
            # (See https://riscosopen.org/forum/forums/4/topics/3903)
            # (See https://riscosopen.org/wiki/documentation/show/Font%20Identifier%20String)
            # (See http://www.riscos.com/support/developers/prm/fontmanager.html#52957)
            matched1 = re.search(r"\\F(.*)", originalname)
            matched2 = re.search(r"\\E(.*)", originalname)

            if matched1:
                originalname = matched1.group(1)
            if matched2:
                alphabet     = matched2.group(1)

            parts = originalname.split('.')

            self.originalfullname = originalname
            self.originalname = parts[0]
            self.alphabet     = alphabet
            font = parts[0]

            lower_name = font.lower()
            if lower_name in self.font_replacements:
                self.name = self.font_replacements[lower_name]
            else:
                warning("Unknown font '{0}'".format(font))
                self.name = font + font_replacements['_default']

            # Default font weight/style
            self.weight = "normal"
            self.style = "normal"

            sans_serif = (lower_name == "swiss") or (lower_name == "system")

            # HACK: To approximate something akin to a BBC Micro style bitmap font, we make the system font bold
            if lower_name == "system":
                self.weight = "bold"

            additional_parts = parts[1:]
            for part in additional_parts:
                lower_part = part.lower()
                if lower_part == "monospaced":
                    if sans_serif:
                        self.name = '"Menlo","Lucida Console","Courier New",Courier,monospace'
                    else:
                        self.name = '"Courier New",Courier,"Lucida Console",monospace'
                elif lower_part == "italic":
                    self.style = "italic"
                elif lower_part == "oblique":
                    self.style = "italic"
                elif lower_part == "bold":
                    self.weight = "bold"

        def __repr__(self):
            return "'{0}' mapped to {1} {2} {3}".format(self.originalname, self.name, self.weight, self.style)


    class ObjectHeader:
        """Each object in the Draw file has this header"""

        def __init__(self):
            self.obj_type = 0
            self.obj_length = 0
            self.low = Convertor.Coords()               # Bounding box, in draw units
            self.high = Convertor.Coords()              # Bounding box, in draw units

        def read(self, f, config):
            if config.one_byte_types:
                self.obj_type   = Convertor.read_uint(f) & 255
            else:
                self.obj_type   = Convertor.read_uint(f) & 65535
            self.obj_length = Convertor.read_uint(f)
            self.low.read(f)
            self.high.read(f)

        def print(self, verbose_level):
            message(verbose_level, "Object")

        def size():
            return 8 + 2*Convertor.Coords.size()

    class FileHeader:
        def __init__(self):
            self.magic = 0
            self.major = 0
            self.minor = 0
            self.creator = ""
            self.low_box = Convertor.Coords()           # Bounding box, in draw units
            self.high_box = Convertor.Coords()          # Bounding box, in draw units

        def read(self, f):
            if os.fstat(f.fileno()).st_size >= 4:
                self.magic = Convertor.read_uint(f)
                if self.magic != 0x77617244:
                    error('Wrong magic number. Is this a Draw file?')
                    return False
            else:
                error('File is less than four bytes long.')
                return False

            self.major = Convertor.read_uint(f)
            self.minor = Convertor.read_uint(f)
            self.creator = Convertor.read_name_string(f, 12).strip()
            self.low_box.read(f)
            self.high_box.read(f)
            return True

        def print(self, convertor, p, verbose_level):
           message(verbose_level, "File      : {0}".format(p))
           message(verbose_level, " Magic num: {0}".format(hex(self.magic)))
           message(verbose_level, " Major ver: {0}".format(self.major))
           message(verbose_level, " Minor ver: {0}".format(self.minor))
           message(verbose_level, " Creator  : {0}".format(self.creator))
           message(verbose_level, " Bound-Box: {0},{1} to {2},{3}".format(
                    self.low_box.x,
                    self.low_box.y,
                    self.high_box.x,
                    self.high_box.y))

    def dp(self, f):
        return "{0:.4f}".format(f)

    def read_font_table_object(self, fin, object_header, curptr):
        fin.seek(curptr+8, 0)

        while fin.tell() < curptr+object_header.obj_length:
            number = Convertor.read_uint(fin, 1)
            if number == 0:
                Convertor.skip_to_word_boundary(fin)
                break
            originalname = Convertor.read_string(fin)
            self.fonts[number] = Convertor.FontDesc(originalname, 24, 24, self.font_replacements)
            message(2, "  Font number {0} is '{1}' alphabet: '{2}'".format(number, self.fonts[number].originalname, self.fonts[number].alphabet))

    def colour_name(self, colour):
        i_colour = 65536*colour.red + 256*colour.green + colour.blue
        if i_colour in colour_names:
            return colour_names[i_colour].lower()
        return "#{0:02x}{1:02x}{2:02x}".format(colour.red, colour.green, colour.blue)

    def read_text_object(self, fin, fout, object_header, text_header, text_width = None, font_flags=1, transform="", pos=None):
        text_length = object_header.obj_length - Convertor.ObjectHeader.size() - Convertor.TextHeader.size()
        if object_header.obj_type == Convertor.OBJECT_TRANSTEXT:
            text_length -= Convertor.DrawMatrix.size() + 4          # Matrix + font flags

        # A text object consists of an object header, text header (these are already read at this
        # point), then the text itself, then padding.

        # Get RISC OS font name, e.g. trinity, selwyn, newhall etc.
        # This is needed so the characters get translated properly from the current font
        # specific character codes to UTF-8.
        current_original_font_name = self.findoriginalfullfontname(text_header.style)
        current_alphabet           = self.findalphabet(text_header.style)

        # Read text
        text = Convertor.read_string(fin, text_length, current_original_font_name, current_alphabet, self.config.utf8)

        # Skip final padding
        Convertor.skip_to_word_boundary(fin)

        svg_fontsize_pixels = self.cc.draw_to_svg_size(Convertor.Coords(text_header.xsize, text_header.ysize))
        svg_fontsize_pts    = CoordinateConversion.px_to_pt(svg_fontsize_pixels)

        message(2, "  Text Object: '{0}'\n   Font: {1} mapped to '{2}'\n   Fontsize: {3} pt x {4} pt\n   Colour: ({5} {6} {7})".format(
            text,
            text_header.style,
            self.findfontname(text_header.style),
            self.dp(svg_fontsize_pts.x), self.dp(svg_fontsize_pts.y),
            text_header.colour.red,
            text_header.colour.green,
            text_header.colour.blue))

        bottom_left = self.cc.draw_to_svg_point(object_header.low)
        top_right   = self.cc.draw_to_svg_point(object_header.high)

        if pos == None:
            pos = self.cc.draw_to_svg_point(Convertor.Coords(text_header.baseline.x, text_header.baseline.y))
            # We actually use the bottom left of the bounding box. This is because of an example file
            # 'Metro.c56' created by the 'Vector' application which can specify the baseline position
            # as an anchor point halfway along the box.
            pos.x = bottom_left.x

        if text_width == None:
            text_width = top_right.x - bottom_left.x

        if transform == "":
            # Scale based on 'aspect ratio' of font size in x and y
            transform = 'transform="translate({0} {1}) scale(1 {4}) translate({2} {3})"'.format(
                self.dp(pos.x),
                self.dp(pos.y),
                self.dp(-pos.x),
                self.dp(-pos.y),
                svg_fontsize_pts.y / svg_fontsize_pts.x)

        if (font_flags & 4) == 4:
            # Underline the text
            decoration = "underline"
            if not self.config.basic_underlines:
                decoration += " " + self.colour_name(text_header.colour)

            transform += " text-decoration='{0}'".format(decoration)

        if (font_flags & 2) == 2:
            # Reverse the text
            text = text[::-1]

        # It's unusual (since !Draw doesn't have the UI to allow it) but text objects can have multiple lines of text, see 'Metro.c56' example.
        num_lines = len(text.split('\n'))
        for line in text.split('\n'):
            # get textLength attribute
            if self.config.use_bbox and (num_lines == 1):
                text_length = ' textLength="{0}px"'.format(self.dp(text_width))
            else:
                text_length = ''

            output = '<text x="{0}" y="{1}" font-family=\'{2}\' font-size="{3}pt" font-weight="{4}" font-style="{5}"{6} fill="{7}" xml:space="preserve" {8}>{9}</text>\n'.format(
                self.dp(pos.x),
                self.dp(pos.y),
                self.findfontname(text_header.style),
                self.formatfontsize(svg_fontsize_pts, text_header.style),
                self.findfontweight(text_header.style),
                self.findfontstyle(text_header.style),
                text_length,
                self.colour_name(text_header.colour),
                transform,
                Convertor.escape(line))

            fout.write(output)
            pos.y += svg_fontsize_pixels.y
        return(text)

    # Information about a single dash.
    class DashEntry:
        def __init__(self, is_start_cap, dist):
            self.is_start_cap = is_start_cap
            self.dist = dist

        def __repr__(self):
            return "'{0},{1}'".format(self.is_start_cap, self.dist)

    def gather_simple_path_caps(self, fout, path, caps, svg_width, offset):
        output = ""
        # Calculate total path length
        total_path_length = 0
        for segment in self.path_segments:
            length = segment[0].dist(segment[1])
            total_path_length += length

        # Essentially a zero length path, so don't try to work out caps
        if total_path_length < epsilon:
            return("")

        if caps == None:
            # One dash for the full length of the path
            caps = [self.DashEntry(False, total_path_length)]

        # If there are an odd number of caps, then add one to make it have the same number of start
        # caps as end caps.
        if (len(caps) & 1) != 0:
            caps.append(self.DashEntry(True, total_path_length))

        # Calculate positions and directions for caps
        cap_info = []

        # Move through the caps based on the initial 'offset'
        cap_index = 0
        current_cap_distance = offset
        while current_cap_distance > caps[cap_index].dist:
            current_cap_distance -= caps[cap_index].dist
            cap_index = (cap_index + 1) % len(caps)

        is_start_cap = not caps[cap_index].is_start_cap
        initial_offset_is_not_a_dash_its_in_a_gap = not is_start_cap

        done = False

        while not done:
            # Variables to record the position and direction of the current cap
            cap_pos = None
            cap_dir = None

            # Find the position and direction at a distance 'current_cap_distance' along the path
            #
            # To do this we look through each straight line segment of the path, until we find the
            # correct distance from the start of the path
            #
            # (TODO: make a more efficient, incremental approach rather than starting from the
            # beginning of the path each time.)
            length_so_far = 0
            for segment in self.path_segments:
                length = segment[0].dist(segment[1])

                if current_cap_distance <= (length_so_far + length):
                    if length > epsilon:
                        # find position within this segment
                        ratio = (current_cap_distance - length_so_far) / length
                        cap_pos = segment[0].lerp(segment[1], ratio)
                        cap_dir = math.atan2(segment[1].y - segment[0].y, segment[1].x - segment[0].x)
                    else:
                        cap_pos = segment[0]
                        cap_dir = 0
                    break

                length_so_far += length

            # Store the cap_pos and cap_dir
            if not initial_offset_is_not_a_dash_its_in_a_gap:
                if cap_pos != None:
                        cap_info.append([cap_pos, cap_dir, is_start_cap, "Middle", cap_index])
                else:
                    if not is_start_cap:
                        # draw final end cap
                        cap_pos = segment[1]
                        cap_dir = math.atan2(segment[1].y - segment[0].y, segment[1].x - segment[0].x)
                        cap_info.append([cap_pos, cap_dir, False, "End", cap_index])
                    done = True
            initial_offset_is_not_a_dash_its_in_a_gap = False

            # Move current distance along the path to the position of the current cap
            current_cap_distance += caps[cap_index].dist
            is_start_cap = caps[cap_index].is_start_cap

            # Move to next cap
            cap_index = (cap_index + 1) % len(caps)

        # Caps data
        fill_caps = 'fill="{0}"'.format(self.colour_name(path.outlinecolour))
        # for triangle caps
        scale_x = svg_width * path.style.tricaplength / 16
        scale_y = svg_width * path.style.tricapwidth / 16

        for cap in cap_info:
            cap_angle   = math.degrees(cap[1])

            if cap[2]:
                # Start Cap
                #   0 = butt caps
                #   1 = round caps
                #   2 = projecting square caps
                #   3 = triangular caps
                if path.style.startcapstyle == 1:
                    # Output round start cap
                    output += '<circle id="cap{0}_start_round" {1} stroke="none" r="{2}" cx="{3}" cy="{4}" />\n'.format(
                        self.cap_count,
                        fill_caps,
                        self.dp(svg_width / 2),
                        self.dp(cap[0].x),
                        self.dp(cap[0].y))
                    self.cap_count += 1
                elif path.style.startcapstyle == 2:
                    # Output square start cap (0.02 is a small amount of overlap to avoid tiny gaps due to accuracy issues)
                    output += '<path id="cap{0}_start_square" {1} stroke="none" transform="translate({2} {3}) rotate({4}) scale({5} {6})" d="M-1 -1 L-1 1 L0.02 1 L0.02 -1 z" />\n'.format(
                        self.cap_count,
                        fill_caps,
                        self.dp(cap[0].x),
                        self.dp(cap[0].y),
                        self.dp(cap_angle),
                        self.dp(svg_width / 2),
                        self.dp(svg_width / 2))
                    self.cap_count += 1
                elif path.style.startcapstyle == 3:
                    # Output triangle start cap (0.02 is a small amount of overlap to avoid tiny gaps due to accuracy issues)
                    output += '<path id="cap{0}_start_triangle" {1} stroke="none" transform="translate({2} {3}) rotate({4}) scale({5} {6})" d="M0.02 -1 L0.02 1 L-1 0 z" />\n'.format(
                        self.cap_count,
                        fill_caps,
                        self.dp(cap[0].x),
                        self.dp(cap[0].y),
                        self.dp(cap_angle),
                        self.dp(scale_x),
                        self.dp(scale_y))
                    self.cap_count += 1
            else:
                # End Cap
                #   0 = butt caps
                #   1 = round caps
                #   2 = projecting square caps
                #   3 = triangular caps
                if path.style.endcapstyle == 1:
                    # Output round end cap
                    output += '<circle id="cap{0}_end_round" {1} stroke="none" r="{2}" cx="{3}" cy="{4}" />\n'.format(
                        self.cap_count,
                        fill_caps,
                        self.dp(svg_width / 2),
                        self.dp(cap[0].x),
                        self.dp(cap[0].y))
                    self.cap_count += 1
                elif path.style.endcapstyle == 2:
                    # Output square end cap (0.02 is a small amount of overlap to avoid tiny gaps due to accuracy issues)
                    output += '<path id="cap{0}_end_square" {1} stroke="none" transform="translate({2} {3}) rotate({4}) scale({5} {6})" d="M-0.02 -1 L-0.02 1 L1 1 L1 -1 z" />\n'.format(
                        self.cap_count,
                        fill_caps,
                        self.dp(cap[0].x),
                        self.dp(cap[0].y),
                        self.dp(cap_angle),
                        self.dp(svg_width / 2),
                        self.dp(svg_width / 2))
                    self.cap_count += 1
                elif path.style.endcapstyle == 3:
                    # Output triangle end cap (0.02 is a small amount of overlap to avoid tiny gaps due to accuracy issues)
                    output += '<path id="cap{0}_end_triangle" {1} stroke="none" transform="translate({2} {3}) rotate({4}) scale({5} {6})" d="M-0.02 -1 L1 0 L-0.02 1 z" />\n'.format(
                        self.cap_count,
                        fill_caps,
                        self.dp(cap[0].x),
                        self.dp(cap[0].y),
                        self.dp(cap_angle),
                        self.dp(scale_x),
                        self.dp(scale_y))
                    self.cap_count += 1
        return(output)

    def get_cap_desc(capstyle):
        capdescs = { 0: "0 (butt caps)",
                     1: "1 (round caps)",
                     2: "2 (square caps)",
                     3: "3 (triangular caps)" }
        if capstyle in capdescs:
            return capdescs[capstyle]
        return "{0} (unknown)".format(capstyle)

    def read_path_object(self, fin, fout, object_header):
        path = Convertor.PathHeader()
        path.read(fin)
        message(2, "  Path Object: {7}\n   Fill: ({0} {1} {2})\n   Outline: colour ({3} {4} {5}) width {6}".format(
            path.fillcolour.red,    path.fillcolour.green,    path.fillcolour.blue,
            path.outlinecolour.red, path.outlinecolour.green, path.outlinecolour.blue,
            path.outlinewidth, self.path_count))
        message(2, "   Style:\n    Join: {0}\n    Startcap: {1}\n    Endcap: {2}".format(
            path.style.joinstyle,
            Convertor.get_cap_desc(path.style.startcapstyle),
            Convertor.get_cap_desc(path.style.endcapstyle)))
        message(2, "    Winding: {0}\n    Dash: {1}\n    Tri cap width: {2}\n    Tri cap length: {3}".format(
            path.style.winding, path.style.dash,
            path.style.tricapwidth, path.style.tricaplength))

        if path.fillcolour.reserved == 0xff:
            fill = 'fill="none"'
        else:
            fill = 'fill="{0}"'.format(self.colour_name(path.fillcolour))

        stroke = 'stroke="{0}"'.format(self.colour_name(path.outlinecolour))
        if path.outlinecolour.reserved == 0xff:
            stroke += ' stroke-opacity="0"'

        if path.outlinewidth==0:
            # Thinnest lines = one pixel
            svg_width = 1
        else:
            svg_width = self.cc.draw_to_svg_width(path.outlinewidth)


        # Handle dash array
        dash_array_string = ""
        offset = 0
        if path.style.dash:
            # Read dasharray
            offset = Convertor.read_int(fin)
            offset = self.cc.draw_to_svg_width(offset)
            dash_count = Convertor.read_uint(fin)

            if offset > 0:
                dash_array_string += 'stroke-dashoffset="{0}" '.format(self.dp(offset))

            dash_array_string += 'style="stroke-dasharray:'

            # Start the first dash at distance zero
            is_start_cap = True
            caps = []
            for i in range(dash_count):
                dash_offset = Convertor.read_uint(fin)
                dash_offset = self.cc.draw_to_svg_width(dash_offset)

                is_start_cap = not is_start_cap
                caps.append(self.DashEntry(is_start_cap, dash_offset))
                dash_array_string += ' {0}'.format(self.dp(dash_offset))
            dash_array_string += '"'
        else:
            # Do this later when we know the length of the path
            caps = None

        # Group together lines with caps, or path segments
        if (path.style.startcapstyle != 0) or (path.style.endcapstyle != 0):
            started_group = True
            fout.write('<g id="draw_path{0}">\n'.format(self.path_count))
            self.path_count += 1
        else:
            started_group = False
            fill = 'id="draw_path{0}" '.format(self.path_count) + fill
            self.path_count += 1

        # Output multiple <paths>, each separated by a 'move' command.
        # The dash offset is reset between these path segments.
        path_header = '<path {0} fill-rule="{1}" {2} stroke-width="{3}" stroke-linejoin="{4}" {5} d="'.format(
            fill,
            "nonzero" if (path.style.winding==0) else "evenodd",
            stroke,
            self.dp(svg_width),
            "miter" if (path.style.joinstyle==0) else "round" if (path.style.joinstyle==1) else "bevel",
            dash_array_string)

        # Output path(s)
        # Converts the path into straight line segments
        fout.write(path_header)

        self.points = []        # Remember points, useful for adding caps afterwards
        self.path_segments = [] # Straight line segments approximating the path
        old_status = ""
        caps_output = ""
        while True:
            status = self.read_path_components(fin)
            if ((status == "Moved") and (old_status != "")) or (status == "Finished"):
                if status == "Moved":
                    move = self.points[-1]
                else:
                    move = None

                self.write_path_components(fout)
                #fout.write('" />\n')  # End previous path

                # Output caps for path
                caps_output += self.gather_simple_path_caps(fout, path, caps, svg_width, offset)
                if move != None:
                    self.points = [move]               # Last 'Move to' point remembered as start of next simple path
                self.path_segments = []                # Straight line segments approximating the path

                if status == "Moved":
                    # Start next simple path
                    #fout.write(path_header)
                    old_status = ""

            if status == "Finished":
                break
            old_status = status

        fout.write('" />\n')  # End previous path
        if caps_output != "":
            fout.write(caps_output)
        if started_group:
            fout.write('</g>\n')


    def write_path_components(self, fout):
        newline_string = ""
        for point in self.points:
            svg_point = point[1]
            if point[0] == "Move":
                fout.write("{0}M{1} {2}".format(newline_string, self.dp(svg_point.x), self.dp(svg_point.y)))
            elif point[0] == "Draw":
                fout.write("{0}L{1} {2}".format(newline_string, self.dp(svg_point.x), self.dp(svg_point.y)))
            elif point[0] == "Bezier1":
                fout.write("{0}C{1} {2} ".format(newline_string, self.dp(svg_point.x), self.dp(svg_point.y)))
            elif point[0] == "Bezier2":
                fout.write("{0} {1} ".format(self.dp(svg_point.x), self.dp(svg_point.y)))
            elif point[0] == "Bezier3":
                fout.write("{0} {1}".format(self.dp(svg_point.x), self.dp(svg_point.y)))
            elif point[0] == "Close":
                fout.write("{0}Z".format(newline_string))
            newline_string = "\n"


    def read_path_components(self, fin):
        end = 0
        tag = Convertor.read_int(fin)
        tag &= 0x7f
        point = Convertor.Coords()

        if tag == Convertor.PATH_END:
            return "Finished"
        elif tag == Convertor.PATH_MOVE:
            point.read(fin)
            svg_point = self.cc.draw_to_svg_point(point)
            self.points.append(["Move", svg_point])
            t = "     MOVE {0},{1}".format(self.dp(svg_point.x), self.dp(svg_point.y))
            message(2, t)
            return "Moved"
        elif tag == Convertor.PATH_CLOSE_SUB:
            self.points.append(["Close", None])
            return "Closed"
        elif tag == Convertor.PATH_DRAW:
            point.read(fin)
            svg_point = self.cc.draw_to_svg_point(point)
            self.points.append(["Draw", svg_point])
            self.path_segments.append([self.points[-2][1], self.points[-1][1]])
            message(2, "     DRAW {0},{1}".format(self.dp(svg_point.x), self.dp(svg_point.y)))
        elif tag == Convertor.PATH_BEZIER:
            point.read(fin)
            svg_point = self.cc.draw_to_svg_point(point)
            self.points.append(["Bezier1", svg_point])
            message(2, "     BEZIER {0},{1},".format(self.dp(svg_point.x), self.dp(svg_point.y)), end="")
            point.read(fin)
            svg_point = self.cc.draw_to_svg_point(point)
            self.points.append(["Bezier2", svg_point])
            message(2, "{0},{1},".format(self.dp(svg_point.x), self.dp(svg_point.y)), end="")
            point.read(fin)
            svg_point = self.cc.draw_to_svg_point(point)
            self.points.append(["Bezier3", svg_point])
            message(2, "{0},{1}".format(self.dp(svg_point.x), self.dp(svg_point.y)))

            # Split the bezier curve into this number of straight line segments
            num_segments = 50

            # This bezier curve
            a = self.points[-4][1]
            b = self.points[-3][1]
            c = self.points[-2][1]
            d = self.points[-1][1]

            old_point = bezier(a,b,c,d,0)
            for t in range(1, num_segments + 1):
                new_point = bezier(a,b,c,d,t/num_segments)
                self.path_segments.append([old_point, new_point])
                old_point = new_point

        return "In Progress"

    def read_group_object(self, fin, fout, object_header):
        groupname = Convertor.read_name_string(fin, 12).strip()
        message(2, '  Group Name: {0}'.format(groupname))
        if len(groupname) > 0:
            fout.write('<g id="{0}">\n'.format(Convertor.escape(groupname)))
        else:
            fout.write('<g>\n')

        self.read_objects(fin, fout, object_header.obj_length - Convertor.ObjectHeader.size() - 12)
        message(2, '  End of group \'{0}\''.format(groupname))
        fout.write('</g>\n')

    def read_tagged_object(self, fin, fout, object_header):
        # Read and ignore the tag identifier
        Convertor.read_uint()

        # Read one object. This could be a group object to allow more rendering.
        self.read_objects(fin, fout, 0)

        # Ignore any additional word-aligned data remaining in this object.

    class SpriteInfo:
        def __init__(self, sprite_ctrl_block):
            # Offset to mask if present
            self.maskbits   = None
            if sprite_ctrl_block.image != sprite_ctrl_block.mask:
                self.maskbits = sprite_ctrl_block.mask - Convertor.SpriteCtrlBlock.size()

            # get stride in bytes, height in pixels
            self.stride = (sprite_ctrl_block.width + 1) * 4
            self.height = sprite_ctrl_block.height + 1

            # See https://www.riscosopen.org/wiki/documentation/show/Sprite%20Mode%20Word

            # Old (pre-RISC OS 3.5 format) sprite, with a simple MODE number
            self.old_format_sprite = sprite_ctrl_block.mode < 256

            # For newer sprites (RISC OS 3.5 and later) a wide mask has 8bpp and acts like an alpha
            # channel, otherwise it's one bit
            self.wide_mask         = (sprite_ctrl_block.mode & 0x80000000) != 0

            self.colour_format = None
            sprite_mode_word = sprite_ctrl_block.mode
            self.xf = 1
            self.yf = 1
            self.dpi_x = None
            self.dpi_y = None

            # Old style sprites (Pre RISC-OS 3.5) just have a MODE number < 256
            if self.old_format_sprite:
                # MODE number
                if sprite_ctrl_block.mode in Convertor.modes:
                    self.bpp = Convertor.modes[sprite_ctrl_block.mode].bpp
                    self.yf = Convertor.modes[sprite_ctrl_block.mode].yf
                    self.xf = Convertor.modes[sprite_ctrl_block.mode].xf
                    self.colour_format = "P"

                    if self.bpp == 0:
                        error("   Mode {0} is a non-graphical mode, this is weird.".format(sprite_ctrl_block.mode))
                        raise ValueError('Bad sprite. Non-graphical MODE found, which is not supported.')
                else:
                    error("   Mode {0} doesn't have a definition. Looks like a user defined mode. This is weird.".format(sprite_ctrl_block.mode))
                    raise ValueError('Bad sprite. User defined MODE found, which is not supported.')
            elif (sprite_mode_word & 1) == 0:
                error("   Mode 0x{0:02x} is an offset to a MODE selector block. That's not supposed to be valid for a sprite, this is weird.".format(sprite_ctrl_block.mode))
                raise ValueError('Bad sprite. Unexpectedly found an offset to a selector block, which is not supported.')
            elif (sprite_mode_word & 0x78000000) == 0x78000000:
                # RISC OS 5 format
                dpi_lookup = [180, 90, 45, 23]
                self.dpi_x = dpi_lookup[(sprite_mode_word >> 4) & 3]
                self.dpi_y = dpi_lookup[(sprite_mode_word >> 6) & 3]
                mode_flags = (sprite_mode_word >> 8) & 0xff
                sprite_type = (sprite_mode_word >> 20) & 0x7f

                c = mode_flags >> 4
                if c == 0:
                    self.colour_format = "TBGR"
                elif c == 1:
                    self.colour_format = "KYMC"
                elif c == 2:
                    self.colour_format = "YCbCr"     # ITU-R BT.601, full range. JPEG (JFIF)
                elif c == 4:
                    self.colour_format = "TRGB"
                elif c == 6:
                    self.colour_format = "YCbCr"     # ITU-R BT.601, video range
                elif c == 8:
                    self.colour_format = "TRGB"
                elif c == 10:
                    self.colour_format = "YCbCr"     # ITU-R BT.709, full range
                elif c == 12:
                    self.colour_format = "ARGB"
                elif c == 14:
                    self.colour_format = "YCbCr"     # ITU-R BT.709, video range
                else:
                    error("    Unsupported mode flags ({0})".format(mode_flags))
                    raise ValueError('Bad sprite. Unsupported mode flags ({0})'.format(mode_flags))
            else:
                # RISC OS 3.5 format
                self.dpi_x = (sprite_mode_word >> 1) & 0x1fff
                self.dpi_y = (sprite_mode_word >> 14) & 0x1fff
                sprite_type = (sprite_mode_word >> 27) & 0x0f

                # HACK: According to the docs, sprite type 6 should have transparency, but it
                # doesn't seem to be reliable (some files have 0 opaque, some have 255) so we
                # just ignore the channel and assume opaque.
                if sprite_type == 6:
                    self.colour_format = "XBGR"

            # WARNING: Following the documentation in PRMs, we set the ncolour and log2bpp variables
            # with strict meanings that don't always adhere to the values you might commonly expect
            # variables with these names to have.
            self.ncolour = None
            self.log2bpp = None
            if not self.old_format_sprite:
                # Based on sprite type, work out bpp, colour_format, ncolour
                if sprite_type == 1:
                    self.bpp = 1
                    self.log2bpp = 0
                    self.ncolour = 1
                    if self.colour_format == None:
                        self.colour_format = "P"
                elif sprite_type == 2:
                    self.bpp = 2
                    self.log2bpp = 1
                    self.ncolour = 3
                    if self.colour_format == None:
                        self.colour_format = "P"
                elif sprite_type == 3:
                    self.bpp = 4
                    self.log2bpp = 2
                    self.ncolour = 15
                    if self.colour_format == None:
                        self.colour_format = "P"
                elif sprite_type == 4:
                    self.bpp = 8
                    self.log2bpp = 3
                    self.ncolour = 63
                    if self.colour_format == None:
                        self.colour_format = "P"
                elif sprite_type == 5:
                    self.bpp = 16
                    self.log2bpp = 4
                    self.ncolour = 65535
                    if self.colour_format == None:
                        self.colour_format = "TBGR"
                    self.colour_format += " 1:5:5:5"
                elif sprite_type == 6:
                    self.bpp = 32
                    self.log2bpp = 5
                    self.ncolour = -1
                    if self.colour_format == None:
                        self.colour_format = "TBGR"
                elif sprite_type == 7:
                    self.bpp = 32
                    self.log2bpp = 5
                    self.ncolour = -1
                    if self.colour_format == None:
                        self.colour_format = "CMYK"
                elif sprite_type == 8:
                    self.bpp = 24
                    self.log2bpp = 6
                    self.ncolour = 16777215
                    if self.colour_format == None:
                        self.colour_format = "BGR"
                elif sprite_type == 9:
                    self.bpp = 24
                    self.log2bpp = None
                    self.ncolour = None
                    if self.colour_format == None:
                        self.colour_format = "YCbCr"
                elif sprite_type == 10:
                    self.bpp = 16
                    self.log2bpp = 4
                    self.ncolour = 65535
                    if self.colour_format == None:
                        self.colour_format = "BGR"
                    self.colour_format += " 5:6:5"
                elif sprite_type == 16:
                    self.bpp = 16
                    self.log2bpp = 4
                    self.ncolour = 4095
                    if self.colour_format == None:
                        self.colour_format = "ABGR"
                    self.colour_format += " 4:4:4:4"
                elif sprite_type == 17:
                    self.bpp = 24
                    self.log2bpp = 7
                    self.ncolour = 420
                    if self.colour_format == None:
                        self.colour_format = "YCbCr"
                elif sprite_type == 18:
                    self.bpp = 24
                    self.log2bpp = 7
                    self.ncolour = 422
                    if self.colour_format == None:
                        self.colour_format = "YCbCr"
                else:
                    error("    Unknown RISC OS sprite type {0}, unsupported".format(sprite_type))
                    raise ValueError('Bad sprite. Unknown RISC OS sprite type {0}'.format(sprite_type))

            # 'self.width' is width in pixels
            self.width = self.stride * 8 // self.bpp
            # take off pixels at the unused left and right edges
            self.width -= (31 - sprite_ctrl_block.lastbit) // self.bpp
            self.width -= sprite_ctrl_block.firstbit // self.bpp

            # Calculate mask stride in bytes
            if self.old_format_sprite:
                # mask has same bpp as image
                self.mask_stride = self.stride
            elif self.wide_mask:
                # 8bpp mask
                self.mask_stride = self.width
            else:
                # 1bpp mask
                self.mask_stride = (self.width + 7) // 8

            # Round up to next multiple of 4 bytes
            if (self.mask_stride & 3) != 0:
                self.mask_stride += 4 - (self.mask_stride & 3)

            message(2, "  xf: {0}\n  yf: {1}\n  bpp: {2}\n  colour_format: {3}  ncolour: {4}  log2bpp: {5}  mask_stride: {6}".format(self.xf,self.yf,self.bpp,self.colour_format, self.ncolour, self.log2bpp, self.mask_stride))

        def __repr__(self):
            return "\n  stride: {0}\n width: {1}\n height: {2}\n xf: {3}\n  yf: {4}\n  bpp: {5}\n  colour_format: {6}\n  ncolour: {7}\n  log2bpp: {8}\n  mask_stride: {9}\n".format(self.stride, self.width, self.height, self.xf,self.yf,self.bpp,self.colour_format, self.ncolour, self.log2bpp, self.mask_stride)


    def parse_palette_data(self, bpp, sprite_ctrl_block, sprite_bytes):
        # Use a standard RISC OS palette by default
        if bpp == 8:
            colpal = Convertor.colpal256
        elif bpp == 4:
            colpal = Convertor.colpal16
        elif bpp == 2:
            colpal = Convertor.colpal4
        elif bpp == 1:
            colpal = Convertor.colpal2
        else:
            colpal = None

        # Override a standard palette if there is a local palette definition
        palette_size = min(sprite_ctrl_block.image, sprite_ctrl_block.mask) - Convertor.SpriteCtrlBlock.size()

        # Offset to palette
        palette = 0

        # Palettes must be a multiple of eight
        if (palette_size > 0) and ((palette_size & 7) == 0):
            colpal = []
            for i in range(0, palette_size, 8):
                colpal += [sprite_bytes[palette + i + 1],
                           sprite_bytes[palette + i + 2],
                           sprite_bytes[palette + i + 3],
                           255]

            # Fill in rest of the 256 colour palette, if palette has 16 or 64 entries
            # See http://www.riscos.com/support/developers/prm/vdu.html#74378
            palette_size //= 8       # Convert #bytes to number of palette entries
            if bpp == 8:
                if (palette_size == 16) or (palette_size == 64):
                    # Each original palette entry is used to generate variants.
                    for j in range(palette_size, 256, palette_size):
                        for i in range(0, palette_size):
                            # Calculate new colour variant from the original colour
                            red   = (((j + i) & 0x10) >> 1) | (colpal[4*i] >> 4)
                            green = (((j + i) & 0x40) >> 3) | \
                                    (((j + i) & 0x20) >> 3) | (colpal[4*i+1] >> 4)
                            blue  = (((j + i) & 0x80) >> 4) | (colpal[4*i+2] >> 4)
                            red   = (red * 255)   // 15
                            green = (green * 255) // 15
                            blue  = (blue * 255)  // 15
                            colpal += [red, green, blue, 255]
        return colpal

    def read_sprite(self, sprite_ctrl_block, sprite_bytes):

        # parse sprite info from header
        try:
            sprite_info = Convertor.SpriteInfo(sprite_ctrl_block)
        except:
            return (None, None)

        # get palette
        colpal = self.parse_palette_data(sprite_info.bpp, sprite_ctrl_block, sprite_bytes)

        ins = sprite_ctrl_block.image-Convertor.SpriteCtrlBlock.size()    # Offset into sprite to read from
        inm = sprite_info.maskbits                                        # Offset into mask to read from
        sprite_pixels = []      # Sprite pixels to write to

        if sprite_info.bpp <= 8:
            # retrieve pixels from sprite_bytes
            bitmask = (1 << sprite_info.bpp) - 1
            shift   = 0

            for row in range(sprite_info.height):
                # remember the offset at the start of the row
                tmpins = ins
                tmpinm = inm

                row_sprite_pixels_offset = len(sprite_pixels)

                # increment the offset to skip past the unused
                # strip of pixels on the left edge of the sprite
                ins += sprite_ctrl_block.firstbit>>3

                # Left hand wastage applies to masks for old sprites too
                if inm != None and sprite_info.old_format_sprite:
                    inm += sprite_ctrl_block.firstbit>>3

                # amount to shift within a sprite byte
                shift = sprite_ctrl_block.firstbit & 7

                # Loop over all pixels
                for col in range(sprite_info.width):
                    pixel = sprite_bytes[ins]
                    mask = 255
                    if sprite_info.maskbits != None:
                        mask = sprite_bytes[inm]
                        # See Mask data section of https://www.riscosopen.org/wiki/documentation/show/Format%20Of%20Sprite
                        if sprite_info.old_format_sprite:
                            # Old format sprite. Mask is same bpp as image,
                            # 0 = invisible, anything else is opaque.
                            mask >>= shift
                            mask &= bitmask
                            if mask != 0:
                                mask = 255
                        elif sprite_info.wide_mask:
                            # 8bpp mask (nothing more to do here)
                            pass
                        else:
                            # 1bpp mask
                            mask &= 1 << (col & 7)

                    pixel >>= shift
                    pixel &= bitmask

                    if mask == 0:
                        # Masked values are set to transparent
                        sprite_pixels.append(0)
                        sprite_pixels.append(0)
                        sprite_pixels.append(0)
                        sprite_pixels.append(0)
                    else:
                        sprite_pixels.append(colpal[pixel * 4])
                        sprite_pixels.append(colpal[pixel * 4 + 1])
                        sprite_pixels.append(colpal[pixel * 4 + 2])
                        sprite_pixels.append(colpal[pixel * 4 + 3])

                    # Copy the pixels based on the x-repetition
                    for r in range(sprite_info.xf - 1):
                        sprite_pixels.append(sprite_pixels[-4])
                        sprite_pixels.append(sprite_pixels[-4])
                        sprite_pixels.append(sprite_pixels[-4])
                        sprite_pixels.append(sprite_pixels[-4])

                    shift += sprite_info.bpp

                    # move to next byte
                    if shift > 7:
                        if inm != None and sprite_info.old_format_sprite:
                            # mask bpp same as image
                            inm += 1
                        ins += 1
                        shift = 0

                    if inm != None and not sprite_info.old_format_sprite:
                        # 1 bpp mask
                        if (col & 7) == 7:
                            inm += 1

                # Repeat rows if needed based on 'sprite_info.yf'
                current_offset = len(sprite_pixels)
                row_of_pixels = sprite_pixels[row_sprite_pixels_offset:current_offset]
                for r in range(sprite_info.yf-1):
                    sprite_pixels.extend(row_of_pixels)

                # move to next row
                ins = tmpins + sprite_info.stride

                if inm != None:
                    inm = tmpinm + sprite_info.mask_stride

            # finish up
            firstbit = 0
            sprite_pixels = bytes(sprite_pixels)
        else:
            # 16,24 or 32 bit image
            if sprite_info.bpp == 16:
                bits_per_channel = [int(x) for x in sprite_info.colour_format.split(' ')[1].split(':')]
            else:
                bits_per_channel = [8,8,8,8]

            colour_format = sprite_info.colour_format.split(' ')[0]

            i = 0
            for row in range(sprite_info.height):
                tmpins = ins
                tmpinm = inm

                # increment the offset to skip past the unused
                # strip of pixels on the left edge of the sprite
                ins += sprite_ctrl_block.firstbit>>3
                if inm != None:
                    inm += sprite_ctrl_block.firstbit>>3

                # amount to shift within a sprite byte
                shift = sprite_ctrl_block.firstbit & 7
                shift_mask = 0

                # Pixel to output in RGBA or CMYK format
                out = [0,0,0,0]

                # Loop over all pixels in the row
                for col in range(sprite_info.width):

                    # Read the byte(s) containing the first channel
                    assert ins < len(sprite_bytes), "len(sprite_bytes): {0} ins: {1}".format(len(sprite_bytes), ins)
                    word = sprite_bytes[ins]
                    # Make sure we don't read beyond the end of the image
                    if len(sprite_bytes) > (ins+1):
                        word += 256*sprite_bytes[ins+1]

                    # Loop over each channel
                    channel_index = -1
                    for c in reversed(colour_format):
                        # How many bits are in the current channel?
                        channel_bits = bits_per_channel[channel_index]

                        # Make a mask for these bits
                        bitmask = (1 << channel_bits) - 1

                        channel_value = (word >> shift) & bitmask

                        # Read channel value and 'normalise' it to the range [0,255]
                        if c == 'R':
                            out[0] = channel_value * 255 // bitmask
                        elif c == 'G':
                            out[1] = channel_value * 255 // bitmask
                        elif c == 'B':
                            out[2] = channel_value * 255 // bitmask
                        elif c == 'T':
                            out[3] = (bitmask-channel_value) * 255 // bitmask
                        elif c == 'X':
                            out[3] = 255
                        elif c == 'A':
                            out[3] = channel_value * 255 // bitmask
                        elif c == 'C':
                            out[0] = channel_value * 255 // bitmask
                        elif c == 'Y':
                            out[1] = channel_value * 255 // bitmask
                        elif c == 'M':
                            out[2] = channel_value * 255 // bitmask
                        elif c == 'K':
                            out[3] = channel_value * 255 // bitmask
                        else:
                            error("Unsupported colour format of {0}".format(sprite_info.colour_format))
                            exit(1)

                        # Move to the next channel
                        shift += channel_bits
                        if shift >= 8:
                            shift -= 8
                            ins += 1

                            # Read the next colour channel of the pixel.
                            # Read two bytes since a channel can spill between two bytes.
                            # (But don't read if we are at the end of the image)
                            if ins < len(sprite_bytes):
                                word = sprite_bytes[ins]
                            else:
                                word = 0

                            # Make sure we don't read beyond the end of the image
                            if (ins+1) < len(sprite_bytes):
                                word += 256*sprite_bytes[ins+1]

                        channel_index -= 1

                    # Apply mask to alpha channel
                    if sprite_info.maskbits != None:
                        if sprite_info.wide_mask:
                            # Each mask value is 8 bits of alpha
                            out[3] = sprite_bytes[inm]
                            inm+=1
                        else:
                            # Each mask value is 1 bit
                            if (sprite_bytes[inm] & (1<<shift_mask)) != 0:
                                out[3] = 255
                            else:
                                out[3] = 0

                            # Move to next mask bit
                            shift_mask += 1
                            if shift_mask == 8:
                                inm += 1
                                shift_mask = 0

                    # 'out' is in RGBA or CMYK order
                    sprite_pixels.append(out[0])
                    sprite_pixels.append(out[1])
                    sprite_pixels.append(out[2])
                    sprite_pixels.append(out[3])

                i += 1

                # move to next row
                ins = tmpins + sprite_info.stride
                if inm != None:
                    inm = tmpinm + sprite_info.mask_stride

            # finish up
            firstbit = 0
            sprite_pixels = bytes(sprite_pixels)

        byte_count_in_theory = sprite_info.width * sprite_info.xf * sprite_info.height * sprite_info.yf * sprite_info.bpp // 8
        if len(sprite_pixels) < byte_count_in_theory:
            error("incorrect number of pixels in image data")
            message(0, "width * height * xf * yf * bpp/8={0}".format(byte_count_in_theory))
            message(0, "len(sprite_pixels)={0}".format(len(sprite_pixels)))
            return (None, None)

        # Make PNG data
        # mode 'P' means 8 bit with colour palette
        png_colour_format = sprite_info.colour_format.split(' ')[0]
        if png_colour_format != "CMYK" and png_colour_format != "KYMC" and png_colour_format != 'YCbCr':
            png_colour_format = "RGBA"

        im = Image.frombytes(png_colour_format, (sprite_info.width * sprite_info.xf, sprite_info.height * sprite_info.yf), sprite_pixels, decoder_name='raw')
        #if colpal:
        #    im.putpalette(colpal, rawmode='RGBA')

        # DEBUG: Save PNGs to files on disk
        #global debug
        #im.save("temp{0}.png".format(debug), "png")
        #debug += 1

        # Return PNG data
        byteIO = io.BytesIO()
        im.save(byteIO, format='PNG')       # DEBUG: 'Save' PNG to byte array
        byteArr = byteIO.getvalue()

        return (byteArr, sprite_info)

    def read_sprite_object(self, fin, fout, object_header):
        matrix = Convertor.DrawMatrix()
        length = object_header.obj_length
        transform = ""

        if object_header.obj_type == Convertor.OBJECT_TRANSSPRITE:
            length -= Convertor.DrawMatrix.size()
            matrix.read(fin)
            matrix = self.cc.draw_to_svg_matrix(matrix)

            message(2, "  Transformed Sprite Object:")
            message(2, "    Draw Matrix:")
            message(2, "{0}".format(matrix))
        else:
            matrix = self.cc.draw_to_svg_matrix(matrix)
            message(2, "  Sprite Object:")

        sprite_ctrl_block = Convertor.SpriteCtrlBlock()
        sprite_ctrl_block.read(fin)
        length -= Convertor.SpriteCtrlBlock.size()

        message(2, "  Sprite Control Block:");
        # Draw only saves one sprite in each chunk
        message(2, "   Name:      {0}".format(sprite_ctrl_block.name))
        message(2, "   Width:     {0}+1 words".format(sprite_ctrl_block.width))
        message(2, "   Height:    {0}+1".format(sprite_ctrl_block.height))
        message(2, "   First bit: {0}".format(sprite_ctrl_block.firstbit))
        message(2, "   Last bit:  {0}".format(sprite_ctrl_block.lastbit))
        binary = format(sprite_ctrl_block.mode, '032b')
        binary = " ".join(binary[i:i + 4] for i in range(0, len(binary), 4))
        message(2, "   Mode:      {0} = {1}".format(hex(sprite_ctrl_block.mode), binary))
        message(2, "   Image:     {0}".format(hex(sprite_ctrl_block.image)))
        message(2, "   Mask:      {0}".format(hex(sprite_ctrl_block.mask)))
        message(2, "   Transformation: {0}".format(transform))

        # Read 'length' bytes of sprite data, parse it and store it as an embedded PNG? image
        sprite_bytes = fin.read(length)
        png_data, sprite_info = self.read_sprite(sprite_ctrl_block, sprite_bytes)
        if png_data == None:
            exit(1)

        width = sprite_info.width * sprite_info.xf
        height = sprite_info.height * sprite_info.yf

        # Get transform
        if object_header.obj_type == Convertor.OBJECT_TRANSSPRITE:
            transform = self.get_sprite_transform(matrix, object_header)

            # Apply DPI setting.
            # Newer RISC OS sprites have a DPI specified, which affects the size of the sprite
            # when rendered on screen.
            if sprite_info.dpi_x:
                scale_x = 96 / sprite_info.dpi_x
            else:
                scale_x = 96 / 90

            if sprite_info.dpi_y:
                scale_y = 96 / sprite_info.dpi_y
            else:
                scale_y = 96 / 90

            transform += " scale({0} {1}) translate(0,{2})".format(
                self.dp(scale_x),
                self.dp(scale_y),
                self.dp(-height))
        else:
            # The bounding box of an object in Draw specifies the bottom left and top right points
            # on the page for that object. This description remains true when converted to SVG
            # coordinates.
            # Note: The terms 'low' and 'high' are not so useful terms once converted.
            bottom_left = self.cc.draw_to_svg_point(object_header.low)
            top_right   = self.cc.draw_to_svg_point(object_header.high)

            # The sprite position is the top left corner of the sprite
            pos = Point(bottom_left.x, top_right.y)

            transform=" translate({0} {1}) scale({2} {3})".format(
                self.dp(pos.x),
                self.dp(pos.y),
                self.dp((top_right.x - bottom_left.x) / width),
                self.dp((bottom_left.y - top_right.y) / height))

        # Output PNG data in base64
        base64_data = base64.b64encode(png_data).decode('ascii')
        fout.write('<image width="{0}" height="{1}" image-rendering="pixelated" transform="{2}" '.format(
            self.dp(width),
            self.dp(height),
            transform))
        fout.write('xlink:href="data:image/png;base64,')
        fout.write(base64_data)
        fout.write('" />\n')

    def read_jpeg_object(self, fin, fout, object_header):
        jpeg_header = Convertor.JpegHeader()
        jpeg_header.read(fin)

        # Convert from Draw matrix to SVG matrix
        matrix = self.cc.draw_to_svg_matrix(jpeg_header.transform)

        message(2, "  Transformed JPEG Object:")
        message(2, "    Draw Matrix:")
        message(2, "{0}".format(matrix))

        transform = self.get_sprite_transform(matrix, object_header)

        jpeg_data = fin.read(jpeg_header.length)
        base64_data = base64.b64encode(jpeg_data).decode('ascii')
        fout.write("<image");

        # Note that the dimensions for JPEG objects are different to those for Sprite objects.
        # The width and height of the image is specified in the JPEGHeader, in Draw units.
        # For a Sprite, the width and height are just taken from the object bounding box.

        wh = self.cc.draw_to_svg_size(Convertor.Coords(jpeg_header.width, jpeg_header.height))
        trans = Point(0,-wh.y)

        fout.write(' x="{0}" y="{1}" width="{2}" height="{3}" transform="{4}"'.format(
            self.dp(trans.x), self.dp(trans.y), self.dp(wh.x), self.dp(wh.y), transform))
        fout.write(' xlink:href="data:image/jpg;base64,')
        fout.write(base64_data)
        fout.write('"/>\n')

    class TextState:
        def __init__(self, font_replacements):
            self.text_area_fonts      = {}
            self.text_area_fonts[0]   = Convertor.FontDesc("system", 24, 24, font_replacements)
            self.line_spacing_px      = CoordinateConversion.pt_to_px(10)
            self.paragraph_spacing_px = CoordinateConversion.pt_to_px(10)
            self.alignment            = "L"
            self.num_columns          = 1
            self.font_index           = 0
            self.left_margin_px       = CoordinateConversion.pt_to_px(1)
            self.right_margin_px      = CoordinateConversion.pt_to_px(1)
            self.text_colour          = Convertor.ColourType()
            self.underline_pos        = 0
            self.underline_thickness  = 0
            self.vertical_move_px     = 0
            self.ignore_full_justification = False
            self.prefix_para_breaks   = 0
            self.prefix_line_breaks   = 0
            self.plain_text           = bytearray()

        def create_font(self, font_desc):
            # Fallback to Times New Roman if nothing else works
            name = font_desc.name + 'TimesNewRoman,"Times New Roman",Times,Times-Roman,Baskerville,Georgia,serif'
            for fname in name.split(","):
                fname = fname.strip().strip('"')

                # Make a list of the possible names of the font based on bold/italic
                # TODO: Is there a better way of finding a font weight/style than just assuming it
                #       has 'Bold' or 'Italic' appended to the name?
                try_fnames = [fname]
                if font_desc.weight == "bold":
                    try_fnames = [fname + " Bold"] + try_fnames
                elif font_desc.weight == "italic":
                    try_fnames = [fname + " Italic"] + try_fnames

                for try_fname in try_fnames:
                    try:
                        font_height_pixels = CoordinateConversion.pt_to_px(font_desc.height_pts)
                        font = ImageFont.truetype(try_fname, font_height_pixels)

                        # Variable fonts
                        if (font != None) and try_fname == fname:
                            try:
                                if font_desc.weight == "bold" and b'Bold' in font.get_variation_names():
                                    font.set_variation_by_name('Bold')
                                if font_desc.weight == "italic" and b'Italic' in font.get_variation_names():
                                    font.set_variation_by_name('Italic')
                            except:
                                continue
                        return font
                    except:
                        continue
            return None

        def to_utf8(self, config):
            if config.utf8:
                return self.plain_text.decode('utf-8')
            else:
                # Convert bytes to UTF-8, based on the current font
                font_desc = self.text_area_fonts[self.font_index]
                font_name = font_desc.originalname.lower()

                return Convertor.decode_bytes_to_utf8(self.plain_text, font_name, font_desc.alphabet)

        def measure(self):
            font_desc = self.text_area_fonts[self.font_index]

            if not font_desc.font:
                font_desc.font = self.create_font(font_desc)
            self.length = font_desc.font.getlength(self.plain_text) * font_desc.width_pts / font_desc.height_pts
            assert(self.length != None)
            #self.bbox = font_desc.font.getbbox(self.plain_text)


        def message(self, verbose_level):
            message(verbose_level, "    PLAIN TEXT   : {0}".format(self.plain_text))
            message(verbose_level, "    #LINE BREAKS : {0}".format(self.prefix_line_breaks))
            message(verbose_level, "    #PARA BREAKS : {0}".format(self.prefix_para_breaks))
            message(verbose_level, "    LINE SPACING : {0}".format(self.line_spacing_px))
            message(verbose_level, "    PARA SPACING : {0}".format(self.paragraph_spacing_px))
            message(verbose_level, "    ALIGNMENT    : {0}".format(self.alignment))
            message(verbose_level, "    NUM COLUMNS  : {0}".format(self.num_columns))
            message(verbose_level, "    FONT INDEX   : {0}".format(self.font_index))
            message(verbose_level, "    LEFT MARGIN  : {0}".format(self.left_margin_px))
            message(verbose_level, "    RIGHT MARGIN : {0}".format(self.right_margin_px))
            message(verbose_level, "    TEXT COLOUR  : {0}".format(self.text_colour))
            message(verbose_level, "    UNDERLINE POS: {0}".format(self.underline_pos))
            message(verbose_level, "    UNDERLINE THK: {0}".format(self.underline_thickness))
            message(verbose_level, "    VERTICAL MOVE: {0}".format(self.vertical_move_px))
            message(verbose_level, "    IGNORE FULL J: {0}".format(self.ignore_full_justification))
            message(verbose_level, "    #FONTS DFINED: {0}".format(len(self.text_area_fonts)))
            message(verbose_level, "    MEASURELENGTH: {0}".format(self.length))

    class TextRun:
        def __init__(self, text_state):
            self.text_state = copy.copy(text_state)

        def measure(self):
            self.text_state.measure()

        def __repr__(self):
            return('"' + self.text_state.plain_text + '"')

        def message(self, verbose_level):
            message(verbose_level, "TEXT RUN:")
            self.text_state.message(verbose_level)

    def store_text_run(self, text_state):
        if text_state.plain_text != b"":
            self.text_runs.append(Convertor.TextRun(text_state))
            text_state.plain_text = bytearray()
            text_state.prefix_para_breaks = 0
            text_state.prefix_line_breaks = 0

    # Optional forward slash pattern
    OPTIONAL_TERM = br"\/?"

    # All patterns to test
    patterns = { # Terminates with forward-slash or newline
                 br'\\! *\d+[\/ \n]':                                                    "version",
                 br'^\\B *(\d+)[ \t]+(\d+)[ \t]+(\d+)[ \t]*[\/\n]':                      "background",
                 br'^\\C *(\d+)[ \t]+(\d+)[ \t]+(\d+)[ \t]*[\/\n]':                      "colour",
                 br'^\\D *(\d+)[\/ \n]':                                                 "columns",
                 br'^\\F[ \t]*(\d+)[ \t]*([^ \t]*)[ \t]*(\d+)[ \t]*[\/\n]':              "font size",
                 br'^\\F[ \t]*(\d+)[ \t]*([^ \t]*)[ \t]*(\d+)[ \t]*(\d+)[ \t]*[\/\n]':   "font size width",
                 br'^\\L *(-?\d+)[\/\n]':                                                "line leading",
                 br'^\\M *(\d+) +(\d+)[\/\n]':                                           "margins",
                 br'^\\P *(-?\d+)[\/\n]':                                                "paragraph leading",
                 br'^\\U *(-?\d+) +(-?\d+) *[\/\n]':                                     "underline",

                 # Optional forward slash terminator
                 br'^\\A(.)'+OPTIONAL_TERM:                                              "alignment",
                 br'^\\U\.'+OPTIONAL_TERM:                                               "underline end",
                 br'^\\V(-?\d+)'+OPTIONAL_TERM:                                          "vertical move",
                 br'^\\-'+OPTIONAL_TERM:                                                 "soft hyphen",
                 br'^\\\n'+OPTIONAL_TERM:                                                "line break",
                 br'^\\\\'+OPTIONAL_TERM:                                                "slash",
                 br'^\\(\d+)'+OPTIONAL_TERM:                                             "setfont",

                 # Must end with a newline
                 br'^\\;(.*)?\n':                                                        "comment",
               }

    def parse_text_area_text(self, text_bytes, text_columns, fout):
        """Parse the text from the Draw file text area including escape sequences to create a list
           of TextRun objects, each holding a run of text in a given font/style"""

        # Look through the text and handle escape sequences

        # "1. control characters are deleted, except for tab, which is replaced by a space."
        # "2. All other characters are copied, except '\', which is interpreted according to the
        #     next character, and newline (see below)"
        remaining_text_bytes = bytearray(b'')
        for c in text_bytes:
            if c == 9:
                c = 32
            elif (c < 32) and (c != 10):
                continue
            remaining_text_bytes.append(c)

        # Initialise to default state
        text_state = Convertor.TextState(self.font_replacements)              # Current state
        text_state.num_columns = len(text_columns)
        self.text_runs = []
        no_text_output_yet = True
        beginning_of_paragraph = True
        previous_byte = b""

        while len(remaining_text_bytes)>0:

            offset = 1
            for p in Convertor.patterns.items():
                matched = re.match(p[0], remaining_text_bytes)
                if matched:
                    offset = len(matched.group(0))

                    # First check for commands that won't break a text run
                    if p[1] == "slash":
                        text_state.plain_text += b"\\"
                        previous_byte = b"\\"
                        no_text_output_yet = False
                        beginning_of_paragraph = False
                    elif p[1] == "comment":
                        message(2, "Comment: {0}".format(matched.group(1)))
                    elif p[1] == "soft hyphen":
                        message(2, "Soft Hyphen")
                        text_state.plain_text += b'\xad'
                        previous_byte = '\u00ad'
                    else:
                        # Found a command that breaks a run. First finish the previous text run (if any).
                        self.store_text_run(text_state)

                        if p[1] == "version":
                            # Nothing to do here
                            pass
                        elif p[1] == "line break":
                            message(2, "Line break")
                            text_state.prefix_line_breaks += 1
                            beginning_of_paragraph = True
                            previous_byte = 10 #b'\n'
                            message(2, "add one line break. line breaks={0}".format(text_state.prefix_line_breaks))
                        elif p[1] == "alignment":
                            text_state.alignment = chr(ord(matched.group(1)))
                            message(2, "alignment type: {0}".format(text_state.alignment))
                            if not beginning_of_paragraph:
                                text_state.prefix_line_breaks += 1
                                beginning_of_paragraph = True
                                message(2, "add one line break for the alignment command. line breaks={0} ".format(text_state.prefix_line_breaks))
                            previous_byte = b'alignment'
                        elif p[1] == "background":
                            message(2, "background colour: {0} {1} {2}".format(int(matched.group(1)), int(matched.group(2)), int(matched.group(3))))
                            # Nothing to do here: background hint colour is only relevant when
                            # rendering using the FontManager on RISC OS. There is no equivalent
                            # for SVG.
                        elif p[1] == "colour":
                            text_state.text_colour = Convertor.ColourType(int(matched.group(1)), int(matched.group(2)), int(matched.group(3)))
                            message(2, "text foreground colour: {0} {1} {2}".format(int(matched.group(1)), int(matched.group(2)), int(matched.group(3))))
                        elif p[1] == "columns":
                            text_state.num_columns = int(matched.group(1))
                            message(2, "num columns: {0}".format(text_state.num_columns))
                        elif p[1] == "font size":
                            font_index = int(matched.group(1))
                            text_state.text_area_fonts[font_index] = Convertor.FontDesc(matched.group(2), int(matched.group(3)), int(matched.group(3)), self.font_replacements)
                            message(2, "font {0}: '{1}' {2}pt".format(int(matched.group(1)), Convertor.latin1_to_utf8(matched.group(2)), int(matched.group(3))))
                        elif p[1] == "font size width":
                            font_index = int(matched.group(1))
                            text_state.text_area_fonts[font_index] = Convertor.FontDesc(matched.group(2), int(matched.group(3)), int(matched.group(4)), self.font_replacements)
                            message(2, "font {0}: '{1}' {2}pt {3}pt".format(int(matched.group(1)), Convertor.latin1_to_utf8(matched.group(2)), matched.group(3), matched.group(4)))
                        elif p[1] == "setfont":
                            text_state.font_index = int(matched.group(1))
                            message(2, "Set Font {0}".format(text_state.font_index))
                        elif p[1] == "line leading":
                            text_state.line_spacing_px = CoordinateConversion.pt_to_px(int(matched.group(1)))
                            message(2, "Line spacing {0}".format(text_state.line_spacing_px))
                        elif p[1] == "margins":
                            text_state.left_margin_px  = CoordinateConversion.pt_to_px(int(matched.group(1)))
                            text_state.right_margin_px = CoordinateConversion.pt_to_px(int(matched.group(2)))
                            message(2, "Margins {0} {1}".format(text_state.left_margin_px, text_state.right_margin_px))
                        elif p[1] == "paragraph leading":
                            text_state.paragraph_spacing_px = CoordinateConversion.pt_to_px(int(matched.group(1)))
                            message(2, "Paragraph spacing {0}".format(text_state.paragraph_spacing_px))
                        elif p[1] == "underline":
                            text_state.underline_pos = int(matched.group(1))
                            text_state.underline_thickness = int(matched.group(2))
                            message(2, "Underline: pos {0} thickness {1}".format(text_state.underline_pos, text_state.underline_thickness))
                        elif p[1] == "underline end":
                            text_state.underline_pos = 0
                            text_state.underline_thickness = 0
                            message(2, "Underline end")
                        elif p[1] == "vertical move":
                            text_state.vertical_move_px += CoordinateConversion.pt_to_px(int(matched.group(1)))
                            message(2, "Vertical move: pos {0}".format(text_state.vertical_move_px))
                    break

            # DEBUG:
            #if is_debug_active():
            #    print("{0}:{1} ".format(remaining_text_bytes[0], chr(remaining_text_bytes[0])), end="")

            if offset == 1:
                should_output_char = True
                keep_previous_byte = None

                # deal with newlines
                if remaining_text_bytes[0] == 10:
                    should_output_char = False
                    if no_text_output_yet:
                        self.store_text_run(text_state)

                        # insert paragraph break for each newline before the text starts
                        text_state.prefix_para_breaks += 1
                        beginning_of_paragraph = True
                        message(2, "Add paragraph break for newline before any text. para breaks={0}".format(text_state.prefix_para_breaks))
                    else:
                        # Get next character (and handle being at end of text)
                        next_byte = None
                        if len(remaining_text_bytes)>1:
                            next_byte = remaining_text_bytes[1]

                        if next_byte == 32 or next_byte == 9:
                            # if newline followed by a space or TAB, then add a paragraph break
                            self.store_text_run(text_state)
                            if text_state.prefix_line_breaks == 0:
                                text_state.prefix_line_breaks += 1
                            text_state.prefix_para_breaks += 1
                            beginning_of_paragraph = True
                            message(2, "Add line and para break for newline followed by space or TAB. para breaks={0} line breaks={1}".format(text_state.prefix_para_breaks, text_state.prefix_line_breaks))
                        elif previous_byte == 10:
                            # Two newlines gives a paragraph break
                            self.store_text_run(text_state)
                            if text_state.prefix_line_breaks == 0:
                                text_state.prefix_line_breaks += 1
                                keep_previous_byte = 10
                            text_state.prefix_para_breaks += 1
                            beginning_of_paragraph = True
                            message(2, "Add line and para break for newline-newline. para breaks={0} line breaks={1}".format(text_state.prefix_para_breaks, text_state.prefix_line_breaks))
                            remaining_text_bytes = bytearray(b' ') + remaining_text_bytes[1:]

                        elif previous_byte == b'alignment':
                            text_state.prefix_para_breaks += 1
                            beginning_of_paragraph = True
                            message(2, "Add para break for alignment-newline. para breaks={0}".format(text_state.prefix_para_breaks))
                            remaining_text_bytes = bytearray(b' ') + remaining_text_bytes[1:]
                        elif previous_byte == 32 or previous_byte == 9:
                            # if previous character was a space or tab, ignore the newline
                            pass
                        else:
                            if next_byte != 10:
                                # replace single newline with space
                                message(2, "replace {0} with space. Previous byte {1}".format(next_byte, previous_byte))
                                remaining_text_bytes = bytearray(b' ') + remaining_text_bytes[1:]
                                should_output_char = True

                if keep_previous_byte:
                    previous_byte = keep_previous_byte
                else:
                    previous_byte = remaining_text_bytes[0]

                if should_output_char:
                    # Control characters are ignored, except for tab, which is replaced by a space.
                    c = remaining_text_bytes[0]
                    if c >= 32:
                        text_state.plain_text.append(remaining_text_bytes[0])
                        no_text_output_yet = False
                        beginning_of_paragraph = False
                    elif c == 9:
                        text_state.plain_text.append(b" ")
                        no_text_output_yet = False
                        beginning_of_paragraph = False

            remaining_text_bytes = remaining_text_bytes[offset:]

        # Finish any final text run
        self.store_text_run(text_state)

        # Convert text to UTF8
        for run in self.text_runs:
            run.text_state.plain_text = run.text_state.to_utf8(self.config)

    def format_text_runs(self, fout, object_header, text_columns):
        # Some number of text runs will make up a single line of text (possibly splitting the
        # final run in two)

        #for col in text_columns:
        #    print("Text Column:", self.dp(col[0].x), self.dp(col[0].y), self.dp(col[1].x), self.dp(col[1].y))

        message(2, "Number of runs: {0}".format(len(self.text_runs)))

        # First measure the width of each run
        for run in self.text_runs:
            run.measure()
            run.message(2)

        # Start with all runs
        remaining_text_runs = self.text_runs
        is_first_line = True

        # Width of the text column
        text_column_index = 0
        bottom_left = text_columns[text_column_index][0]
        top_right   = text_columns[text_column_index][1]

        # Start position
        y = top_right.y + self.text_runs[0].text_state.line_spacing_px
        is_start_of_text_column = True

        #run = remaining_text_runs[0]

        while len(remaining_text_runs) > 0:
            # Start of a line
            last_line_of_paragraph = False

            x = bottom_left.x
            # Apply line and paragraph spacing
            run = remaining_text_runs[0]
            if run.text_state.prefix_line_breaks > 0:
                y += run.text_state.line_spacing_px + run.text_state.paragraph_spacing_px * (run.text_state.prefix_line_breaks - 1)

            # 'paragraph leading at the top of a new text column is ignored'
            if not is_start_of_text_column:
                y += run.text_state.paragraph_spacing_px * run.text_state.prefix_para_breaks

            run.text_state.prefix_line_breaks = 0
            run.text_state.prefix_para_breaks = 0

            text_area_width = top_right.x - bottom_left.x - run.text_state.left_margin_px - run.text_state.right_margin_px

            # Check for end of text column
            if y >= bottom_left.y:
                # We have reached the end of a text column, start at the top of the next column
                # Width of the text column
                text_column_index += 1
                if text_column_index < len(text_columns):
                    # start a new text column
                    bottom_left = text_columns[text_column_index][0]
                    top_right   = text_columns[text_column_index][1]

                    text_area_width = top_right.x - bottom_left.x - run.text_state.left_margin_px - run.text_state.right_margin_px

                    # Start position
                    x = bottom_left.x

                    y = top_right.y + run.text_state.line_spacing_px
                    is_start_of_text_column = True
                else:
                    # Reached the end of all columns
                    break

            # Find out how many runs will fit on the current line
            current_width = 0
            line_text_runs = []
            while (len(remaining_text_runs) > 0) and (current_width < text_area_width):
                # If we reach a run with prefix line breaks or para breaks, then break out (this is the last line of a paragraph)
                end_of_paragraph = ((remaining_text_runs[0].text_state.prefix_line_breaks > 0) or (remaining_text_runs[0].text_state.prefix_para_breaks > 0))
                if (len(line_text_runs) > 0) and end_of_paragraph:
                    last_line_of_paragraph = True
                    break
                line_text_runs.append(remaining_text_runs[0])
                remaining_text_runs = remaining_text_runs[1:]
                previous_width = current_width
                line_text_runs[-1].measure()
                current_width += line_text_runs[-1].text_state.length

            final_run = line_text_runs[-1]
            # Now we have added the final run, we may have gone past the end of the line.
            if current_width > text_area_width:
                # Cut off one word at a time, to find the best place to line break the text.
                # If we get down to a single word, then cut down by one character at a time until
                # we reach one character. Draw at least that.

                # make a copy of the final run
                test_run = copy.deepcopy(final_run)
                test_run.text_state.prefix_line_breaks = 0
                test_run.text_state.prefix_para_breaks = 0
                full_text = final_run.text_state.plain_text

                number_of_spaces_on_current_line = 0
                for run in line_text_runs[:-1]:
                    number_of_spaces_on_current_line += run.text_state.plain_text.count(' ')
                    #print("PLN TEXT:'{0}'".format(run.text_state.plain_text))
                #print("SPACES:", number_of_spaces_on_current_line)

                while (current_width > text_area_width) and (len(test_run.text_state.plain_text) > 1):
                    # TODO: Handle leading spaces / soft hyphens
                    last_space = test_run.text_state.plain_text.rfind(' ')
                    last_soft_hyphen = test_run.text_state.plain_text.rfind('\u00ad')
                    if (last_soft_hyphen > 0) and (last_soft_hyphen > last_space):
                        # Try chopping off at the final soft hyphen (adding an actual hyphen instead)
                        test_run.text_state.plain_text = test_run.text_state.plain_text[0:last_soft_hyphen] + "-"
                    elif last_space > 0:
                        # Chop off the final word
                        test_run.text_state.plain_text = test_run.text_state.plain_text[0:last_space]
                    elif len(test_run.text_state.plain_text) > 1:
                        if number_of_spaces_on_current_line == 0:
                            # if there is only one word on the current line, chop off a character
                            # at a time.
                            test_run.text_state.plain_text = test_run.text_state.plain_text[0:-1]
                        else:
                            # not one word of this run fits on the current line.
                            test_run.text_state.plain_text = ""
                            test_run.measure()
                            current_width = previous_width + test_run.text_state.length

                            # strip any final space
                            line_text_runs[-1].text_state.plain_text = line_text_runs[-1].text_state.plain_text.rstrip()
                            line_text_runs[-1].measure()
                            break

                    # Re-measure the shorter text
                    test_run.measure()
                    #print("new measure=", test_run.text_state.length, "for text:", test_run.text_state.plain_text)

                    # Get the current width now we have measured the final run
                    current_width = previous_width + test_run.text_state.length

                # Now we know how much text fits on the line, we split the final run into two parts
                # (1) The part that fits on the current line, and (2) the remaining text that doesn't.

                # (2) the remaining text that doesn't fit.
                new_run = line_text_runs[-1]
                new_run.text_state.prefix_line_breaks = 0
                new_run.text_state.prefix_para_breaks = 0
                start = len(test_run.text_state.plain_text)
                # Remainder of string, removing any whitespace at the start of the line
                new_run.text_state.plain_text = new_run.text_state.plain_text[start:].lstrip()
                if (len(new_run.text_state.plain_text) > 0):
                    new_run.vertical_move_px = 0
                    new_run.measure()
                    remaining_text_runs.insert(0, new_run)

                # (1) The part that fits on the current line.
                line_text_runs[-1] = copy.copy(test_run)

            # Output current line (line_text_runs)
            last_line_of_paragraph = last_line_of_paragraph or (len(remaining_text_runs) == 0)

            # How much to indent the line for centre / right alignment
            line_offset_x = run.text_state.left_margin_px
            if run.text_state.alignment == 'R':     # right
                line_offset_x += text_area_width - current_width
            elif run.text_state.alignment == 'C':   # centre
                line_offset_x += (text_area_width - current_width) / 2

            num_characters_on_line = 0
            for run in line_text_runs:
                num_characters_on_line += len(run.text_state.plain_text)
            num_gaps_on_line = num_characters_on_line - 1

            letter_spacing = 0.0
            if (run.text_state.alignment == 'D') and (not last_line_of_paragraph) and (not run.text_state.ignore_full_justification) and (num_gaps_on_line > 0):
                letter_spacing = (text_area_width - current_width) / num_gaps_on_line

            for run in line_text_runs:
                text_state = run.text_state
                font = text_state.text_area_fonts[text_state.font_index]

                text_decoration = ""
                if (run.text_state.underline_thickness > 0) and (font.height_pts > 0):
                    # Underline the text
                    decoration = "underline"
                    if not self.config.basic_underlines:
                        decoration += " {0}pt {1}".format(
                            self.dp(run.text_state.underline_thickness * font.height_pts / 256),
                            run.text_state.text_colour)

                    text_decoration = " text-decoration='{0}'".format(decoration)

                style_for_text = 'font-family=\'{0}\' font-size="{1}pt" font-weight="{2}" font-style="{3}" letter-spacing="{4}" fill="{5}"{6}'.format(
                    font.name,
                    font.height_pts,
                    font.weight,
                    font.style,
                    self.dp(letter_spacing),
                    text_state.text_colour,
                    text_decoration)
                style_for_text += ' xml:space="preserve"'

                style_for_text += " transform='translate({0} {1}) scale({2} 1)'".format(
                    self.dp(x + line_offset_x),
                    self.dp(y - run.text_state.vertical_move_px),
                    self.dp(font.width_pts / font.height_pts))

                if self.config.use_tspans:
                    # Start by opening <text> then use <tspans> for the remaining runs.
                    if is_first_line:
                        fout.write("<text {0}>{1}\n".format(
                            style_for_text,
                            Convertor.escape(text_state.plain_text)))
                        is_first_line = False
                    else:
                        fout.write("<tspan {0}>{1}</tspan>\n".format(
                            style_for_text,
                            Convertor.escape(text_state.plain_text)))
                else:
                    # Use individual <text> runs.
                    fout.write("<text {0}>{1}</text>\n".format(
                        style_for_text,
                        Convertor.escape(text_state.plain_text)))
                x += run.text_state.length + (len(run.text_state.plain_text)-1) * letter_spacing

            is_start_of_text_column = False
            if len(remaining_text_runs) > 0:
                # Add a newline if no newlines already present
                if (remaining_text_runs[0].text_state.prefix_line_breaks == 0) and (remaining_text_runs[0].text_state.prefix_para_breaks == 0):
                    remaining_text_runs[0].text_state.prefix_line_breaks = 1
                    #message(2, "add line break if none already")

        if self.config.use_tspans:
            fout.write('</text>\n')


    def read_text_area_object(self, fin, fout, object_header):
        global debug_index

        text_columns = []
        # Read any text column objects until we reach a terminator
        while True:
            object_type = Convertor.peek_uint(fin)
            if object_type != 0:
                obj_header = Convertor.ObjectHeader()
                obj_header.read(fin, self.config)
                bottom_left = self.cc.draw_to_svg_point(obj_header.low)
                top_right   = self.cc.draw_to_svg_point(obj_header.high)

                # Don't allow columns with width <= 0
                if top_right.x - bottom_left.x > 0:
                    bbox = (bottom_left, top_right)
                    text_columns.append((bottom_left, top_right))
            else:
                # Skip past reserved bytes
                Convertor.read_uint(fin)
                Convertor.read_uint(fin)
                Convertor.read_uint(fin)
                break

        foreground_colour      = Convertor.ColourType()
        background_hint_colour = Convertor.ColourType()
        foreground_colour.read(fin)
        background_hint_colour.read(fin)
        message(2, "Text area foreground colour: {0}".format(foreground_colour))
        message(2, "Text area background hint colour: {0}".format(background_hint_colour))

        # We read in the text as a byte array so that we don't lose data in the conversion from
        # bytes into string. We don't know the encoding of some of the data yet (the plain_text
        # of each run).
        #
        # Later we will convert the plain_text part each run to proper UTF-8.
        text_bytes = Convertor.read_bytes_until_zero(fin)
        message(2, "Text area has {0} text columns. Debug Index: {1} Text: {2}".format(len(text_columns), debug_index, text_bytes))

        for col in text_columns:
            message(2, "  Text column: {0} {1}".format(col[0], col[1]))

        self.parse_text_area_text(text_bytes, text_columns, fout)
        self.format_text_runs(fout, object_header, text_columns)

    def read_options_object(self, fin, fout, object_header):
        self.options = Convertor.Options()
        self.options.read(fin)

        message(2, "Paper size in mm: {0}".format(self.options.paper_size_mm()))

    def get_proper_text_width(self, w, h, a, b, c, d, rotation, skew_x, font_height):
        # For a transformed text object, 'Draw' doesn't actually store the true width of the text.
        # It stores a 2x2 matrix (a,b,c,d) of the transformation that is applied to the text, and
        # the resultant bounding box (w,h) after transformation.
        #
        # We want to know the true width of the text to make sure it is drawn at the correct width
        # despite being drawn using a (modern) font with different metrics than the RISC OS fonts.
        #
        # So we use some fancy maths to extract the width of the line of text.
        #
        # We only rely on the height of the font in degenerate cases, since it is not normally required.
        #
        # (This was quite an interesting diversion to derive. 'Processing' was an invaluable tool
        # to test the results of my calculations.)

        # Height of the font after transformation.
        transformed_font_height = font_height * math.sqrt(c*c + d*d)
        cossx = math.cos(skew_x)
        if math.fabs(cossx) < 0.001:
            cossx = 0.001
        transformed_font_height = font_height / cossx

        # Create indexes based on the signs of each of a,b,c,d.
        index1 = 2*(b<0) + (a<0)
        index2 = 2*(d<0) + (c<0)

        # Get angles theta and phi, depending on the quadrants of (a,b) and (c,d)
        if index1 == 0:
            theta = rotation
        elif index1 == 1:
            theta = math.pi - rotation
        elif index1 == 2:
            theta = -rotation
        else: #index1 == 3:
            theta = math.pi + rotation

        if index2 == 0:
            phi = skew_x - rotation
        elif index2 == 1:
            phi = -(skew_x - rotation)
        elif index2 == 2:
            phi = math.pi - (skew_x - rotation)
        else: # index2 == 3:
            phi = math.pi + (skew_x - rotation)

        # Finally, calculate the text_width using these angles and the bounding box.
        costp = math.cos(phi+theta)
        if math.fabs(costp) < 0.001:
            # Deal with degenerate edge cases
            cost = math.cos(theta)
            if math.fabs(cost) < 0.001:
                text_width = h - transformed_font_height
            else:
                text_width = (w - transformed_font_height*math.sin(phi))/ math.cos(theta)
        else:
            text_width = (w * math.cos(phi) - h * math.sin(phi)) / costp

        return(text_width)


    def get_text_transform_info(self, matrix, object_header, text_header):
        # Decompose the matrix into translation, skew, rotation, scale

        (translation, rotation, skew, scale) = matrix.decompose()

        # The bounding box of an object in Draw specifies the bottom left and top right points
        # on the page for that object. This description remains true when converted to SVG coordinates.
        # Note: The terms 'low' and 'high' are not so useful terms once converted.
        bottom_left = self.cc.draw_to_svg_point(object_header.low)
        top_right   = self.cc.draw_to_svg_point(object_header.high)

        svg_fontsize_pixels = self.cc.draw_to_svg_size(Convertor.Coords(text_header.xsize, text_header.ysize))

        # Failsafe
        if math.fabs(svg_fontsize_pixels.x) < epsilon:
            svg_fontsize_pixels.x = epsilon

        pos = self.cc.draw_to_svg_point(text_header.baseline)

        box_width = top_right.x - bottom_left.x
        box_height = bottom_left.y - top_right.y

        # Account for skew in text_width
        font_aspect_ratio = svg_fontsize_pixels.y / svg_fontsize_pixels.x

        text_width = self.get_proper_text_width(box_width, box_height, matrix.a, matrix.b, matrix.c, matrix.d, -rotation, -skew.x, svg_fontsize_pixels.y)
        #print("box_width: ", self.dp(box_width), "box_height:", self.dp(box_height), "true text width:", self.dp(text_width), "matrix:", self.dp(matrix.a), self.dp(matrix.b), self.dp(matrix.c), self.dp(matrix.d), "rotation:", self.dp(rotation), "skew:", skew, "font size (px):", svg_fontsize_pixels)

        # Take font aspect ratio into account by scaling in Y
        scale.y *= font_aspect_ratio

        # translate, skew, rotate, scalex, scaley
        return (pos, rotation, skew, scale, text_width)

    def get_sprite_transform(self, matrix, object_header):
        # Decompose the matrix into translation, skew, rotation, scale
        (translation, rotation, skew, scale) = matrix.decompose()

        # translate, skew, rotate, scale
        transform = 'translate({0} {1}) rotate({2}) skewX({3}) skewY({4}) scale({5} {6})'.format(
            self.dp(translation.x),
            self.dp(translation.y),
            self.dp(math.degrees(rotation)),
            self.dp(math.degrees(skew.x)),
            self.dp(math.degrees(skew.y)),
            self.dp(scale.x),
            self.dp(scale.y))
        return transform


    def read_trans_text_object(self, fin, fout, object_header):
        matrix = Convertor.DrawMatrix()
        matrix.read(fin)
        matrix = self.cc.draw_to_svg_matrix(matrix)

        font_flags = Convertor.read_uint(fin, 4)

        message(2, "  Transformed Text:")
        message(2, "    Draw Matrix:")
        message(2, "{0}".format(matrix))
        message(2, "    Font Flags: {0}".format(font_flags))

        text_header = Convertor.TextHeader()
        text_header.read(fin)

        (pos, angle, skew, scale, text_width) = self.get_text_transform_info(matrix, object_header, text_header)

        transform = 'transform="translate({0} {1}) rotate({2}) skewX({3}) skewY({4}) scale({5} {6})"'.format(
            self.dp(pos.x),
            self.dp(pos.y),
            self.dp(math.degrees(angle)),
            self.dp(math.degrees(skew.x)),
            self.dp(math.degrees(skew.y)),
            self.dp(scale.x),
            self.dp(scale.y))

        if (font_flags & 2) == 2:
            transform += ' direction="rtl"'

        self.read_text_object(fin, fout, object_header, text_header, text_width, font_flags, transform, Point(0, 0))

    def read_objects(self, fin, fout, length):
        global debug_index

        saveptr = fin.tell()
        while True:
            curptr = fin.tell()
            object_header = Convertor.ObjectHeader()
            object_header.read(fin, self.config)
            debug_index += 1

            if fout == None:
                # First pass: Just look for and read an options object
                if object_header.obj_type == Convertor.OBJECT_OPTIONS:
                    self.read_options_object(fin, fout, object_header)
            else:
                bottom_left = self.cc.draw_to_svg_point(object_header.low)
                top_right   = self.cc.draw_to_svg_point(object_header.high)

                # Show object names
                if object_header.obj_type in Convertor.objectnames:
                    message(2, " ------------------------------------------------\n Object type: {0}={1}, (index={6}) bounding box ({2},{3} to {4},{5})".format(
                        object_header.obj_type,
                        Convertor.objectnames[object_header.obj_type],
                        self.dp(bottom_left.x), self.dp(bottom_left.y),
                        self.dp(top_right.x), self.dp(top_right.y),
                        debug_index))
                else:
                    message(2, " Object type: {0}, (index={1})".format(object_header.obj_type, debug_index))

                if object_header.obj_type == Convertor.OBJECT_OPTIONS:
                    self.read_options_object(fin, fout, object_header)
                elif object_header.obj_type == Convertor.OBJECT_FONTTABLE:
                    self.read_font_table_object(fin, object_header, curptr)
                elif object_header.obj_type == Convertor.OBJECT_TEXT:
                    text_header = Convertor.TextHeader()
                    text_header.read(fin)
                    self.read_text_object(fin, fout, object_header, text_header)
                elif object_header.obj_type == Convertor.OBJECT_TRANSTEXT:
                    self.read_trans_text_object(fin, fout, object_header)
                elif object_header.obj_type == Convertor.OBJECT_PATH:
                    self.read_path_object(fin, fout, object_header)
                elif object_header.obj_type == Convertor.OBJECT_GROUP:
                    self.read_group_object(fin, fout, object_header)
                elif object_header.obj_type == Convertor.OBJECT_SPRITE:
                    self.read_sprite_object(fin, fout, object_header)
                elif object_header.obj_type == Convertor.OBJECT_TRANSSPRITE:
                    self.read_sprite_object(fin, fout, object_header)
                elif object_header.obj_type == Convertor.OBJECT_TAGGED:
                    self.read_tagged_object(fin, fout, object_header)
                elif object_header.obj_type == Convertor.OBJECT_TEXTAREA:
                    self.read_text_area_object(fin, fout, object_header)
                elif object_header.obj_type == Convertor.OBJECT_JPEG:
                    self.read_jpeg_object(fin, fout, object_header)
                else:
                    warning("Unknown object type {0}, skipping".format(object_header.obj_type))

                    bottom_left = self.cc.draw_to_svg_point(object_header.low)
                    top_right   = self.cc.draw_to_svg_point(object_header.high)
                    fout.write('<rect x="{0}" y="{1}" width="{2}" height="{3}" stroke="none" fill="#a0a0a080" />\n'.format(bottom_left.x, top_right.y, top_right.x - bottom_left.x, bottom_left.y - top_right.y))

                # Show bounding box on top of object
                if self.config.show_bounding_boxes:
                    # Show object bounding boxes
                    bottom_left = self.cc.draw_to_svg_point(object_header.low)
                    top_right   = self.cc.draw_to_svg_point(object_header.high)
                    fout.write('<rect x="{0}" y="{1}" width="{2}" height="{3}" stroke="#ff0000" fill="none" />\n'.format(bottom_left.x, top_right.y, top_right.x - bottom_left.x, bottom_left.y - top_right.y))

                # Show index
                if self.config.show_debug_index:
                    fout.write("<text x='{0}' y='{1}'>{2}</text>\n".format(self.dp(bottom_left.x), self.dp(top_right.y + 12), Convertor.escape("{0}".format(debug_index))))
                debug_index += 1


            # Are we done?
            if Convertor.eof(fin, self.file_size):
                break

            fin.seek(curptr + object_header.obj_length, 0)

            # Are we done?
            if Convertor.eof(fin, self.file_size):
                break

            if (length != -1) and fin.tell()>=(saveptr+length):
                break

    def add_entry(self, result, text):
        if len(result) > 0:
            result += ','

        if (" " in text) or ("," in text):
            result += '"' + text + '"'
        else:
            result += text
        return result

    def add_quotes_in_comma_separated_list(self,text):
        # In a comma separated list, add quotes around any entries that have spaces in them (unless they are already quoted)
        i = 0
        inQuotes = False
        result = ""
        entry = ""
        while i < len(text):
            if text[i] == '"':
                inQuotes = not inQuotes
            elif text[i] == ',' and not inQuotes:
                # end of entry
                result = self.add_entry(result, entry)

                # start new entry
                entry = ""
            else:
                entry += text[i]
            i += 1
        result = self.add_entry(result, entry)
        return result

    def convert_to_svg(self, infile, outfile = None):
        self.cap_count = 0
        self.path_count = 0

        global debug_index
        debug_index = 0

        # Read external ini file for font stacks if specified:
        self.font_replacements = {}
        if self.config.fonts_ini:
            cp = ConfigParser()
            cp.optionxform = lambda option: option      # Don't convert keys to lowercase
            cp.read(self.config.fonts_ini)              # Read ini file
            if "main" in cp:
                # Read "main" section into font_replacements dictionary, quoting as needed
                for k in cp["main"]:
                    self.font_replacements[k.lower()] = self.add_quotes_in_comma_separated_list(cp["main"][k])

        # Use default font stacks:
        if len(self.font_replacements) == 0:
            self.font_replacements = Convertor.default_font_replacements.copy()

        if outfile == None:
            outfile = infile + ".svg"

        message(1, "File {0}".format(os.path.abspath(outfile)))

        file_header = Convertor.FileHeader()

        with open(infile, 'rb') as fin:
            fin.seek(0, 2)              # move to end of file
            self.file_size = fin.tell() # get file size
            fin.seek(0, 0)              # move to start of file

            if not file_header.read(fin):
                return False

            file_header.print(self, infile, 2)

            # Pass 1: Search for 'options' object to tell us page size
            self.options = None

            message(2, "Pass 1")
            start_here = fin.tell() # Remember start point
            self.read_objects(fin, None, -1)
            fin.seek(start_here, 0)  # move back to start point
            message(2, "Pass 2")

            if self.options == None:
                # Use default options if none specified (i.e. A0, Portrait)
                self.options = Convertor.Options()

                file_dims_pts = (file_header.high_box.x/640.0, file_header.high_box.y/640.0)
                file_dims_px  = (CoordinateConversion.pt_to_px(file_dims_pts[0]), CoordinateConversion.pt_to_px(file_dims_pts[1]))

                # Allow a little extra leeway when choosing the best paper size?
                # file_dims_px = (file_dims_px[0] * 0.99, file_dims_px[1] * 0.99)

                for i in Convertor.a4_and_up:
                    size_in_mm = Convertor.paper_sizes[i]
                    size_in_pixels = (size_in_mm[0] * 3.7795, size_in_mm[1] * 3.7795)

                    if (file_dims_px[0] < size_in_pixels[1]) and (file_dims_px[1] < size_in_pixels[0]):
                        # Landscape fits
                        self.options.paper_size = i
                        self.options.paper_limits = 16
                        message(2, "{0} landscape".format(hex(i)))
                        break
                    if (file_dims_px[0] < size_in_pixels[0]) and (file_dims_px[1] < size_in_pixels[1]):
                        # Portrait fits
                        self.options.paper_size = i
                        message(2, "{0} portrait".format(hex(i)))
                        break
                    message(2, "size in pixels {0} {1} {2}".format(hex(i), size_in_pixels[0], size_in_pixels[1]))

            # For SVG units, see https://oreillymedia.github.io/Using_SVG/guide/units.html
            # We use pixel ('px') coordinates for SVG.
            size_in_mm = self.options.paper_size_mm()
            size_in_pixels = (size_in_mm[0] * 3.7795, size_in_mm[1] * 3.7795)

            # Definitions:
            # 1 inch = 2.54 cm = 25.4mm
            # 1 inch = 180 OS units
            # 1 OS unit = 256 draw units

            # So:
            # 25.4mm = 1 inch = 180 OS units = 256*180 draw units = 46080 draw units
            # 1mm = 46080 / 25.4 draw units
            mm_to_draw_units = 46080 / 25.4
            size_in_draw_units = (size_in_mm[0] * mm_to_draw_units, size_in_mm[1] * mm_to_draw_units)

            # Initialise coordinate conversion object
            self.cc = CoordinateConversion(size_in_draw_units[0], size_in_draw_units[1], size_in_pixels[0], size_in_pixels[1])

            # Pass 2: Parse all objects and write out the results
            with open(outfile, 'w') as fout:

                # Write file header out, including page size
                fout.write('<?xml version="1.0" encoding="UTF-8"?>\n<!-- Generated by \'draw_to_svg.py\' (by TobyLobster) -->\n')

                # File's bounding box
                bottom_left = self.cc.draw_to_svg_point(file_header.low_box)
                top_right   = self.cc.draw_to_svg_point(file_header.high_box)

                if convertor.config.fit_border:
                    # For 50 pixel border, say '50px' or '50'
                    # For 20 percent border, say '20%'

                    bounding_box = [bottom_left.x, top_right.y, top_right.x, bottom_left.y]
                    matched = re.match("([\+\-\.\d]+)(.*)", convertor.config.fit_border)
                    if matched:
                        border_pixels_x = float(matched.group(1))
                        border_pixels_y = float(matched.group(1))
                        units = matched.group(2).strip().lower()
                        if units == "%":
                            border_pixels_x = (top_right.x - bottom_left.x) * border_pixels_x / 100.0
                            border_pixels_y = (bottom_left.y - top_right.y) * border_pixels_y / 100.0

                    bounding_box[0] -= border_pixels_x
                    bounding_box[1] -= border_pixels_y
                    bounding_box[2] += border_pixels_x
                    bounding_box[3] += border_pixels_y
                else:
                    bounding_box = [0, 0, size_in_pixels[0], size_in_pixels[1]]

                fout.write('<svg xmlns="http://www.w3.org/2000/svg" xml:space="preserve" viewBox="{0} {1} {2} {3}" xmlns:xlink="http://www.w3.org/1999/xlink">\n'.format(
                   self.dp(bounding_box[0]),
                   self.dp(bounding_box[1]),
                   self.dp(bounding_box[2] - bounding_box[0]),
                   self.dp(bounding_box[3] - bounding_box[1]) ))
                fout.write("")

                #fout.write("<style>")
                #fout.write('@import url("https://fonts.googleapis.com/css?family=VT323");')
                #fout.write("</style>")

                self.read_objects(fin, fout, -1)

                if convertor.config.show_bounding_boxes:
                    # Show file's bounding border in green
                    fout.write('<rect x="{0}" y="{1}" width="{2}" height="{3}" stroke="#00ff00" fill="none" />\n'.format(bottom_left.x, top_right.y, top_right.x - bottom_left.x, bottom_left.y - top_right.y))

                fout.write('</svg>')

        return True

convertor = Convertor()

class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

    def print_help(self, venue=sys.stdout):
        print("""usage: draw_to_svg.py <options>

Converts Acorn's Draw files to SVG.

options:
  -h   --help                 show this help message and exit
  -d   --dir <directory>      search recursively from <directory> for .draw files to convert (overrides --input and --output)
  -i   --input INPUT          input draw filepath
  -o   --output OUTPUT        output SVG filepath
  -8   --utf8                 assume all text in the Draw file is already UTF8 encoded, no conversion needed
  -s   --tspans               uses SVG <tspan>s to output text areas (but these are not well supported by SVG renderers)
  -v                          output verbosity level 1, which shows each filename as it's being processed
  -vv                         output verbosity level 2, which shows lots of debugging data as it's being processed
  -u   --basic-underlines     use basic underlines (no colour or thickness) to help out Safari that can't cope
  -n   --no-bbox              ignore the bounding box width when outputting text
  -f   --fonts <ini-file>     fonts ini file listing the replacement font stacks
  -b   --fit-border <amount>  Set SVG page size to match Draw content with a border amount in pixels or percentage (e.g. '50px' or '20%')
  -1   --one-byte-types       Some applications use a one byte object type, as opposed to the default two byte value

For debugging the tool:
  -l   --label-debug          add debugging labels to each object
  -x   --show-boxes           for debugging purposes, show the bounding box for each object
""", file=venue)

if __name__ == '__main__':
    parser = MyParser(
                    prog="draw_to_svg",
                    description="Converts Acorn's Draw files to SVG",
                    epilog="TobyLobster, 2023")

    parser.add_argument('-d', '--dir',              help="search recursively for .draw files to convert", metavar="<directory>")
    parser.add_argument('-i', '--input',            help="input draw filepath")
    parser.add_argument('-o', '--output',           help="output SVG filepath")
    parser.add_argument('-8', '--utf8',             help="assume all UTF8 text, no conversion needed", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument('-s', '--tspans',           help="uses SVG <tspan>s to output text areas (but these are not well supported by SVG renderers)", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument('-v', '--verbose',          help="output verbosity (0, 1, or 2)", action='count', default=0)
    parser.add_argument('-l', '--label-debug',      help="add debugging labels to each object", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument('-x', '--show-boxes',       help="for debugging purposes, show bounding box for each object", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument('-u', '--basic-underlines', help="use basic underlines (no colour or thickness) to help out Safari that can't cope", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument('-n', '--no-bbox',          help="ignore the bounding box width when outputting text", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument('-f', '--fonts',            help="fonts ini file listing the replacement font stacks", metavar="<ini-file>")
    parser.add_argument('-1', '--one-byte-types',   help="Some applications use a one byte object type, as opposed to the default two byte value", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument('-b', '--fit-border',       help="fit page size to match SVG with a border amount in pixels or percentage (e.g. '50px' or '20%%')", metavar="<border-amount>")

    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    convertor.config.verbose_level       = args.verbose
    convertor.config.utf8                = args.utf8
    convertor.config.use_tspans          = args.tspans
    convertor.config.show_debug_index    = args.label_debug
    convertor.config.show_bounding_boxes = args.show_boxes
    convertor.config.basic_underlines    = args.basic_underlines
    convertor.config.use_bbox            = not args.no_bbox
    convertor.config.fonts_ini           = args.fonts
    convertor.config.fit_border          = args.fit_border
    convertor.config.one_byte_types      = args.one_byte_types

    if (args.input != None) and (args.output != None):
        if args.input == args.output:
            error("Input and output are the same")
            exit(-2)
        convertor.convert_to_svg(args.input, args.output)
        exit(0)

    if args.dir != None:
        path = Path(args.dir)
        for p in path.rglob("*"):
            filename, file_extension = os.path.splitext(p)
            if file_extension.lower() != ".draw":
                continue
            convertor.convert_to_svg(p, str(p)+".svg")

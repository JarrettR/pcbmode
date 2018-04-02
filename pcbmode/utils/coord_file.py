#!/usr/bin/python

import os
import re
import pcbmode.config as config

from . import utils
from . import messages as msg
from .shape import Shape
from .style import Style


def makeCoordFile(arg=False):
    """

    """


    def _getOutline():
        """
        Process the module's outline shape. Modules don't have to have an outline
        defined, so in that case return None.
        """
        shape = None

        outline_dict = config.brd.get('outline')
        if outline_dict != None:
            shape_dict = outline_dict.get('shape')
            if shape_dict != None:
                shape = Shape(shape_dict)
                style = Style(shape_dict, 'outline')
                shape.setStyle(style)

        return shape

    # A dict of the components
    comp_dict = config.brd['components']

    # Get the board's dimensions
    # This gives the bounding box of the shape
    outline = _getOutline()
    board_width = outline.getWidth()
    board_height = outline.getHeight()

    board_name = config.cfg['name']
    board_revision = config.brd['config'].get('rev')
    base_name = "%s_rev_%s" % (board_name, board_revision)

    coord_path = os.path.join(config.cfg['base-dir'],
                              config.cfg['locations']['build'],
                              'production')

    coord_csv_c = os.path.join(coord_path, base_name + '_%s_%s.csv'% ('coord_file', 'CENTRE'))
    coord_csv_bl = os.path.join(coord_path, base_name + '_%s_%s.csv'% ('coord_file', 'BOTTOM_LEFT'))

    # To print as the file's header
    preamble = ("This file was auto-generated by PCBmodE.\n\nThe coordinates are relative to the %s of the board outline shape\n\nRotation is in degrees, clockwise, and as seen from the\ntop or EACH layer. Confirm with ASSEMBLY DRAWING for correctness.\n\nAll dimension are in MILLIMETERS (mm).\n\n")

    # CSV header
    header = "%s,%s,%s,%s,%s" % ('Designator',
                                 'Placement-layer',
                                 'Coord-X(mm)',
                                 'Coord-Y(mm)',
                                 'Rotation(deg)')

    # Create coordinate file with centre as origin
    # as it is in the board's json
    with open(coord_csv_c, "wb") as f:
        f.write(preamble % 'CENTRE'+'\n')
        f.write(header+'\n')
        for refdef in comp_dict:
            ent = comp_dict[refdef]
            f.write("%s,%s,%s,%s,%s\n" % (refdef,
                                          ent['layer'],
                                          ent['location'][0],
                                          ent['location'][1],
                                          ent['rotate']))



    # Create coordinate file with bottom left as origin
    with open(coord_csv_bl, "wb") as f:
        f.write(preamble % 'BOTTOM LEFT'+'\n')
        f.write(header+'\n')
        for refdef in comp_dict:
            ent = comp_dict[refdef]
            f.write("%s,%s,%s,%s,%s\n" % (refdef,
                                          ent['layer'],
                                          board_width/2 + ent['location'][0],
                                          board_height/2 + ent['location'][1],
                                          ent['rotate']))




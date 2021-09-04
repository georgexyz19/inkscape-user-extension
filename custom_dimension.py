#!/usr/bin/env python
# coding=utf-8
#
# Copyright (C) 2007 Peter Lewerin, peter.lewerin@tele2.se
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
"""
An Inkscape effect for adding CAD style dimensions to selected objects
in a drawing.

It uses the selection's bounding box, so if the bounding box has empty
space in the x- or y-direction (such as with some stars) the results
will look strange.  Strokes might also overlap the edge of the
bounding box.

The dimension arrows aren't measured: use the "Visualize Path/Measure
Path" effect to add measurements.

This code contains snippets from existing effects in the Inkscape
extensions library, and marker data from markers.svg.
"""

import inkex
from inkex import Group, Marker, PathElement

import pathmodifier


from draw_arrowhead import Arrow
from draw_arrowhead import NewPath
from inkex import Style


class Dimension(pathmodifier.PathModifier):
    """Add dimensions as a path modifier"""
    def add_arguments(self, pars):
        pars.add_argument("--xoffset", type=float, default=100.0,\
            help="x offset of the vertical dimension arrow")
        pars.add_argument("--yoffset", type=float, default=100.0,\
            help="y offset of the horizontal dimension arrow")
        pars.add_argument("--type", default="geometric", help="Bounding box type")

    def add_marker(self, name, rotate):
        """Create a marker in the defs of the svg"""
        marker = Marker()
        marker.set('id', name)
        marker.set('orient', 'auto')
        marker.set('refX', '0.0')
        marker.set('refY', '0.0')
        marker.set('style', 'overflow:visible')
        marker.set('inkscape:stockid', name)
        self.svg.defs.append(marker)

        arrow = PathElement(d='M 0.0,0.0 L 5.0,-5.0 L -12.5,0.0 L 5.0,5.0 L 0.0,0.0 z ')
        if rotate:
            arrow.set('transform', 'scale(0.8) rotate(180) translate(12.5,0)')
        else:
            arrow.set('transform', 'scale(0.8) translate(12.5,0)')
        arrow.set('style', 'fill-rule:evenodd;stroke:#000000;stroke-width:1.0pt;marker-start:none')
        marker.append(arrow)

    def horz_line(self, y, xlat, bbox):
        """Create a horzontal line"""
        line = PathElement()
        x1 = bbox.left - xlat[0] * self.options.xoffset
        x2 = bbox.right
        y1 = y - xlat[1] * self.options.yoffset
        line.set('d', 'M %f %f H %f' % (x1, y1, x2))
        return line

    def vert_line(self, x, xlat, bbox):
        """Create a vertical line"""
        line = PathElement()
        x = x - xlat[0] * self.options.xoffset
        y1 = bbox.top - xlat[1] * self.options.yoffset
        y2 = bbox.bottom
        line.set('d', 'M %f %f V %f' % (x, y1, y2))
        return line

    def effect(self):
        scale = self.svg.unittouu('1px')  # convert to document units
        self.options.xoffset *= scale
        self.options.yoffset *= scale

        if not self.svg.selected:
            raise inkex.AbortExtension("Please select an object")
        if self.options.type == "geometric":
            bbox = self.svg.selection.bounding_box()
        else:
            bbox = self.svg.selection.first().bounding_box()

        layer = self.svg.get_current_layer()

        # remove adding markers 
        # self.add_marker('Arrow1Lstart', False)
        # self.add_marker('Arrow1Lend', True)

        group = Group()
        layer.append(group)
        group.set('fill', 'none')
        group.set('stroke', 'black')

        line = self.horz_line(bbox.top, [0, 1], bbox)
        # line.set('marker-start', 'url(#Arrow1Lstart)')
        # line.set('marker-end', 'url(#Arrow1Lend)')
        # line.set('stroke-width', str(scale))
        layer.append(line)

        ## Modify here 
        style = 'fill:none;stroke:#000000;stroke-width:0.264583px;' + \
            'stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1'
        st = Style(style)  # style of selected path
        line.style = st


        L = self.svg.unittouu('15px')
        A = 30
        start_type = 'both'
        style_type = 'sharp'
        style_ratio = 0.0 if style_type == 'normal' else .25

        arrow = Arrow(L, A, start_type, style_ratio, st)
        newpath = NewPath(line, arrow)

        newpath.new_arrow(layer)
        newpath.new_pathelem()
        ## Modify end

        # group.append(line)


        line = self.vert_line(bbox.left, [0, 2], bbox)
        line.set('stroke-width', str(0.5 * scale))
        group.append(line)

        line = self.vert_line(bbox.right, [0, 2], bbox)
        line.set('stroke-width', str(0.5 * scale))
        group.append(line)

        ## modify here 
        line = self.vert_line(bbox.left, [1, 0], bbox)
        # line.set('marker-start', 'url(#Arrow1Lstart)')
        # line.set('marker-end', 'url(#Arrow1Lend)')
        # line.set('stroke-width', str(scale))
        # group.append(line)
        line.style = st
        layer.append(line)

        arrow = Arrow(L, A, start_type, style_ratio, st)
        newpath = NewPath(line, arrow)

        newpath.new_arrow(layer)
        newpath.new_pathelem()
        ## End modification



        line = self.horz_line(bbox.top, [2, 0], bbox)
        line.set('stroke-width', str(0.5 * scale))
        group.append(line)

        line = self.horz_line(bbox.bottom, [2, 0], bbox)
        line.set('stroke-width', str(0.5 * scale))
        group.append(line)

        ## I do not like this, comment out
        # for node in self.svg.selected.values():
        #     group.append(node)

        layer.append(group)
        return None


if __name__ == '__main__':
    Dimension().run()

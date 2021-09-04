import inkex
from inkex import Style, TextElement, PathElement, Vector2d

import math

from draw_arrowhead import Arrow
from draw_arrowhead import NewPath

# manually editing the drawing after extension run

class ArrowHeadAngle(inkex.EffectExtension):

    def create_path(self, point1, point2):
        name = 'arrowhead'
        elem = PathElement()
        elem.update(**{
            'style': self.st,
            'inkscape:label': name,
            'd': 'M ' + str(point1.x) + ',' + str(point1.y) +
                ' L ' + str(point2.x) + ',' + str(point2.y)
                 })
        return elem

    def add_text(self, x, y, text):
        """Add a text label at the given location"""
        elem = TextElement()
        elem.text = str(text)
        elem.style = {
            'font-size': self.svg.unittouu('18pt'),
            'fill-opacity': '1.0',
            'stroke': 'none',
            'font-weight': 'normal',
            'font-style': 'normal' }
        elem.update(x=str(x), y=str(y))
        return elem

    def effect(self):

        style = 'fill:none;stroke:#000000;stroke-width:0.264583px;' + \
        'stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1'

        self.st = Style(style)  # style of selected path

        layer = self.svg.get_current_layer()
        L = self.svg.unittouu('30px')
        start_type = 'end'
        style_type = 'normal'
        style_ratio = 0.0 if style_type == 'normal' else .25

        y = 30

        def float_range(start, stop, step):
            while start < stop:
                yield float(start)
                start += step

        for A in float_range(15.0, 51, 2.5):
            pt1 = Vector2d(20, y)  ##  y + 15
            pt2 = Vector2d(80, y) 
            el = self.create_path(pt1, pt2)

            layer.add(el)
            # A = 30

            arrow = Arrow(L, A, start_type, style_ratio, self.st)
            newpath = NewPath(el, arrow)

            newpath.new_arrow(layer)
            newpath.new_pathelem()

            textel = self.add_text(85, y + 2, str(A) + ' degrees')
            layer.add(textel)
            y = y + 15

  
if __name__ == '__main__':
    ArrowHeadAngle().run()

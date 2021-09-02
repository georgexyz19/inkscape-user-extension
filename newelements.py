import inkex
from inkex import Line, Polyline, Polygon, Rectangle, Circle,\
    Ellipse, PathElement
from inkex import TextElement


class NewElement(inkex.EffectExtension):

    def effect(self):
        self.style = {'fill' : 'none', 'stroke' : '#000000', 
            'stroke-width' : '0.264583'}
        self.text_template = \
            'font-size:%dpx;text-align:center;text-anchor:middle;'
        layer = self.svg.get_current_layer()
        layer.add(*self.add_line(), *self.add_rect())
        layer.add(self.add_circle(), self.add_ellipse(), 
            self.add_polygon(), self.add_path())
        layer.add(*self.add_coordinates())

    def add_line(self):
        """Add a line"""

        el1 = Line()
        el1.set('x1', '10')
        el1.set('y1', '10')
        el1.set('x2', '40')
        el1.set('y2', '40')
        el1.set('style', self.style)

        el2 = Line.new(start=(40, 10), end=(10, 40))
        el2.style = self.style
        
        el3 = Line()
        el3.update(**{
            'x1': '50', 
            'y1': '10', 
            'x2': '80', 
            'y2': '40',
            'style': self.style
        })

        el4 = Line(x1='50', y1='40', x2='80', y2='10')
        el4.style = self.style

        return el1, el2, el3, el4

    def add_rect(self):

        el1 = Rectangle(x='10', y='60', width='30', height='20')
        el1.style = self.style

        el2 = Rectangle.new(50, 60, 30, 20)
        el2.style = self.style 
        return el1, el2

    def add_circle(self):
        el = Circle.new(center=(105, 25), radius=15)
        el.style = self.style
        return el

    def add_ellipse(self):
        el = Ellipse.new(center=(105, 70), radius=(15,10))
        el.style = self.style
        return el

    def add_polygon(self):
        el = Polygon()
        el.set('points', 
            '130,10 160,10 160,25 145,25 145,40 130,40')
        el.style = self.style
        return el 

    def add_path(self):
        el = PathElement()
        el.set('d', 'M 130,60 h30 v10 h-15 v10 h-15 z')
        el.style = self.style
        return el

    def add_text(self, x, y, position='top', font_size=3.88):
        text = TextElement()
        x0, y0 = x, y
        # adjust y position
        if position == 'top':
            y = y - 2
        elif position == 'bottom':
            y = y + 4
        else:
            y = y 
        text.set('x', x)
        text.set('y', y)
        text.set('style', self.text_template % font_size)
        text.set('xml:space', 'preserve')
        text.text = f'({x0},{y0})'
        return text
    
    def add_coordinates(self):
        coordinates = [ (10, 10), (40, 40, 'bottom'), 
                        (40, 10), (10, 40, 'bottom'),
                        (50, 10), (80, 40, 'bottom'), 
                        (50, 40, 'bottom'), (80, 10, 'top'),
                        (105, 25, 'top'), (105, 70, 'top'), 
                        (10, 60, 'top'), (50, 60, 'top'), 
                        (130, 10, 'top'), (130, 60, 'top'),
                        (160, 10, 'top'), (160, 60, 'top'),
                    ]

        text_elements = [self.add_text(*c) for c in coordinates]
        circle_elements = [self.generate_circle(c[0], c[1]) \
            for c in coordinates]
        return text_elements + circle_elements

    def generate_circle(self, x, y, r=0.66145):
        circle_style = 'fill:#000000;stroke:none;stroke-width:0.264583'
        el = Circle.new(center=(x, y), radius=r)
        el.style = circle_style
        return el


if __name__ == '__main__':
    NewElement().run()

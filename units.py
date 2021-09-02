import inkex
from inkex import Line, TextElement
import logging

class Units(inkex.GenerateExtension):
    container_label = 'lines'
    container_layer = True

    def add_arguments(self, pars):
        pars.add_argument('--name', type=str, default='Placeholder',
            dest='name', help="name input")

    def generate(self):
        sw = '1px'
        sw = self.svg.unittouu(sw)
        logging.debug(f'sw is {sw}')
        self.style = {'fill' : 'none', 'stroke' : '#000000', 
            'stroke-width' : sw}
        lines = self.add_lines()
        text = self.add_text(self.svg.unittouu('10pt'),self.svg.unittouu('50pt'), 'Hello Inkscape')
        for l in lines:
            yield l
        yield text

    def add_lines(self):
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

    def add_text(self, x, y, text):
        """Add a text label at the given location"""
        elem = TextElement()
        elem.text = str(text)
        elem.style = {
            'font-size': self.svg.unittouu('10pt'),
            'fill-opacity': '1.0',
            'stroke': 'none',
            'font-weight': 'normal',
            'font-style': 'normal' }
        elem.update(x=str(x), y=str(y))
        return elem


if __name__ == '__main__':
    Units().run()

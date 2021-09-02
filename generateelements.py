import inkex
from inkex import Line

class NewElement(inkex.GenerateExtension):
    container_label = 'lines'
    container_layer = True

    def generate(self):
        self.style = {'fill' : 'none', 'stroke' : '#000000', 
            'stroke-width' : '0.264583'}
        lines = self.add_lines()
        for l in lines:
            yield l

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


if __name__ == '__main__':
    NewElement().run()

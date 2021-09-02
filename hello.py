import inkex
from inkex import TextElement

class Hello(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument('--name', type=str, default='Inkscape',
            dest='name', help="name input")

    def effect(self):
        name = 'Hello ' + self.options.name 
        layer = self.svg.get_current_layer()
        x = self.svg.unittouu('40px')
        y = x
        layer.add(self.add_text(x, y, name))
        # self.debug('...end of effect method')

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

if __name__ == '__main__':
    Hello().run()

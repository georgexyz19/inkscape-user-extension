import inkex
from inkex import Rectangle, Transform 

class NewElement(inkex.GenerateExtension):
    container_label = 'transform'
    container_layer = True

    def generate(self):
        self.style = {'fill' : 'none', 'stroke' : '#000000', 
            'stroke-width' : self.svg.unittouu('1px')}
        rects = self.add_rect()
        for r in rects:
            yield r

    def add_rect(self):

        el1 = Rectangle(x='10', y='10', width='60', height='40')
        el1.style = self.style

        el2 = Rectangle.new(20, 20, 60, 40)
        el2.style = self.style 
        tr = Transform('rotate(30)')
        el2.transform = tr

        el3 = Rectangle.new(20, 20, 60, 40)
        el3.style = self.style 
        tr = Transform('rotate(30, 50, 40)')
        el3.transform = tr

        el4 = Rectangle.new(20, 20, 60, 40)
        el4.style = self.style 
        tr = Transform('translate(10, 10) rotate(45)')
        el4.transform = tr

        el5 = Rectangle.new(20, 20, 60, 40)
        el5.style = self.style 
        tr = Transform('scale(2.0) rotate(60)')
        el5.transform = tr

        el6 = Rectangle.new(20, 20, 60, 40)
        el6.style = self.style 
        tr = Transform('rotate(60)') * Transform('scale(2.0)')
        el6.transform = tr

        return el1, el2, el3, el4, el5, el6


if __name__ == '__main__':
    NewElement().run()

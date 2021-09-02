
import math

from inkex import GenerateExtension
from inkex import Polygon
from inkex import Vector2d, DirectedLineSegment


def draw_rect(v1, v2, v3, v4, style):
    elem = Polygon()
    elem.style = style
    elem.set('points', f'{v1.x},{v1.y} ' +
                f'{v2.x},{v2.y} ' +
                f'{v3.x},{v3.y} ' +
                f'{v4.x},{v4.y}')
    return elem


def draw_star(center, R, style):

    RAD = math.radians
    (A, B, C, D, E)  = (Vector2d.from_polar(R, RAD(-90 + 360/5 * i)) \
            for i in range(5) )  

    def intersection(A1, A2, B1, B2):
        A12 = DirectedLineSegment(A1, A2)
        B12 = DirectedLineSegment(B1, B2)
        return A12.intersect(B12)

    lines = [(A, C, B, E), (A, C, B, D), (C, E, B, D), (A, D, C, E), \
                (A, D, B, E)]
    P = [intersection(*p) for p in lines]

    PP = [A, P[0], B, P[1], C, P[2], D, P[3], E, P[4]] 
    points_str = ' '.join([f'{(p+center).x},{(p+center).y}' for p in PP])

    elem = Polygon()
    elem.style = style
    elem.set('points', points_str)
    return elem


def draw_stripes(origin, A, B, C, D, L, style):
    blue = '#002868'
    red = '#BF0A30'
    elems = []
    rect = [origin, origin + (B, 0), origin + (B, A), \
                origin + (0, A) ]
    elem =draw_rect(*rect, style)
    elems.append(elem)

    st1 = style.copy()
    st1.update({'fill': red, 'stroke': 'none'})
    for i in range(7):
        rect = [origin + (D, 0), origin + (B, 0), origin + (B, L), \
                    origin + (D, L)]
        rect_move = [ p + (0, 2 * L * i) for p in rect ]
        if i >= 4:
            rect_move[0] -= (D, 0)
            rect_move[3] -= (D, 0)
            
        elem = draw_rect(*rect_move, st1)
        elems.append(elem)

    st2 = style.copy()
    st2.update({'fill': blue, 'stroke': 'none'})
    rect = [origin, origin + (D, 0), origin + (D, C), \
                origin + (0, C)]
    elem = draw_rect(*rect, st2)
    elems.append(elem)

    return elems


def draw_stars(origin, E, H, K, style):
    white = '#ffffff'
    st1 = style.copy()
    st1.update({'fill': white, 'stroke': 'none'})

    R = K / 2.0 / math.cos(math.radians(18))

    elems = []
    for j in range(5):
        for i in range(6):
            elem = draw_star(origin + (H + 2 * H * i, E + 2 * E * j), 
                R, st1)
            elems.append(elem)
    for j in range(4):
        for i in range(5):
            elem = draw_star(origin + (2 * H * (i + 1), 2 * E * (j + 1)), 
                R, st1)
            elems.append(elem)

    return elems


class DrawFlag(GenerateExtension):
    container_label = 'star'
    container_layer = True

    def generate(self):
        style = {'fill' : 'none', 'stroke' : '#000000', 
            'stroke-width' : '0.264583', 'stroke-linejoin' : 'round'}

        A = 100
        B = 1.9 * A
        C = 7/13 * A
        D = 0.76 * A
        E = 0.054 * A
        F = E
        G = 0.063 * A
        H = G
        K = 0.0616 * A
        # The diameter of a polygon is the largest distance between any pair 
        #  of vertices. In other words, it is the length of the longest polygon 
        #  diagonal (e.g., straight line segment joining two vertices).
        # K is diameter
        # Diameter = R * sqrt( (5 + sqrt(5))/2 ) = 2 * R * cos 18 (degree) wikipedia
        L = 1/13 * A

        elems1 = draw_stripes(Vector2d(0, 0), A, B, C, D, L, style)
        elems2 = draw_stars(Vector2d(0, 0), E, H, K, style)

        lst = elems1 + elems2
        for l in lst:
            yield l     


if __name__ == '__main__':
    DrawFlag().run()

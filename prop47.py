# inkscape extension to draw picture proof of Euclid's Elements Theorem I.47

import math

from inkex import GenerateExtension
from inkex import Line, Polygon, Rectangle, Transform
from inkex import Vector2d


def draw_triangle(v1, v2, v3, style):
    elem = Polygon()
    elem.style = style
    elem.set('points', f'{v1.x},{v1.y} ' +
                f'{v2.x},{v2.y} ' +
                f'{v3.x},{v3.y}')
    return elem


def draw_rect(v1, v2, v3, v4, style):
    elem = Polygon()
    elem.style = style
    elem.set('points', f'{v1.x},{v1.y} ' +
                f'{v2.x},{v2.y} ' +
                f'{v3.x},{v3.y} ' +
                f'{v4.x},{v4.y}')
    return elem


def draw_line(v1, v2, style):
    elem = Line.new(start=v1, end=v2)
    elem.style = style
    return elem


def draw_grid(width, height, style):
    # width and height in mm
    wi = math.floor(width) // 10 * 10
    he = math.floor(height) // 10 * 10

    elems = []
    for w in range(0, wi + 10, 10):
        v1 = Vector2d(w, 0)
        v2 = Vector2d(w, he)
        elem = draw_line(v1, v2, style)
        elems.append(elem)

    for h in range(0, he + 10, 10):
        v1 = Vector2d(0, h)
        v2 = Vector2d(wi, h)
        elem = draw_line(v1, v2, style)
        elems.append(elem)
    return elems


def calc_vecs(origin, length, alpha):
    A = origin
    B = A + Vector2d(length, 0)
    side_c = length
    ALPHA = math.radians(alpha)
    side_b = side_c * math.sin(ALPHA)
    side_a = side_c * math.cos(ALPHA)
    C = A + Vector2d(side_b * math.sin(ALPHA), 
                -1 * side_b * math.cos(ALPHA))

    D = B + Vector2d(0, side_c)
    E = A + Vector2d(0, side_c)

    F = C + (C - B) / side_a * side_b
    G = A + (C - B) / side_a * side_b

    H = B + (C - A) / side_b * side_a
    I = C + (C - A) / side_b * side_a

    J = C + Vector2d(0, side_b * math.cos(ALPHA) + side_c)
    return (A, B, C, D, E, F, G, H, I, J, side_a, side_b, side_c)


def dash_style(style):
    st = style.copy()
    st.update({'stroke': '#808080', 'stroke-miterlimit': '4', \
            'stroke-dashoffset': '0', 'stroke-dasharray': '0.79,0.79'})
    return st
    

def draw_base(origin, length, alpha, style):
    (A, B, C, D, E, F, G, H, I, J, side_a, side_b, side_c) = \
        calc_vecs(origin, length, alpha)
    
    tri = draw_triangle(A, B, C, style)

    angle_len = 1/6 * side_b
    C1 = C + (A - C)/side_b * angle_len
    C2 = C1 + (B - C)/side_a * angle_len
    C3 = C2 + (C - A)/side_b * angle_len
    line1 = draw_line(C1, C2, style)
    line2 = draw_line(C2, C3, style) 

    rect_c = draw_rect(A, B, D, E, style)

    rect_b = draw_rect(A, C, F, G, style)

    rect_a = draw_rect(C, B, H, I, style)

    st1 = dash_style(style)
    line = draw_line(C, J, st1)

    return [tri, line1, line2, rect_c, rect_b, rect_a, line]

    
def draw_figure(origin, length, alpha, ht, vm, style):
    # ht is height ratio, first - 0, second - 1/2, third - 1
    # vm is vertial move, first 3 - 0, 4th - 1/2 * side_c 5th - side_c
    # for the first 5 ones
    (A, B, C, D, E, F, G, H, I, J, side_a, side_b, side_c) = \
        calc_vecs(origin, length, alpha)

    elems = draw_base(origin, length, alpha, style)

    if vm > 0:
        st3 = dash_style(style)
        H = F + (I - C)
        line1 = draw_line(F, H, st3)
        line2 = draw_line(H, I, st3)
        elems.extend([line1, line2])

    st1 = style.copy()
    st1.update({'fill': '#a02c2c'})
    ALPHA = math.radians(alpha)
    J1 = J + Vector2d(0, -1 * side_c)
    J2 = J + Vector2d(0, -1 * side_a * math.sin(ALPHA) * ht)
    J3 = J1 + Vector2d(0, -1 * side_a * math.sin(ALPHA) * ht)

    V = Vector2d(0, -1 * side_c * vm )
    rect_left = draw_rect(A+V, E+V, J2+V, J3+V, st1)
    
    st2 = style.copy()
    st2.update({'fill': '#e6e6e6'})
    rect_right = draw_rect(B+V, D+V, J2+V, J3+V, st2)
    elems.extend([rect_left, rect_right])
    return elems


def draw_sixth(origin, length, alpha, style):
    (A, B, C, D, E, F, G, H, I, J, side_a, side_b, side_c) = \
        calc_vecs(origin, length, alpha)

    elems = draw_base(origin, length, alpha, style)

    st1 = style.copy()
    st1.update({'fill': '#a02c2c'})
    ALPHA = math.radians(alpha)
    G1 = G + (F - G) / 2
    F1 = F + (F - G) / 2
    rect_left = draw_rect(A, C, F1, G1, st1)
    
    st2 = style.copy()
    st2.update({'fill': '#e6e6e6'})
    H1 = H + (I - H) / 2
    I1 = I + (I - H) / 2
    rect_right = draw_rect(B, C, I1, H1, st2)

    st3 = dash_style(style)

    H = F + (I - C)
    line1 = draw_line(F, H, st3)
    line2 = draw_line(H, I, st3)

    elems.extend([line1, line2, rect_left, rect_right])
    return elems


def draw_seventh(origin, length, alpha, style):
    (A, B, C, D, E, F, G, H, I, J, side_a, side_b, side_c) = \
        calc_vecs(origin, length, alpha)

    elems = draw_base(origin, length, alpha, style)

    st1 = style.copy()
    st1.update({'fill': '#a02c2c'})
    rect_left = draw_rect(A, C, F, G, st1)
    
    st2 = style.copy()
    st2.update({'fill': '#e6e6e6'})
    rect_right = draw_rect(B, C, I, H, st2)

    st3 = dash_style(style)
    H = F + (I - C)
    line1 = draw_line(F, H, st3)
    line2 = draw_line(H, I, st3)

    elems.extend([line1, line2, rect_left, rect_right])
    return elems


def draw_last(origin, length, alpha, style):
    (A, B, C, D, E, F, G, H, I, J, side_a, side_b, side_c) = \
        calc_vecs(origin, length, alpha)

    elems = draw_base(origin, length, alpha, style)

    st1 = style.copy()
    st1.update({'fill': '#a02c2c'})
    rect_left = draw_rect(A, C, F, G, st1)
    J1 = J + Vector2d(0, -1 * side_c)
    rect_left1 = draw_rect(A, E, J, J1, st1)
    
    st2 = style.copy()
    st2.update({'fill': '#e6e6e6'})
    rect_right = draw_rect(B, C, I, H, st2)
    rect_right2 = draw_rect(B, D, J, J1, st2)

    st3 = dash_style(style)

    H = F + (I - C)
    line1 = draw_line(F, H, st3)
    line2 = draw_line(H, I, st3)

    elems.extend([line1, line2, rect_left, rect_left1, \
        rect_right, rect_right2])
    return elems


class Prop47(GenerateExtension):
    container_label = 'prop47'
    container_layer = True

    def generate(self):
        style = {'fill' : 'none', 'stroke' : '#000000', 
            'stroke-width' : '0.264583', 'stroke-linejoin' : 'round'}

        origin = Vector2d(30, 50)
        length = 25
        alpha = 30

        viewbox = self.svg.get_viewbox()
        st1 = style.copy()
        st1.update({'stroke': '#b3b3b3'})
        grids = draw_grid(viewbox[2], viewbox[3], st1)

        lst = draw_figure(origin, length, alpha, 0, 0, style)

        origin = Vector2d(100, 50)
        lst += draw_figure(origin, length, alpha, 1/2, 0, style)

        origin = Vector2d(170, 50)
        lst += draw_figure(origin, length, alpha, 1, 0, style)

        origin = Vector2d(30, 130)
        lst += draw_figure(origin, length, alpha, 1, 1/2, style)

        origin = Vector2d(100, 130)
        lst += draw_figure(origin, length, alpha, 1, 1, style)

        origin = Vector2d(170, 130)
        lst += draw_sixth(origin, length, alpha, style)

        origin = Vector2d(65, 200)
        lst += draw_seventh(origin, length, alpha, style)

        origin = Vector2d(135, 200)
        lst += draw_last(origin, length, alpha, style)

        lst = grids + lst 
        for l in lst:
            yield l     


if __name__ == '__main__':
    Prop47().run()

import random
from string import ascii_uppercase

from manim import *
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

import directed_graphs as dg
from visual_config import add_background_rectangle

COIN_RADIUS = 0.4
NUM_STATES = 7
MARGIN = 0.8
SPACE_BETWEEN_COINS = 0.15

def get_coin_label(face, coin):
    label_mobj = Text(face).move_to(coin).scale(coin.radius * 2)
    label_mobj.set_z_index(2)
    return label_mobj


# TODO this is slightly different from how I created drop shadows
# in other scenes and I might want to change those other scenes
# to be more like this
def create_drop_shadow(mobj):
    mobj.set_z_index(1)
    shadow = mobj.copy()
    shadow.set_z_index(0)
    shadow.fill_color = dg.STROKE_COLOR
    shadow.stroke_color = dg.STROKE_COLOR
    shadow.shift(dg.DROP_SHADOW_THICKNESS * DOWN)
    shadow.shift(dg.DROP_SHADOW_THICKNESS * RIGHT)
    return shadow


def create_coin(face):
    coin = Dot(radius=COIN_RADIUS,
               stroke_width=dg.VERTEX_STROKE_WIDTH,
               color=dg.STROKE_COLOR,
               fill_color=dg.FILL_COLOR)
    return VGroup(coin, 
                  get_coin_label(face, coin), 
                  create_drop_shadow(coin))


def coin_coords():
    width_of_side = COIN_RADIUS * 2 + SPACE_BETWEEN_COINS
    t = Triangle()
    t.scale(width_of_side / t.width)
    
    coords = []
    for vertex in t.get_vertices():
        coords.append(vertex)#vertex.get_center())

    return coords


# faces: a list of three characters
def create_coin_cluster(faces):
    coords = coin_coords()
    cluster = VGroup()
    
    for i in range(0, 3):
        cluster.add(create_coin(faces[i]).move_to(coords[i]))

    return cluster


def create_less_than_sign(cluster1, cluster2):
    x_coord = (cluster1.get_center()[0] + cluster2.get_center()[0]) / 2
    y_coord = cluster1.get_center()[1]
    point = Point(location=[x_coord, y_coord, 0])
    # TODO decide on bolding and size
    return MathTex(r"\boldsymbol{\prec_{C}}") \
            .move_to(point).scale(COIN_RADIUS * 2)


def create_equals_sign(cluster1, cluster2):
    x_coord = cluster1.get_center()[0]
    y_coord = (cluster1.get_center()[1] + cluster2.get_center()[1]) / 2
    point = Point(location=[x_coord, y_coord, 0])
    # TODO decide on bolding and size
    return MathTex(r"\boldsymbol{\sim_{C}}") \
            .move_to(point).scale(COIN_RADIUS * 2)


# face_clusters: a list of three lists of three characters
def create_section(face_clusters):
    c1 = create_coin_cluster(face_clusters[0])
    c1.align_on_border(UP, buff=MARGIN)
    
    c2 = create_coin_cluster(face_clusters[1])

    c3 = create_coin_cluster(face_clusters[2])
    c3.align_on_border(DOWN, buff=MARGIN)
    
    return VGroup(c1, 
                  c2, 
                  c3, 
                  create_equals_sign(c1, c2),
                  create_equals_sign(c2, c3))


class HeadsTails(Scene):
    def construct(self):
        add_background_rectangle(self, config)

        # TODO standardize text size across images
        # TODO delete this code when I decide for sure I'm not using it
        lo_label = Text("Less optimized").scale(1.6 * COIN_RADIUS)
        lo_label.align_on_border(LEFT, buff=MARGIN)
        lo_label.align_on_border(DOWN, buff=MARGIN)
        lo_arrow = Arrow(stroke_width=dg.ARROW_STROKE_WIDTH, 
                         start=RIGHT,
                         end=LEFT,
                         max_tip_length_to_length_ratio=0.16)
        lo_arrow.width = lo_label.width * 2/3
        lo_arrow.next_to(lo_label, UP)
        lo_arrow.align_on_border(LEFT, buff=MARGIN)
        # self.add(lo_label, lo_arrow)

        mo_label = Text("More optimized").scale(1.6 * COIN_RADIUS)
        mo_label.align_on_border(RIGHT, buff=MARGIN)
        mo_label.align_on_border(DOWN, buff=MARGIN)
        mo_arrow = Arrow(stroke_width=dg.ARROW_STROKE_WIDTH, 
                         start=LEFT,
                         end=RIGHT,
                         max_tip_length_to_length_ratio=0.16)
        mo_arrow.width = mo_label.width * 2/3
        mo_arrow.next_to(mo_label, UP)
        mo_arrow.align_on_border(RIGHT, buff=MARGIN)
        # self.add(mo_label, mo_arrow)

        # Add all the triangle coins
        s1 = create_coin_cluster(['T', 'T', 'T'])
        s1.move_to([0, 0, 0])
        s1.align_on_border(LEFT, buff=MARGIN)

        s4 = create_coin_cluster(['H', 'H', 'H'])
        s4.move_to([0, 0, 0])
        s4.align_on_border(RIGHT, buff=MARGIN)

        width = s4.get_center()[0] - s1.get_center()[0]
        left_side = s1.get_center()[0]

        s2 = create_section([['H', 'T', 'T'], 
                             ['T', 'H', 'T'],
                             ['T', 'T', 'H']])
        s2.move_to([left_side + width / 3 * 1, 0, 0])

        s3 = create_section([['H', 'H', 'T'], 
                             ['T', 'H', 'H'], 
                             ['H', 'T', 'H']])
        s3.move_to([left_side + width / 3 * 2, 0, 0])

        lt1 = create_less_than_sign(s1, s2)
        lt2 = create_less_than_sign(s2, s3)
        lt3 = create_less_than_sign(s3, s4)

        self.add(s1, s2, s3, s4, lt1, lt2, lt3)


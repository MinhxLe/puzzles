from polygon_old import (
    Utils,
)
import math


class TestUtils:
    def test_get_num_edges_triangle(self):
        # triangle
        assert Utils(3).get_num_edges(0, 0) == 0
        assert Utils(3).get_num_edges(0, 1) == 1
        assert Utils(3).get_num_edges(0, 2) == 1
        assert Utils(3).get_num_edges(1, 2) == 1

    def test_get_num_edges_offset(self):
        assert Utils(10).get_num_edges(3, 6) == 3

    def test_get_num_edges_ordering(self):
        assert Utils(10).get_num_edges(6, 3) == 3

    def test_get_num_edges_other_direction(self):
        assert Utils(10).get_num_edges(0, 7) == 3

    def test_get_distance_square(self):
        square = Utils(4)
        assert math.isclose(square.get_distance(0, 1), 1)
        assert math.isclose(square.get_distance(0, 2), math.sqrt(2))
        assert math.isclose(square.get_distance(0, 3), 1)
        assert math.isclose(square.get_distance(1, 1), 0)

    def test_get_distance_hexagon(self):
        hexagon = Utils(6)
        assert math.isclose(hexagon.get_distance(0, 1), 1)
        R = (2 * math.sin(math.pi / 6)) ** -1
        assert math.isclose(
            hexagon.get_distance(0, 2),
            math.sqrt(2 * R**2 - 2 * R**2 * math.cos(2 * math.pi / 3)),
        )
        assert math.isclose(hexagon.get_distance(0, 3), 2 * R)

    def test_get_triangle_area_square(self):
        square = Utils(4)
        assert math.isclose(square.get_triangle_area([0, 1, 2]), 0.5)
        assert math.isclose(square.get_triangle_area([0, 1, 1]), 0)

    def test_get_triangle_area_hexagon(self):
        hexagon = Utils(6)
        assert math.isclose(hexagon.get_triangle_area([0, 2, 2]), 0)

        # area of hexagon / 2
        assert math.isclose(hexagon.get_triangle_area([0, 2, 4]), 3 * math.sqrt(3) / 4)

        assert math.isclose(hexagon.get_triangle_area([0, 3, 4]), math.sqrt(3) / 2)


# def test_find_max_triangle_count_octogon():
#     poly = PolygonProblem(8)
#     assert poly.find_max_triangle_count([0, 2, 4]) == 4
#     assert poly.find_max_triangle_count([0, 2, 5]) == 4
#
#
# def test_find_all_max_triangle_count_square():
#     square = PolygonProblem(4)
#     counter = square.find_all_max_triangle_count()
#     assert sum(c.values()) == 0
#
#
# def test_find_all_max_triangle_count_hexagon():
#     hex = PolygonProblem(6)
#     counter = hex.find_all_max_triangle_count()
#     assert sum(c.values()) == 1
#
#
# def test_find_all_max_triangle_count_pentagon():
#     poly = PolygonProblem(5)
#     counter = poly.find_all_max_triangle_count()
#     for triangle, count in c.items():
#         if count > 0:
#             print(f"{triangle} {count}")
#     assert sum(c.values()) == 3
#
#
# def test_find_all_max_triangle_count_big():
#     poly = PolygonProblem(444)
#     counter = poly.find_all_max_triangle_count()
#     for triangle, count in c.items():
#         if count > 0:
#             print(f"{triangle} {count}")
#     assert sum(c.values()) == 3

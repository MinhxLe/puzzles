from polygon import PolygonProblem, partition_polygon
import math


def test_get_num_edges_triangle():
    # triangle
    assert PolygonProblem(3).get_num_edges(0, 0) == 0
    assert PolygonProblem(3).get_num_edges(0, 1) == 1
    assert PolygonProblem(3).get_num_edges(0, 2) == 1
    assert PolygonProblem(3).get_num_edges(1, 2) == 1


def test_get_num_edges_offset():
    assert PolygonProblem(10).get_num_edges(3, 6) == 3


def test_get_num_edges_ordering():
    assert PolygonProblem(10).get_num_edges(6, 3) == 3


def test_get_num_edges_other_direction():
    assert PolygonProblem(10).get_num_edges(0, 7) == 3


def test_get_distance_square():
    square = PolygonProblem(4)
    assert math.isclose(square.get_distance(0, 1), 1)
    assert math.isclose(square.get_distance(0, 2), math.sqrt(2))
    assert math.isclose(square.get_distance(0, 3), 1)
    assert math.isclose(square.get_distance(1, 1), 0)


def test_get_distance_hexagon():
    hexagon = PolygonProblem(6)
    assert math.isclose(hexagon.get_distance(0, 1), 1)
    R = (2 * math.sin(math.pi / 6)) ** -1
    assert math.isclose(
        hexagon.get_distance(0, 2),
        math.sqrt(2 * R**2 - 2 * R**2 * math.cos(2 * math.pi / 3)),
    )
    assert math.isclose(hexagon.get_distance(0, 3), 2 * R)


def test_get_area_square():
    square = PolygonProblem(4)
    assert math.isclose(square.get_area([0, 1, 2]), 0.5)
    assert math.isclose(square.get_area([0, 1, 1]), 0)


def test_get_area_hexagon():
    hexagon = PolygonProblem(6)
    assert math.isclose(hexagon.get_area([0, 2, 2]), 0)

    # area of hexagon / 2
    assert math.isclose(hexagon.get_area([0, 2, 4]), 3 * math.sqrt(3) / 4)

    assert math.isclose(hexagon.get_area([0, 3, 4]), math.sqrt(3) / 2)


def test_partition_polygon():
    assert partition_polygon([0, 1], list(range(4))) == [[0, 1], [0, 1, 2, 3]]
    assert partition_polygon([0, 2], list(range(4))) == [[0, 1, 2], [0, 2, 3]]
    assert partition_polygon([0, 3], list(range(4))) == [[0, 1, 2, 3], [0, 3]]

    assert partition_polygon([0, 2, 4], list(range(6))) == [
        [0, 1, 2],
        [2, 3, 4],
        [0, 4, 5],
    ]

    assert partition_polygon([0, 1, 4], list(range(6))) == [
        [0, 1],
        [1, 2, 3, 4],
        [0, 4, 5],
    ]

    assert partition_polygon([0, 1], [0, 2, 4, 5]) == [[0, 2], [0, 2, 4, 5]]

    assert partition_polygon([1, 4], [4, 5, 6, 7, 8, 9]) == [[5, 6, 7, 8], [4, 5, 8, 9]]


def test_find_max_triangle_count_octogon():
    poly = PolygonProblem(8)
    assert poly.find_max_triangle_count([0, 2, 4]) == 4
    assert poly.find_max_triangle_count([0, 2, 5]) == 4


def test_find_all_max_triangle_count_square():
    square = PolygonProblem(4)
    counter = square.find_all_max_triangle_count()
    assert sum(counter.values()) == 0


def test_find_all_max_triangle_count_hexagon():
    hex = PolygonProblem(6)
    counter = hex.find_all_max_triangle_count()
    assert sum(counter.values()) == 1


def test_find_all_max_triangle_count_pentagon():
    poly = PolygonProblem(5)
    counter = poly.find_all_max_triangle_count()
    for triangle, count in counter.items():
        if count > 0:
            print(f"{triangle} {count}")
    assert sum(counter.values()) == 3


def test_find_all_max_triangle_count_big():
    poly = PolygonProblem(444)
    counter = poly.find_all_max_triangle_count()
    for triangle, count in counter.items():
        if count > 0:
            print(f"{triangle} {count}")
    assert sum(counter.values()) == 3

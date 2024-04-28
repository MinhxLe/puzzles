import pytest
import random
from polygon import (
    Polygon,
    MaxTriangleCounter,
    NPolygon,
    PolygonCache,
)


def P(vertices: Polygon, N: int):
    return Polygon(vertices, NPolygon(N))


def random_polygon(num_vertices=None, N: int = random.randint(3, 444)):
    num_vertices = num_vertices or random.randint(3, N)
    vertices = random.sample(range(0, N), num_vertices)
    return P(vertices, N)


class TestMaxTriangleCounter:
    """
    hand validated tests for sanity checking my code
    """

    def MTC(self, n: int, use_cache=True):
        return MaxTriangleCounter(NPolygon(n), use_cache)

    def test_get_max_triangle_count_4(self):
        c = self.MTC(4)
        assert c.get_max_triangle_count(P([0, 1, 2], 4)) == 0
        assert c.get_max_triangle_count(P([0, 2, 3], 4)) == 0
        assert c.get_max_triangle_count(P([0, 3, 1], 4)) == 0

    def test_get_max_triangle_count_5(self):
        c = self.MTC(5)
        assert c.get_max_triangle_count(P([0, 1, 2], 5)) == 0
        # isoles triangle
        assert c.get_max_triangle_count(P([0, 1, 3], 5)) == 1
        assert c.get_max_triangle_count(P([1, 4, 2], 5)) == 1

    def test_get_max_triangle_count_6(self):
        c = self.MTC(6)
        assert c.get_max_triangle_count(P([0, 1, 2], 6)) == 0
        assert c.get_max_triangle_count(P([0, 2, 3], 6)) == 0
        # equilateral triangle
        assert c.get_max_triangle_count(P([0, 2, 4], 6)) == 1
        assert c.get_max_triangle_count(P([1, 3, 5], 6)) == 1

    def test_get_max_triangle_count_8(self):
        c = self.MTC(8, False)
        assert c.get_max_triangle_count(P([0, 2, 4], 8)) == 4

    def test_get_max_triangle_count_7(self):
        c = self.MTC(7)
        assert c.get_max_triangle_count(P([0, 1, 4], 7)) == 4
        assert c.get_max_triangle_count(P([0, 3, 6], 7)) == 4

    def test_get_all_4(self):
        _, count = self.MTC(4).get_all_max_triangle_counts()
        assert count == 0

    def test_get_all_5(self):
        _, count = self.MTC(5).get_all_max_triangle_counts()
        assert count == 5

    def test_get_all_6(self):
        _, count = self.MTC(6).get_all_max_triangle_counts()
        assert count == 2

    def test_get_all_7(self):
        counter, all_count = self.MTC(7).get_all_max_triangle_counts()
        assert all_count == 42

    def test_get_all_8(self):
        _, count = self.MTC(8, False).get_all_max_triangle_counts()
        assert count == 64

    def test_get_all_10(self):
        _, count = self.MTC(10, False).get_all_max_triangle_counts()
        assert count == 1010

    def test_get_all_12(self):
        _, count = self.MTC(12, False).get_all_max_triangle_counts()
        assert count == 13316

    @pytest.mark.skip
    def test_get_all_15(self):
        _, count = self.MTC(15, False).get_all_max_triangle_counts()
        assert count == 714340


class TestPolygon:
    def test_rotate(self):
        assert P([1, 2, 4, 7], 8).rotate(2) == P([3, 4, 6, 1], 8)
        assert P([1, 2, 4, 7], 8).rotate(-2) == P([7, 0, 2, 5], 8)

    def test_flip(self):
        assert P([0, 1, 2], 8).flip() == P([0, 7, 6], 8)
        assert P([0, 1, 3], 8).flip() == P([0, 7, 5], 8)

    def test_partition(self):
        assert P([1, 2, 4, 5], 8).partition(2, 5) == [
            P([2, 4, 5], 8),
            P([2, 5, 1], 8),
        ]

        assert P([1, 2, 4, 5], 8).partition(4, 2) == [
            P([2, 4], 8),
            P([2, 5, 4, 1], 8),
        ]

    def test_partition_boundary(self):
        assert P([1, 2, 4, 5], 8).partition(1, 2) == [
            P([1, 2], 8),
            P([1, 2, 4, 5], 8),
        ]

    def test_edge_distances(self):
        assert P([0], 8).edge_distances == [8]
        assert P([1, 2], 8).edge_distances == [1, 7]
        assert P([1, 2, 4, 7], 8).edge_distances == [1, 2, 3, 2]
        assert P([4, 7, 1], 8).edge_distances == [3, 3, 2]

    def test_is_same_diff_vertices_count(self):
        assert not P([1, 2, 3], 4).is_same(P([1, 2], 4))

    def test_is_same_diff_n(self):
        assert not P([1, 2, 3], 4).is_same(P([1, 2, 3], 5))

    def test_is_same_diff_edge_distance(self):
        assert not P([0, 1], 4).is_same(P([0, 2], 4))

    def test_is_same_translation(self):
        p = random_polygon()
        assert p.is_same(p.rotate(random.randint(0, 100)))

    def test_is_same_reflection(self):
        p = random_polygon()
        assert p.is_same(p.flip())

    def test_is_same_both(self):
        p = random_polygon()
        assert p.is_same(p.rotate(random.randint(0, 100)).flip())
        assert p.is_same(p.flip().rotate(random.randint(0, 100)))

    def test_area_segment(self):
        pass

    def test_area_triangle(self):
        pass

    def test_area_whole(self):
        pass

    def test_triangle_combo(self):
        assert random_polygon(3, 10).num_triangle_combos == 1
        # assert random_polygon(4, 10).num_triangle_combos == 2
        assert random_polygon(5, 10).num_triangle_combos == 5
        assert random_polygon(6, 10).num_triangle_combos == 14


class TestNPolygon:
    def test_R(self):
        pass

    def test_get_edge_distance(self):
        pass

    def test_add_edge_distance(self):
        pass

    def test_get_distance(self):
        pass

    def test_get_triangle_area(self):
        pass


class TestPolygonCache:
    def test_rotation(self):
        cache = PolygonCache()
        p = random_polygon()
        cache[p] = 0
        assert cache[p.rotate(random.randint(0, 100))] == 0

        cache[p.rotate(random.randint(0, 100))] = 1
        assert cache[p] == 1

        with pytest.raises(KeyError):
            cache[random_polygon()]

    def test_reflection(self):
        cache = PolygonCache()
        p = random_polygon()
        cache[p] = 0
        assert cache[p.flip()] == 0

        cache[p.flip()] = 1
        assert cache[p] == 1

        with pytest.raises(KeyError):
            cache[random_polygon()]

    def test_is_in(self):
        cache = PolygonCache()
        p = random_polygon()
        cache[p] = 0

        assert p.rotate(3) in cache
        assert p.flip() in cache

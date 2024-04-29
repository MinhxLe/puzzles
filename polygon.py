from dataclasses import dataclass
import math
from functools import cached_property
from typing import Any, Counter, Optional, Tuple


@dataclass
class NPolygon:
    """
    N dimensional unit regular polygon
    """

    N: int

    def get_edge_distance(self, v1: int, v2: int) -> int:
        """
        clockwise distance on polygon between 2 vertices. Note that this
        is NOT a commutative operation.
        """
        if v2 <= v1:
            v2 += self.N
        return v2 - v1

    def add_edge_distance(self, v: int, n: int) -> int:
        if n < 0:
            n = self.N + n
        return (v + n) % self.N

    @cached_property
    def R(self) -> float:
        """
        radius of circumscribed circle of polygon
        """
        return (2 * math.sin(math.pi / self.N)) ** -1

    def get_distance(self, v1: int, v2: int) -> float:
        """
        distance of line segment connecting 2 verices
        """
        edge_distance = self.get_edge_distance(v1, v2)
        edge_distance = min(edge_distance, self.N - edge_distance)

        # interior angle between 2 vertices
        alpha = edge_distance * ((2 * math.pi) / self.N)
        # law of cosine
        return math.sqrt((2 * self.R**2) - (2 * self.R**2 * math.cos(alpha)))

    def get_triangle_area(self, vertices: list[int]) -> float:
        assert len(vertices) == 3
        assert all([n < self.N for n in vertices])
        # heron's formula
        d = [
            self.get_distance(vertices[0], vertices[1]),
            self.get_distance(vertices[0], vertices[2]),
            self.get_distance(vertices[1], vertices[2]),
        ]
        s = sum(d) / 2
        return math.sqrt(s * (s - d[0]) * (s - d[1]) * (s - d[2]))


@dataclass(frozen=True)
class Polygon:
    """
    Polygon defined by edges between set of vertices labeled by int on a N regular polygon
    """

    vertices: list[int]
    n_polygon: NPolygon

    def __post_init__(self):
        assert len(set(self.vertices)) == len(self.vertices)
        assert all([v < self.n_polygon.N for v in self.vertices])
        self.vertices.sort()

    def __hash__(self):
        return hash((tuple(self.vertices), self.n_polygon.N))

    @cached_property
    def edge_distances(self) -> list[int]:
        """
        return edge distances between every adjacent vertice in order. This should
        sum up to N.
        """
        num_vertices = len(self.vertices)
        return [
            self.n_polygon.get_edge_distance(
                self.vertices[i], self.vertices[(i + 1) % num_vertices]
            )
            for i in range(num_vertices)
        ]

    def rotate(self, n: int) -> "Polygon":
        return Polygon(
            [self.n_polygon.add_edge_distance(v, n) for v in self.vertices],
            self.n_polygon,
        )

    def flip(self) -> "Polygon":
        new_vertices = []
        for v in self.vertices:
            distance = self.n_polygon.get_edge_distance(self.vertices[0], v)
            new_vertices.append(
                self.n_polygon.add_edge_distance(self.vertices[0], -distance)
            )
        return Polygon(new_vertices, self.n_polygon)

    def partition(self, i: int, j: int) -> list["Polygon"]:
        """
        partition polygon with a segment from ith vertex to jth vertex
        """
        i_idx = self.vertices.index(i)
        j_idx = self.vertices.index(j)
        i_idx, j_idx = min(i_idx, j_idx), max(i_idx, j_idx)
        return [
            # +1 since partitioning includes the partition vertices
            Polygon(self.vertices[i_idx : j_idx + 1], self.n_polygon),
            Polygon(self.vertices[: i_idx + 1] + self.vertices[j_idx:], self.n_polygon),
        ]

    @property
    def num_triangle_combos(self) -> int:
        # all polygons are convex so this still applies
        if self.num_vertices < 3:
            return 0
        elif self.num_vertices == 3:
            return 1
        else:
            return catalan_number(self.num_vertices - 2)

    def is_same(self, that: "Polygon") -> bool:
        """
        returns whether 2 polygon are the same under translation and reflection.
        """
        if self.n_polygon != that.n_polygon:
            return False
        return same_under_rotation(
            self.edge_distances, that.edge_distances
        ) or same_under_rotation(self.edge_distances, that.flip().edge_distances)

    @cached_property
    def area(self) -> float:
        if len(self.vertices) < 3:
            return 0.0
        elif len(self.vertices) == 3:
            return self.n_polygon.get_triangle_area(self.vertices)
        else:
            p1, p2 = self.partition(self.vertices[0], self.vertices[2])
            assert len(p1.vertices) == 3
            return p1.area + p2.area

    @property
    def num_vertices(self) -> int:
        return len(self.vertices)


@dataclass
class PolygonCache:
    """
    cache for polygon that is translation/reflection invariant
    """

    def __init__(self):
        self._cache = dict()

    def _canon_form(self, p: Polygon):
        return (p.n_polygon.N, tuple(p.edge_distances))

    def __setitem__(self, polygon: Polygon, value) -> None:
        for p in [polygon, polygon.flip()]:
            for v in p.vertices:
                # change the "start" for the polygon
                canon_form = self._canon_form(p.rotate(-v))
                if canon_form in self._cache:
                    self._cache[canon_form] = value
                    return None
        self._cache[self._canon_form(polygon)] = value

    def __getitem__(self, polygon: Polygon) -> Any:
        for p in [polygon, polygon.flip()]:
            for v in p.vertices:
                # change the "start" for the polygon
                canon_form = self._canon_form(p.rotate(-v))
                if canon_form in self._cache:
                    return self._cache[canon_form]
        raise KeyError

    def __contains__(self, polygon: Polygon) -> bool:
        try:
            self[polygon]
            return True
        except KeyError:
            return False


@dataclass
class MaxTriangleCounter:
    n_polygon: NPolygon
    include_cache: bool = True

    def _get_valid_combo_counts(
        self,
        max_area: float,
        polygon: Polygon,
        cache: Optional[PolygonCache],
    ) -> int:
        if polygon.num_vertices < 3:
            return 1
        if cache is not None and polygon in cache:
            return cache[polygon]

        if polygon.num_vertices == 3:
            triangle = polygon
            if not lt(triangle.area, max_area):
                count = 1
            else:
                count = 0
        else:
            if lt(polygon.area, max_area):
                return polygon.num_triangle_combos
            else:
                count = 0
                # every edge vertex is part of exactly 1 triangle
                for i in range(2, polygon.num_vertices):
                    v1, v2, v3 = (
                        polygon.vertices[0],
                        polygon.vertices[1],
                        polygon.vertices[i],
                    )
                    triangle = Polygon([v1, v2, v3], self.n_polygon)
                    if lt(triangle.area, max_area):
                        p1, p2, p3 = self._get_paritions_minus_triangle(
                            triangle, polygon
                        )
                        count += (
                            self._get_valid_combo_counts(max_area, p1, cache)
                            * self._get_valid_combo_counts(max_area, p2, cache)
                            * self._get_valid_combo_counts(max_area, p3, cache)
                        )

                if cache is not None:
                    assert polygon not in cache
                    cache[polygon] = count
        return count

    def get_all_max_triangle_counts(self) -> Tuple[Counter, int]:
        # without loss of generality, we pick 1 vertices to be 0
        counts = Counter()
        N = self.n_polygon.N
        for j in range(1, N - 1):
            for k in range(j + 1, N):
                triangle = Polygon([0, j, k], self.n_polygon)
                counts[triangle] = self.get_max_triangle_count(triangle)
        # there is nothing special about the first vertex but we triple count
        # since every triangle has 3 vertex.
        total_count = sum(counts.values()) * N
        assert total_count % 3 == 0
        return counts, total_count // 3

    def get_max_triangle_count(self, triangle: Polygon) -> int:
        full_polygon = Polygon(list(range(self.n_polygon.N)), self.n_polygon)
        p1, p2, p3 = self._get_paritions_minus_triangle(triangle, full_polygon)
        if self.include_cache:
            cache = PolygonCache()
        else:
            cache = None
        return (
            self._get_valid_combo_counts(triangle.area, p1, cache)
            * self._get_valid_combo_counts(triangle.area, p2, cache)
            * self._get_valid_combo_counts(triangle.area, p3, cache)
        )

    def _get_paritions_minus_triangle(
        self, triangle: Polygon, polygon: Polygon
    ) -> list[Polygon]:
        assert len(triangle.vertices) == 3
        assert all([i in polygon.vertices] for i in triangle.vertices)
        i, j, k = triangle.vertices
        p1, r1 = polygon.partition(i, j)
        p2, r2 = r1.partition(j, k)
        # remaining is the triangle
        r3, p3 = r2.partition(i, k)
        assert r3 == triangle
        return [p1, p2, p3]


# Random utils
def same_under_rotation(l1: list, l2: list):
    if len(l1) != len(l2):
        return False
    repeated_l1 = l1 + l1
    for i in range(len(l1)):
        if repeated_l1[i : i + len(l1)] == l2:
            return True
    return False


def catalan_number(n: int) -> int:
    return math.factorial(2 * n) // (math.factorial(n + 1) * math.factorial(n))


def lt(n1: float, n2: float) -> bool:
    return not math.isclose(n1, n2) and n1 < n2

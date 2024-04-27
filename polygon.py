from dataclasses import dataclass
import math
from functools import cached_property
from typing import Counter, Tuple


@dataclass
class V:
    a: int
    b: int
    c: int


def partition_polygon(idxs: list[int], vertices: list[int]) -> list[list[int]]:
    idxs.sort()
    vertices.sort()
    return [vertices[idxs[i] : idxs[i + 1] + 1] for i in range(len(idxs) - 1)] + [
        list(set(vertices[: idxs[0] + 1] + vertices[idxs[-1] :]))
    ]


@dataclass(frozen=True)
class Polygon:
    """
    polygon defined by edges between set of vertices labeled by int on a N regular polyong
    """

    vertices: list[int]
    N: int

    def __post_init__(self):
        assert len(set(self.vertices)) == len(self.vertices)
        self.vertices.sort()

    def canonical_form(self) -> Tuple[set[int], int]:
        # sort vertices, index at 0
        min_vertex = min(self.vertices)
        return (set([(v - min_vertex) for v in self.vertices]), self.N)

    def __hash__(self):
        vertices, N = self.canonical_form()

        return hash((tuple(vertices), N))

    def partition(self, i: int, j: int) -> list["Polygon"]:
        """
        partition polygon with a segment from ith vertex to jth vertex
        """
        i_idx = self.vertices.index(i)
        j_idx = self.vertices.index(j)
        i_idx, j_idx = min(i_idx, j_idx), max(i_idx, j_idx)
        return [
            Polygon(self.vertices[i_idx : j_idx + 1], self.N),
            Polygon(self.vertices[: i_idx + 1] + self.vertices[j_idx:], self.N),
        ]


@dataclass
class Utils:
    """
    utils scoped to a N regular unit polygon
    """

    N: int

    @cached_property
    def R(self) -> float:
        """
        radius of circumscribed circle of polygon
        """
        return (2 * math.sin(math.pi / self.N)) ** -1

    def get_num_edges(self, v1: int, v2: int) -> int:
        """
        get number of edges between 2 vertices going any direction
        """
        assert v1 < self.N
        assert v2 < self.N
        distance = max(v1, v2) - min(v1, v2)
        return min(distance, self.N - distance)

    def get_distance(self, v1: int, v2: int) -> float:
        """
        distance of line segment connecting 2 verices
        """
        num_edges = self.get_num_edges(v1, v2)
        # interior angle between 2 vertices
        alpha = num_edges * ((2 * math.pi) / self.N)
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


@dataclass
class MaxTriangleCounter(Utils):
    N: int

    def _get_valid_combo_counts(self, max_area: float, polygon: Polygon, cache) -> int:
        if polygon in cache:
            return cache[polygon]
        vertices = polygon.vertices
        if len(vertices) < 3:
            return 1
        elif len(vertices) == 3:
            area = self.get_triangle_area(vertices)
            if not math.isclose(area, max_area) and area < max_area:
                count = 1
            else:
                count = 0
        else:
            count = 0
            for i in range(len(vertices)):
                for dist in range(2, len(vertices) - 1):  # exclude adjacent vertices
                    j = (i + dist) % len(vertices)
                    p1, p2 = polygon.partition(vertices[i], vertices[j])
                    count += self._get_valid_combo_counts(
                        max_area, p1, cache
                    ) * self._get_valid_combo_counts(max_area, p2, cache)
            cache[polygon] = count
        return count

    def get_max_triangle_count(self, idxs: list[int]) -> int:
        assert len(idxs) == 3
        full_polygon = Polygon(list(range(self.N)), self.N)
        area = self.get_triangle_area(idxs)
        idxs.sort()
        i, j, k = idxs
        p1, r1 = full_polygon.partition(i, j)
        p2, r2 = r1.partition(j, k)
        # remaining is the triangle
        r3, p3 = r2.partition(i, k)
        assert r3.vertices == idxs
        cache = dict()
        return (
            self._get_valid_combo_counts(area, p1, cache)
            * self._get_valid_combo_counts(area, p2, cache)
            * self._get_valid_combo_counts(area, p3, cache)
        )

    def get_all_max_triangle_counts(self) -> Tuple[Counter, int]:
        # without loss of generality, we pick 1 vertices to be 0
        counts = Counter()
        i = 0
        for j in range(1, self.N - 1):
            for k in range(j + 1, self.N):
                triangle = [i, j, k]
                counts[tuple(triangle)] = self.get_max_triangle_count(triangle)
        # every vertex has the same counts but every count is triple counted
        # since it takes 3 vertices to make a get_triangle
        total_count = sum(counts.values()) * self.N
        assert total_count % 3 == 0

        return counts, total_count // 3


@dataclass
class PolygonProblem(Utils):
    N: int

    def find_valid_count(
        self, max_area: float, vertices: list[int], seen_partition: set[Tuple[int, int]]
    ) -> int:
        vertices.sort()
        if len(vertices) < 3:
            return 1
        elif len(vertices) == 3:
            area = self.get_triangle_area(vertices)
            if not math.isclose(area, max_area) and area < max_area:
                return 1
            else:
                return 0
        else:
            count = 0
            # how do you iterate through all triangle partitions?
            for i in range(len(vertices)):
                for dist in range(2, len(vertices) - 1):  # exclude adjacent vertices
                    j = (i + dist) % len(vertices)
                    if (i, j) not in seen_partition:
                        seen_partition.add((i, j))
                        p1, p2 = partition_polygon([i, j], vertices)
                        count += self.find_valid_count(
                            max_area,
                            p1,
                            seen_partition,
                        ) * self.find_valid_count(max_area, p2, seen_partition)
            return count

    def find_max_triangle_count(self, triangle: list[int]) -> int:
        max_area = self.get_triangle_area(triangle)
        p1, p2, p3 = partition_polygon(triangle, list(range(self.N)))
        return math.prod(
            [
                self.find_valid_count(max_area, p1, set()),
                self.find_valid_count(max_area, p2, set()),
                self.find_valid_count(max_area, p3, set()),
            ]
        )

    def find_all_max_triangle_count(self) -> Counter:
        # without loss of generality, we pick 1 vertices to be 0
        counts = Counter()
        i = 0
        for j in range(1, self.N - 1):
            for k in range(j + 1, self.N):
                triangle = [i, j, k]
                counts[tuple(triangle)] = self.find_max_triangle_count(triangle)
        return counts

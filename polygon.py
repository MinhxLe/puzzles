from dataclasses import dataclass
import math
from functools import cached_property
from typing import Counter


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


# write a polygon class


@dataclass
class PolygonProblem:
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

    def get_area(self, vertices: list[int]) -> float:
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

    def find_valid_count(self, max_area: float, vertices: list[int]) -> int:
        vertices.sort()
        if len(vertices) < 3:
            return 1
        elif len(vertices) == 3:
            area = self.get_area(vertices)
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
                    p1, p2 = partition_polygon([i, j], vertices)
                    count += self.find_valid_count(
                        max_area, p1
                    ) * self.find_valid_count(max_area, p2)
            # im severly double counting
            return count // (2 * (len(vertices) - 3))

    def find_max_triangle_count(self, triangle: list[int]) -> int:
        max_area = self.get_area(triangle)
        p1, p2, p3 = partition_polygon(triangle, list(range(self.N)))
        return math.prod(
            [
                self.find_valid_count(max_area, p1),
                self.find_valid_count(max_area, p2),
                self.find_valid_count(max_area, p3),
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

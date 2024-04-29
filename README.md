# Introduction
This problem can be simplified to finding the number of triangle partitions such that a candidate triangle is the unique maximum triangle. The total count will then be to iterate through all candidate triangles (0(N^3)).

# Naive Recursive Solution 
Given a candidate maximum triangle, we need to to partition the remaining region of the polygon into triangles that are smaller than the candidate triangle. The algorithm is roughly the following:
```
def find_count(
    max_area,
    polygon,
    diagonals_to_exclude,  # used to prevent double counting
):
    if polygon is a triangle:
        return 1 if polygon.area < max_area else 0
    else:
        count = 0
        diagonals_to_exclude = diagonals_to_exclude.copy()  # we only exclude edges used from this recursion level and below
        for all possible diagnonals D in polygon:
            if D in diagonals_to_exclude:
                count += 0
            else:
                diagonals_to_exclude.add(D)
                polygon1, polygon2 = partition_polygon(polygon, D)
                count += find_count(max_area, polygon1, diagonals_to_exclude) * find_count(max_area, polygon2, diagonals_to_exclude)
        return count
```
Actual implementation can be found in `MaxTriangleCounter.get_max_triangle_count`


# Attempts at better than naive. 
We can see that the recursive algorithm quickly blows up in complexity. For a given polygon with N vertices, there are O(N^2) edges to try and each sub problem only reduces the problem by 1 vertex. This results in O(N^2 * N!) time complexity. For N=15, the problem already takes too long for me to run. We can do better.

1. Caching 
In my implementation, a polygon is defined by the set of vertices represented by ints. However the output to `find_count` for a given polygon does not change if the polygon is reflected or rotated. As such we can cache this algorithm based on an equivalent relationship. Full details can be found in `PolygonCache` implementation but the rough idea is to represent a polygon as relative edge distances (number of edges between vertices) between adjacent vertex instead of absolute vertex position. Finding a matching polygon during lookup is then looking up all the edge distance  of all rotations and reflection of that polygon. Note that this approach will blow up memory complexity intead since we can store all possible polygons.
```
def __getitem__(self, polygon: Polygon) -> Any:
    for p in [polygon, polygon.flip()]:
        for v in p.vertices:
            # change the "start" for the polygon
            canon_form = self._canon_form(p.rotate(-v))
            if canon_form in self._cache:
                return self._cache[canon_form]
    raise KeyError
```

2. Catalan numbers
There were 2 key insights:
- after a partition, both polygons are still convex.
- if a polygon's area is smaller than the maximum area, this problem reduces to counting the number of unique diagonalization of the the polygon. 
This insight lead to using catalan numbers which is O(n) for the factorial instead of a recursive relationship.


# [WIP] Curse of double counting 
Incorporating (1) and (2) turns out much more challenging than expected because over double counting. When iterating over possible diagonals to partition a polygon, there will be certain solutions containing previous diagonals, resulting in double counting. I have not fully solved this yet but my current approach is to build a set of diagonals that we have already add as part of our count. We then select a diagonal must "cross" every diagonal in that set. Any solution including that diagonal will be not counted yet because of the crossing.  

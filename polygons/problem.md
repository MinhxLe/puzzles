Problem Statement	
You are given ints n and z. We have a regular n-gon: a convex polygon with n sides, in which all sides have the same length and all internal angles are equal. We want to draw (n-3) non-intersecting diagonals in some way. Once we do that, we will have the polygon divided into exactly (n-2) triangles. We want to produce a situation in which one of these (n-2) triangles has a strictly larger area than each of the remaining (n-3).

The vertices of the polygon are labeled 1 through n in clockwise order. Two sets of diagonals are different if one of them contains a diagonal that is not present in the other one. Count all sets of (n-3) non-intersecting diagonals that produce an arrangement with the above property. Return that count modulo z.
Definition
Class:	MaximalTriangle
Method:	howMany
Parameters:	int, int
Returns:	int
Method signature:	int howMany(int n, int z)
(be sure your method is public)
Constraints
-	n will be between 3 and 444, inclusive.
-	z will be between 1 and 1,000,000,000 (10^9), inclusive.
Examples
0)	
    	
4
1000000000
Returns: 0
There are two ways how to select a diagonal in a square. Each of them produces two triangles of equal size.
1)	
    	
5
100
Returns: 5
There are five ways how to select two non-intersecting diagonals in a regular pentagon. Each of them produces an arrangement in which one triangle has a larger area than each of the other two.
2)	
    	
6
1000003
Returns: 2
For a regular hexagon, some sets of diagonals produce a good set of triangles, and some do not.
3)	
    	
10
1000000000
Returns: 1010
4)	
    	
15
1000000000
Returns: 714340
5)	
    	
100
987654321
Returns: 308571232

308571232

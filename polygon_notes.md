            for i in range(len(vertices) - 2):
                for j in range(i + 2, len(vertices)):
                    if i == 0 and j == len(vertices) - 1:
                        pass
                    else:
                        p1, p2 = partition_polygon([i, j], vertices)
                        count += self.find_valid_count(
                            max_area, p1
                        ) * self.find_valid_count(max_area, p2)
                        print(vertices, p1, p2, count)

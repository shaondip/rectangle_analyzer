class RectangleAnalyzer:
    def __init__(self, rectangles: list[dict]):
        self.rectangles = rectangles

    def find_overlaps(self) -> list[tuple]:
        """
        Find all pairs of rectangles that overlap.
        Returns a list of tuples like (i, j) where i < j are indices.
        """
        if not self.rectangles:
            return [] #if there are no rectangles, we return an empty list as there can be no overlaps
        results = []        
        for i in range(len(self.rectangles)): #iterating over all rectangles

            for j in range(i + 1, len(self.rectangles)):#according to the conditions of the problem-all the rectangles are parallel to the axes, so we can check for overlaps by checking if the orthogonal dimesions of the rectangles intersect.
                    if not (self.rectangles[i]['x'] >= self.rectangles[j]['x'] + self.rectangles[j]['width'] or self.rectangles[i]['x'] + self.rectangles[i]['width'] <= self.rectangles[j]['x'] or
                    self.rectangles[i]['y'] >= self.rectangles[j]['y'] + self.rectangles[j]['height'] or self.rectangles[j]['y'] >= self.rectangles[i]['y'] + self.rectangles[i]['height']):
                    
                        results.append((i, j))#if the rectangles overlap, we add the pair of indices to the results list
                
        return results
    


    def calculate_coverage_area(self) -> float:
        if not self.rectangles:
            return 0

        # Collect all unique x and y boundaries
        x_coords = sorted(set(
            val for r in self.rectangles
            for val in [r['x'], r['x'] + r['width']]
        ))
        y_coords = sorted(set(
            val for r in self.rectangles
            for val in [r['y'], r['y'] + r['height']]
        ))

        total_area = 0

        # Check each cell formed by consecutive coordinates
        for i in range(len(x_coords) - 1):
            for j in range(len(y_coords) - 1):
                # Pick a point inside this cell (the midpoint works)
                mid_x = (x_coords[i] + x_coords[i + 1]) / 2
                mid_y = (y_coords[j] + y_coords[j + 1]) / 2

                if self.is_point_covered(mid_x, mid_y):
                    # The whole cell is either covered or not
                    cell_width = x_coords[i + 1] - x_coords[i]
                    cell_height = y_coords[j + 1] - y_coords[j]
                    total_area += cell_width * cell_height

        return total_area



        
    def get_overlap_regions(self) -> list[dict]:
        """
        Find actual overlap regions between rectangles.
        Returns: List of dicts containing:
        - 'rect_indices': tuple of rectangle indices
        - 'region': dict with x, y, width, height of overlap

        """
        if not self.rectangles:
            return [] #if there are no rectangles, we return an empty list as there can be no overlaps
        overlap_region = []
        for i in range(len(self.rectangles)): #iterating over all rectangles
            for j in range(i + 1, len(self.rectangles)):
                if not (self.rectangles[i]['x'] >= self.rectangles[j]['x'] + self.rectangles[j]['width'] or self.rectangles[i]['x'] + self.rectangles[i]['width'] <= self.rectangles[j]['x'] or
                self.rectangles[i]['y'] >= self.rectangles[j]['y'] + self.rectangles[j]['height'] or self.rectangles[j]['y'] >= self.rectangles[i]['y'] + self.rectangles[i]['height']):
                    #overlap exists, we can calculate the boundaries of the overlapping region
                    overlap_along_x = min(self.rectangles[i]['x'] + self.rectangles[i]['width'], self.rectangles[j]['x'] + self.rectangles[j]['width']) - max(self.rectangles[i]['x'], self.rectangles[j]['x'])
                    overlap_along_y = min(self.rectangles[i]['y'] + self.rectangles[i]['height'], self.rectangles[j]['y'] + self.rectangles[j]['height']) - max(self.rectangles[i]['y'], self.rectangles[j]['y'])
                    overlap_region.append({
                        'rect_indices': (i, j),
                        'region': {
                            'x': max(self.rectangles[i]['x'], self.rectangles[j]['x']),#farthest left edge of the two rectangles
                            'y': max(self.rectangles[i]['y'], self.rectangles[j]['y']),#lowest bottom edge of the two rectangles
                            'width': overlap_along_x,
                            'height': overlap_along_y
                        }
                    })
        return overlap_region
                
        
    def is_point_covered(self, x: int|float, y: int|float) ->bool:
        
        """
        Check if a point is covered by any rectangle.
        Returns: boolean
        """
        if not self.rectangles:
            return False #if there are no rectangles, we return False as there can be no coverage
        for i in range(len(self.rectangles)):
            if self.rectangles[i]['x'] <= x < self.rectangles[i]['x'] + self.rectangles[i]['width'] and self.rectangles[i]['y'] <= y < self.rectangles[i]['y'] + self.rectangles[i]['height']:
                return True #if the point is within the boundaries of any rectangle, we return True 
        return False #if the point is not covered by any rectangle, we return False
    
        

    def find_max_overlap_point(self) -> dict:#works only for integers
        """
        Find a point covered by maximum number of rectangles.
        Returns: dict with 'x', 'y', 'count' keys
        Note: There might be multiple such points, return any

        one.
        """
        if not self.rectangles:
            return {'x': None, 'y': None, 'count': 0}
        max_overlap = {'x': 0, 'y': 0, 'count': 0}
        min_x = min(r['x'] for r in self.rectangles)
        max_x = max(r['x'] + r['width'] for r in self.rectangles)
        min_y = min(r['y'] for r in self.rectangles)
        max_y = max(r['y'] + r['height'] for r in self.rectangles)

        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                count = sum(1 for r in self.rectangles
                            if r['x'] <= x < r['x'] + r['width']
                            and r['y'] <= y < r['y'] + r['height'])
                if count > max_overlap['count']:
                    max_overlap = {'x': x, 'y': y, 'count': count}

        return max_overlap
    def get_stats(self) -> dict:
        """
        Get coverage statistics.
        Returns: dict with:
        - 'total_rectangles': int
        - 'overlapping_pairs': int
        - 'total_area': float (union area)
        - 'overlap_area': float (sum of all overlap regions)
        - 'coverage_efficiency': float (total_area /

        sum_of_individual_areas)

        """
        total_rectangles = len(self.rectangles)
        overlapping_pairs = len(self.find_overlaps())       
        total_area = self.calculate_coverage_area()
        
        overlap_area = sum(r['region']['width'] * r['region']['height'] for r in self.get_overlap_regions())
        sum_of_individual_areas = sum(r['width'] * r['height'] for r in self.rectangles)
        coverage_efficiency = total_area / sum_of_individual_areas if sum_of_individual_areas > 0 else 0    
        stats= {
            'total_rectangles': total_rectangles,   
            'overlapping_pairs': overlapping_pairs,
            'total_area': total_area,
            'overlap_area': overlap_area,
            'coverage_efficiency': coverage_efficiency
        }
        return stats    
    
       







rectangles = [
    {'x': 0, 'y': 0, 'width': 4, 'height': 3},
    {'x': 2, 'y': 1, 'width': 3, 'height': 3},
    {'x': 1, 'y': 2, 'width': 2, 'height': 4},
]
analyzer = RectangleAnalyzer(rectangles)
print(analyzer.find_overlaps())
print(analyzer.calculate_coverage_area())
print(analyzer.get_overlap_regions())   
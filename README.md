# Rectangle Analyzer

A Python tool for analyzing rectangle overlaps and coverage.

## Usage

```python
from rectangle_analyzer import RectangleAnalyzer

rectangles = [
    {'x': 0, 'y': 0, 'width': 4, 'height': 3},
    {'x': 2, 'y': 1, 'width': 3, 'height': 3},
    {'x': 1, 'y': 2, 'width': 2, 'height': 4},
]

analyzer = RectangleAnalyzer(rectangles)

print(analyzer.find_overlaps())           # [(0, 1), (0, 2), (1, 2)]
print(analyzer.calculate_coverage_area()) # 22
print(analyzer.is_point_covered(2, 2))    # True
print(analyzer.find_max_overlap_point())  # {'x': 2, 'y': 2, 'count': 3}
print(analyzer.get_stats())
```

## Type hints

### `RectangleAnalyzer(rectangles: list[dict])`
Constructor. Each dict must have keys: `x`, `y`, `width`, `height` (all `int` or `float`).

### `find_overlaps() -> list[tuple]`
Find all pairs of rectangles that overlap.
Returns a list of tuples `(i, j)` where `i < j` are rectangle indices.

### `calculate_coverage_area() -> float`
Calculate the total union area covered by all rectangles. Overlapping areas are counted only once. Uses coordinate compression.

### `get_overlap_regions() -> list[dict]`
Find the actual overlap regions between all pairs of rectangles.
Each result dict contains:
- `rect_indices`: `tuple` — pair of rectangle indices `(i, j)`
- `region`: `dict` — overlap rectangle with `x`, `y`, `width`, `height`

### `is_point_covered(x: int|float, y: int|float) -> bool`
Check if a point is inside any rectangle. Boundaries (edges) are inclusive.

### `find_max_overlap_point() -> dict`
Find a point covered by the maximum number of rectangles. Works only with integer coordinates.
Returns a dict with keys: `x`, `y`, `count`.

### `get_stats() -> dict`
Get coverage statistics. Returns a dict with:
- `total_rectangles`: `int`
- `overlapping_pairs`: `int`
- `total_area`: `float` — union area
- `overlap_area`: `float` — sum of all pairwise overlap region areas
- `coverage_efficiency`: `float` — `total_area / sum_of_individual_areas`

## Running Tests

```bash
pip install pytest
pytest test_rectangles.py -v
```

## Requirements

- Python >= 3.10

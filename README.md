# Rectangle Analyzer



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

## Running Tests

```bash
pip install pytest
pytest test_rectangles.py -v
```

## Requirements

- Python >= 3.10

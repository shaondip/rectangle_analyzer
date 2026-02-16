import pytest
from rectangle_analyzer import RectangleAnalyzer

def test_two_overlapping_rectangles():
    rectangles = [
        {'x': 0, 'y': 0, 'width': 4, 'height': 3},
        {'x': 2, 'y': 1, 'width': 3, 'height': 3},
    ]
    analyzer = RectangleAnalyzer(rectangles)
    assert analyzer.find_overlaps() == [(0, 1)]

def test_no_overlap():
    rectangles = [
        {'x': 0, 'y': 0, 'width': 2, 'height': 2},
        {'x': 10, 'y': 10, 'width': 2, 'height': 2},
    ]
    analyzer = RectangleAnalyzer(rectangles)
    assert analyzer.find_overlaps() == []

def test_empty_list():
    analyzer = RectangleAnalyzer([])
    assert analyzer.find_overlaps() == []

# --- calculate_coverage_area ---

def test_coverage_area_two_overlapping():
    rectangles = [
        {'x': 0, 'y': 0, 'width': 4, 'height': 3},
        {'x': 2, 'y': 1, 'width': 3, 'height': 3},
    ]
    analyzer = RectangleAnalyzer(rectangles)
    # rect 0 = 12, rect 1 = 9, overlap = 2x2 = 4, union = 17
    assert analyzer.calculate_coverage_area() == 17

def test_coverage_area_no_overlap():
    rectangles = [
        {'x': 0, 'y': 0, 'width': 2, 'height': 2},
        {'x': 10, 'y': 10, 'width': 3, 'height': 3},
    ]
    analyzer = RectangleAnalyzer(rectangles)
    assert analyzer.calculate_coverage_area() == 13

def test_coverage_area_empty():
    analyzer = RectangleAnalyzer([])
    assert analyzer.calculate_coverage_area() == 0

# --- get_overlap_regions ---

def test_overlap_region_simple():
    rectangles = [
        {'x': 0, 'y': 0, 'width': 4, 'height': 3},
        {'x': 2, 'y': 1, 'width': 3, 'height': 3},
    ]
    analyzer = RectangleAnalyzer(rectangles)
    regions = analyzer.get_overlap_regions()
    assert len(regions) == 1
    assert regions[0]['rect_indices'] == (0, 1)
    assert regions[0]['region'] == {'x': 2, 'y': 1, 'width': 2, 'height': 2}

def test_overlap_region_none():
    rectangles = [
        {'x': 0, 'y': 0, 'width': 2, 'height': 2},
        {'x': 10, 'y': 10, 'width': 2, 'height': 2},
    ]
    analyzer = RectangleAnalyzer(rectangles)
    assert analyzer.get_overlap_regions() == []

# --- is_point_covered ---

def test_point_inside():
    rectangles = [{'x': 0, 'y': 0, 'width': 4, 'height': 3}]
    analyzer = RectangleAnalyzer(rectangles)
    assert analyzer.is_point_covered(2, 1) == True

def test_point_outside():
    rectangles = [{'x': 0, 'y': 0, 'width': 4, 'height': 3}]
    analyzer = RectangleAnalyzer(rectangles)
    assert analyzer.is_point_covered(10, 10) == False

# --- find_max_overlap_point ---

def test_max_overlap_simple():
    rectangles = [
        {'x': 0, 'y': 0, 'width': 4, 'height': 3},
        {'x': 2, 'y': 1, 'width': 3, 'height': 3},
    ]
    analyzer = RectangleAnalyzer(rectangles)
    result = analyzer.find_max_overlap_point()
    assert result['count'] == 2

# --- get_stats ---

def test_stats_basic():
    """Basic stats test with two overlapping rectangles"""
    rectangles = [
        {'x': 0, 'y': 0, 'width': 4, 'height': 3},
        {'x': 2, 'y': 1, 'width': 3, 'height': 3},
    ]
    analyzer = RectangleAnalyzer(rectangles)
    stats = analyzer.get_stats()
    assert stats['total_rectangles'] == 2
    assert stats['overlapping_pairs'] == 1

def test_touching_edges_no_overlap():
    """Two rectangles sharing an edge but not overlapping"""
    rectangles = [
        {'x': 0, 'y': 0, 'width': 2, 'height': 2},
        {'x': 2, 'y': 0, 'width': 2, 'height': 2},
    ]
    analyzer = RectangleAnalyzer(rectangles)
    assert analyzer.find_overlaps() == []

def test_one_inside_another():
    """Small rectangle completely inside a large one"""
    rectangles = [
        {'x': 0, 'y': 0, 'width': 10, 'height': 10},
        {'x': 2, 'y': 2, 'width': 3, 'height': 3},
    ]
    analyzer = RectangleAnalyzer(rectangles)
    assert analyzer.find_overlaps() == [(0, 1)]
    assert analyzer.calculate_coverage_area() == 100

def test_identical_rectangles():
    """Two rectangles at the exact same position and size"""
    rectangles = [
        {'x': 0, 'y': 0, 'width': 5, 'height': 5},
        {'x': 0, 'y': 0, 'width': 5, 'height': 5},
    ]
    analyzer = RectangleAnalyzer(rectangles)
    assert analyzer.find_overlaps() == [(0, 1)]
    assert analyzer.calculate_coverage_area() == 25

def test_single_rectangle():
    """Only one rectangle, so no overlaps and area is just the rectangle's area"""
    rectangles = [{'x': 0, 'y': 0, 'width': 5, 'height': 3}]
    analyzer = RectangleAnalyzer(rectangles)
    assert analyzer.find_overlaps() == []
    assert analyzer.calculate_coverage_area() == 15

def test_negative_coordinates():
    """Two rectangles with negative coordinates overlapping"""
    rectangles = [
        {'x': -3, 'y': -3, 'width': 4, 'height': 4},
        {'x': -1, 'y': -1, 'width': 4, 'height': 4},
    ]
    analyzer = RectangleAnalyzer(rectangles)
    assert analyzer.find_overlaps() == [(0, 1)]

def test_three_overlapping_rectangles():
    """Three rectangles with pairwise and triple overlaps"""
    rectangles = [
        {'x': 0, 'y': 0, 'width': 4, 'height': 3},
        {'x': 2, 'y': 1, 'width': 3, 'height': 3},
        {'x': 1, 'y': 2, 'width': 2, 'height': 4},
    ]
    analyzer = RectangleAnalyzer(rectangles)
    # All three pairs overlap
    assert analyzer.find_overlaps() == [(0, 1), (0, 2), (1, 2)]
    # Union area via inclusion-exclusion: 12+9+8-4-2-2+1 = 22
    assert analyzer.calculate_coverage_area() == 22
    # 3 pairwise overlap regions
    regions = analyzer.get_overlap_regions()
    assert len(regions) == 3
    # Triple overlap at [2,3)×[2,3), so point (2,2) is covered by all 3
    result = analyzer.find_max_overlap_point()
    assert result['count'] == 3

def test_many_rectangles_overlapping():
    """100 rectangles all overlapping at origin"""
    rectangles = [
        {'x': 0, 'y': 0, 'width': 10, 'height': 10}
        for _ in range(100)
    ]
    analyzer = RectangleAnalyzer(rectangles)
    assert analyzer.calculate_coverage_area() == 100
    assert len(analyzer.find_overlaps()) == 100 * 99 // 2  # all pairs
def test_many_rectangles_non_overlapping():

    """100 rectangles all non-overlapping, placed side by side"""
    rectangles = [
        {'x': i * 10, 'y': 0, 'width': 10, 'height': 10}
        for i in range(100)
    ]
    analyzer = RectangleAnalyzer(rectangles)
    assert analyzer.calculate_coverage_area() == 100 * 100  # 100 rects × 100 area each
    assert len(analyzer.find_overlaps()) == 0  # no pairs overlap
"""
 Ashley Foglia
 SSW 567 - Fall 2023

 test_triangleclassification

 Test functions for the triangle_classification program.

"""

import math
import pytest
import triangle_classification as tc

class TestClassifyTriangle:
    """Tests the classify_triangle function in the triangle_classification program"""
    # Define test cases
    validTriangleCases = [
        [1, 1, 1, "Equilateral"],
        [13.7, 13.7, 13.7, "Equilateral"],
        [2, 1, 2, "Isosceles"],
        [9.76, 9.76, 14.02, "Isosceles"],
        [12.7, 3.4, 14, "Scalene"],
        [3, 4, 5, "Scalene Right"],
        [2 * math.sqrt(3), 4 * math.sqrt(3), 2 * math.sqrt(15), "Scalene Right"],
        [5, 5, 5 * math.sqrt(2), "Isosceles Right"],
        [10, 10, 10 * math.sqrt(2), "Isosceles Right"],
    ]

    invalidTriangleCases = [
        [0, 0, 0, ],
        [None, None, None],
        [-1, -1, -1],
        [10, 0, 10],
        [10, 10, None],
        [-1, 10, 10],
        [10, 2, 1],
        [None, -1, 0],
        [999, 1, 1],
        ["test1", "test2", "test3"],
    ]

    @pytest.mark.parametrize('valid_triangle_case', validTriangleCases)
    def test_validtrianglecases(self, valid_triangle_case):
        """Test valid triangle cases output valid triangle classification string"""
        assert tc.classify_triangle(valid_triangle_case[0]
                                , valid_triangle_case[1]
                                , valid_triangle_case[2]) == valid_triangle_case[3]

    @pytest.mark.parametrize('invalid_triangle_case', invalidTriangleCases)
    def test_invalidtrianglecases(self, invalid_triangle_case):
        """Test invalid triangle cases raise ValueError"""
        with pytest.raises((ValueError, TypeError)):
            tc.classify_triangle(invalid_triangle_case[0]
                            , invalid_triangle_case[1]
                            , invalid_triangle_case[2])

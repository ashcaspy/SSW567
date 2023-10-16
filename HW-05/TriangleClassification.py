# Ashley Foglia
# SSW 567 - Fall 2023
# HW 01 - Testing Triangle Classification

import pytest
import math

# Define triangle classification function
def classify_triangle(a: float, b: float, c: float) -> str:
    #Store inputs as array
    sides = [a, b, c]

    #Validation
    # No null values
    if any(sides) is None:
        raise Exception("All input values must be non-null.")
    
    # All side lengths need to be > 0
    if not all(i > 0 for i in sides):
        raise Exception("All input values must be nonzero and positive.")
    
    # Sum of smaller sides must be greater than (not equal to) length of greatest side
    if sum(sides) - max(sides) <= max(sides):
        raise Exception("Input values do not define a valid triangle.")

    # Initialize output string - Default to Undefined if triangle does not fall into any of the 4 categories
    triangleType = "Undefined"

    #Comparison + categorization
    if len(set(sides)) == 1:
        triangleType = "Equilateral"
    elif len(set(sides)) == 2 :
        triangleType = "Isosceles"
    elif len(set(sides)) == 3:
        triangleType = "Scalene"

    #Right triangle check - exclude undefined triangle type
    if triangleType != "Undefined" and round(a*a + b*b, 10) == round(c*c, 10):
        triangleType += " Right"

    #Output
    return triangleType

# Main method
def main():
    a = float(input("Length of side 1: "))
    b = float(input("Length of side 2: "))
    c = float(input("Length of side 3: "))
    print(classify_triangle(a, b, c))

if __name__ == "__main__":
    main()

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

@pytest.mark.parametrize('validTriangleCase', validTriangleCases)
def test_validtrianglecases(validTriangleCase):
    assert classify_triangle(validTriangleCase[0], validTriangleCase[1], validTriangleCase[2]) == validTriangleCase[3]

@pytest.mark.parametrize('invalidTriangleCase', invalidTriangleCases)
def test_invalidtrianglecases(invalidTriangleCase):
    with pytest.raises(Exception):
        classify_triangle(invalidTriangleCase[0], invalidTriangleCase[1], invalidTriangleCase[2])
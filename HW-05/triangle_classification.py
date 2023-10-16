"""
 Ashley Foglia
 SSW 567 - Fall 2023

 triangle_classification
 
 Classifies triangles based on user inputted side length

"""

# Define triangle classification function
def classify_triangle(a: float, b: float, c: float) -> str:
    """Function used to classify a triangle type, given inputs of side lengths."""
    #Store inputs as array
    sides = [a, b, c]

    #Validation
    # No null values
    if any(sides) is None:
        raise ValueError("All input values must be non-null.")

    # All side lengths need to be > 0
    if not all(i > 0 for i in sides):
        raise ValueError("All input values must be nonzero and positive.")

    # Sum of smaller sides must be greater than (not equal to) length of greatest side
    if sum(sides) - max(sides) <= max(sides):
        raise ValueError("Input values do not define a valid triangle.")

    # Initialize output string - Default to Undefined if triangle does not fall into any
    # of the 4 categories
    triangle_type = "Undefined"

    #Comparison + categorization
    if len(set(sides)) == 1:
        triangle_type = "Equilateral"
    elif len(set(sides)) == 2 :
        triangle_type = "Isosceles"
    elif len(set(sides)) == 3:
        triangle_type = "Scalene"

    #Right triangle check - exclude undefined triangle type
    if triangle_type != "Undefined" and round(a*a + b*b, 10) == round(c*c, 10):
        triangle_type += " Right"

    #Output
    return triangle_type

import math

SQFT_PER_BUNDLE = 33  # sq ft of roof area covered by one bundle of shingles (company rules)

def pitch_factor(rise):
    """Return the slope multiplier for a pitch of rise/12."""
    return math.sqrt(1 + (rise / 12) ** 2)

def area_from_dimensions(length, width, rise):
    """Footprint length x width (feet) -> real roof area in sq ft."""
    footprint_area = length * width
    return footprint_area * pitch_factor(rise)

def bundles_needed(area_sqft):
    """Roof area -> number of shingle bundles (always round UP)."""
    return math.ceil(area_sqft / SQFT_PER_BUNDLE)

def area_from_face(length, width, rise, num_faces=1):
    """Return the area of a roof with the given dimensions and number of faces."""
    return area_from_dimensions(length, width, rise) * num_faces


#quick test code
if __name__ == "__main__":
    assert bundles_needed(990) == 30    
    assert bundles_needed(991) == 31    
    assert bundles_needed(1000) == 31   
    assert bundles_needed(0) == 0
    assert round(pitch_factor(6), 3) == 1.118
    assert round(area_from_face(40, 15, 6)) == 1342   # two 40x15 faces at 6/12
    print("All tests passed")            
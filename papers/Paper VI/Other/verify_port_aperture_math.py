"""
Verify the correct port domain boundary size for k=4 packing on a sphere.

For a tetrahedron with 4 faces, each face normal points to a port on the enclosing sphere.
The domain boundary is where adjacent port regions meet.
"""
import math

print("=" * 60)
print("PORT APERTURE SIZING FOR k=4")
print("=" * 60)

# For a regular tetrahedron inscribed in a sphere,
# the angle between any two face normals is:
# arccos(-1/3) ≈ 109.47 degrees

face_normal_angle = math.acos(-1/3)
print(f"\nAngle between face normals: {math.degrees(face_normal_angle):.2f} degrees")

# The domain boundary is at the midpoint between adjacent face normals
# So the angular radius of each port domain is half this:
domain_angular_radius = face_normal_angle / 2
print(f"Domain angular radius (half-angle): {math.degrees(domain_angular_radius):.2f} degrees")

# The aperture factor sqrt(k/π) for k=4:
aperture_factor = math.sqrt(4 / math.pi)
print(f"\nAperture factor sqrt(4/pi): {aperture_factor:.4f}")

# What does the aperture factor represent?
# It's the ratio of the port "opening" diameter to the sphere's characteristic length
# For a unit sphere, this would give the linear aperture size

# Alternative calculation: spherical cap area
# Each of 4 ports covers 1/4 of the sphere's surface
# Spherical cap area = 2πR²(1 - cos(θ))
# For 1/4 sphere: area = πR²
# So: πR² = 2πR²(1 - cos(θ))
#     1/2 = 1 - cos(θ)
#     cos(θ) = 1/2
#     θ = 60 degrees

cap_angle_for_quarter_sphere = math.acos(0.5)
print(f"\nAngle for spherical cap = 1/4 sphere area: {math.degrees(cap_angle_for_quarter_sphere):.2f} degrees")

print("\n" + "=" * 60)
print("RECOMMENDATION")
print("=" * 60)

# The domain boundary (where ports meet) is at 54.74 degrees
# But the "aperture" (opening) might be smaller
# For k=4 packing, the aperture factor gives the effective opening

# Using the aperture formula from the code: asin(sqrt(4/π)/2)
code_angle = math.asin(math.sqrt(4 / math.pi) / 2)
print(f"\nCode's calculated angle: asin(sqrt(4/pi)/2) = {math.degrees(code_angle):.2f} degrees")

# But the code then uses 45 degrees "for visual clarity"
print(f"Code's actual angle used: 45 degrees")

print(f"\nTheoretically correct domain boundary: {math.degrees(domain_angular_radius):.2f} degrees")

print("""
SUMMARY:
- Face normals are ~109.47° apart
- Domain boundaries meet at ~54.74° from each face normal
- Current code uses 45° (too small by ~10°)
- For accurate k=4 representation, use ~54.74° or ~55°
""")

# For the sphere radius calculation
print("=" * 60)
print("CIRCLE RADIUS ON SPHERE")
print("=" * 60)

sphere_radius = 1.0  # Unit sphere for calculation
# The circle on the sphere at angular radius θ has radius: R * sin(θ)

circle_radius_correct = sphere_radius * math.sin(domain_angular_radius)
circle_radius_current = sphere_radius * math.sin(math.radians(45))

print(f"\nFor unit sphere (R=1):")
print(f"  Correct circle radius (54.74°): {circle_radius_correct:.4f}")
print(f"  Current circle radius (45°): {circle_radius_current:.4f}")
print(f"  Ratio (current/correct): {circle_radius_current/circle_radius_correct:.2%}")

import math

class Ray:
    def __init__(self, origin, direction, length):
        self.origin = origin
        self.direction = direction
        self.length = length

def ray_aabb_intersection(ray, aabb_min, aabb_max):
    tmin = (aabb_min[0] - ray.origin[0]) / ray.direction[0]
    tmax = (aabb_max[0] - ray.origin[0]) / ray.direction[0]
    if tmin > tmax:
        tmin, tmax = tmax, tmin

    tymin = (aabb_min[1] - ray.origin[1]) / ray.direction[1]
    tymax = (aabb_max[1] - ray.origin[1]) / ray.direction[1]
    if tymin > tymax:
        tymin, tymax = tymax, tymin

    if (tmin > tymax) or (tymin > tmax):
        return False

    if tymin > tmin:
        tmin = tymin
    if tymax < tmax:
        tmax = tymax

    tzmin = (aabb_min[2] - ray.origin[2]) / ray.direction[2]
    tzmax = (aabb_max[2] - ray.origin[2]) / ray.direction[2]
    if tzmin > tzmax:
        tzmin, tzmax = tzmax, tzmin

    if (tmin > tzmax) or (tzmin > tmax):
        return False

    if tzmin > tmin:
        tmin = tzmin
    if tzmax < tmax:
        tmax = tzmax

    return (tmin < ray.length) and (tmax > 0)

def raycast(ray, objects):
    for obj in objects:
        aabb_min = obj.bounding_box_min  # Assuming these are lists
        aabb_max = obj.bounding_box_max
        if ray_aabb_intersection(ray, aabb_min, aabb_max):
            return obj  # Return the first object hit by the ray
    return None

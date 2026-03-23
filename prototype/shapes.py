"""
Rich geometric shapes for high-dimensional embedding.
Each returns (n, k) points where k is the native dimensionality of the shape.
"""

import numpy as np


def helix(n=1000, turns=4, radius=1.0):
    """3D helix — coils along z-axis."""
    t = np.linspace(0, turns * 2 * np.pi, n)
    x = radius * np.cos(t)
    y = radius * np.sin(t)
    z = t / (turns * 2 * np.pi) * 2 - 1  # normalize to [-1, 1]
    return np.column_stack([x, y, z])


def torus(n=2000, R=1.0, r=0.35):
    """3D torus surface — doughnut shape."""
    theta = np.random.uniform(0, 2 * np.pi, n)
    phi = np.random.uniform(0, 2 * np.pi, n)
    x = (R + r * np.cos(phi)) * np.cos(theta)
    y = (R + r * np.cos(phi)) * np.sin(theta)
    z = r * np.sin(phi)
    return np.column_stack([x, y, z])


def linked_rings(n=1500):
    """3D linked rings — two interlocking circles."""
    n_each = n // 2
    # Ring 1: in XY plane
    t1 = np.linspace(0, 2 * np.pi, n_each, endpoint=False)
    r1 = np.column_stack([np.cos(t1), np.sin(t1), np.zeros(n_each)])
    # Ring 2: in XZ plane, offset in Y
    t2 = np.linspace(0, 2 * np.pi, n_each, endpoint=False)
    r2 = np.column_stack([np.cos(t2) + 0.5, np.zeros(n_each), np.sin(t2)])
    pts = np.vstack([r1, r2])
    pts += np.random.randn(*pts.shape) * 0.02
    labels = np.array([0] * n_each + [1] * n_each)
    return pts, labels


def lissajous(n=1000, a=3, b=2, delta=np.pi / 4):
    """2D Lissajous curve."""
    t = np.linspace(0, 2 * np.pi, n)
    x = np.sin(a * t + delta)
    y = np.sin(b * t)
    pts = np.column_stack([x, y])
    pts += np.random.randn(n, 2) * 0.02
    return pts


def trefoil_knot(n=1000):
    """3D trefoil knot — a classic mathematical knot."""
    t = np.linspace(0, 2 * np.pi, n)
    x = np.sin(t) + 2 * np.sin(2 * t)
    y = np.cos(t) - 2 * np.cos(2 * t)
    z = -np.sin(3 * t)
    pts = np.column_stack([x, y, z]) / 3  # normalize
    pts += np.random.randn(n, 3) * 0.02
    return pts


def sphere_surface(n=1500, radius=1.0):
    """3D sphere surface — uniform points on a sphere."""
    phi = np.random.uniform(0, 2 * np.pi, n)
    cos_theta = np.random.uniform(-1, 1, n)
    sin_theta = np.sqrt(1 - cos_theta ** 2)
    x = radius * sin_theta * np.cos(phi)
    y = radius * sin_theta * np.sin(phi)
    z = radius * cos_theta
    return np.column_stack([x, y, z])


def mobius_strip(n=1500, R=1.0, w=0.4):
    """3D Möbius strip — a non-orientable surface."""
    u = np.random.uniform(0, 2 * np.pi, n)
    v = np.random.uniform(-w, w, n)
    x = (R + v * np.cos(u / 2)) * np.cos(u)
    y = (R + v * np.cos(u / 2)) * np.sin(u)
    z = v * np.sin(u / 2)
    return np.column_stack([x, y, z])


def star_polygon(n=800, points=7, inner_ratio=0.4):
    """2D star polygon."""
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    r = np.where(np.sin(points * t / 2) > 0, 1.0, inner_ratio)
    x = r * np.cos(t)
    y = r * np.sin(t)
    pts = np.column_stack([x, y])
    pts += np.random.randn(n, 2) * 0.03
    return pts


def grid_3d(n=1000):
    """3D grid / lattice of points."""
    side = int(np.cbrt(n)) + 1
    x = np.linspace(-1, 1, side)
    pts = np.array(np.meshgrid(x, x, x)).reshape(3, -1).T
    idx = np.random.choice(len(pts), min(n, len(pts)), replace=False)
    pts = pts[idx]
    pts += np.random.randn(*pts.shape) * 0.03
    return pts

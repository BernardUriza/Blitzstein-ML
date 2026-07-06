# cwc - Declarative 3D Viz Builders
# Traduce specs JSON de content/ a escenas three.js. El contenido declara
# QUÉ visualizar (superficie, barras, puntos); el motor decide CÓMO.

import math

from browser import window

from engine.three.scene import ThreeScene

_SAFE_MATH = {name: getattr(math, name) for name in dir(math) if not name.startswith('_')}


def build_viz(spec):
    """
    Crea un ThreeScene a partir de un spec declarativo.

    Spec común: kind (surface|bars|points), height, camera, grid, grid_size.
    surface: expr (en x, y), x [min,max], y [min,max], n, z_scale, color, wireframe
    bars:    values (matriz 2D), z_scale, gap, color
    points:  points ([[x,y,z], ...]), size, color
    """
    builders = {
        'surface': _build_surface,
        'bars': _build_bars,
        'points': _build_points,
    }
    builder = builders.get(spec.get('kind', 'surface'), _build_surface)

    def build(THREE, scene):
        _add_grid(THREE, scene, spec)
        builder(THREE, scene, spec)

    return ThreeScene(
        height=spec.get('height', 380),
        camera=spec.get('camera', [7, 6, 9]),
        build=build,
    )


def _eval_expr(expr, **variables):
    scope = dict(_SAFE_MATH)
    scope.update(variables)
    return eval(expr, {'__builtins__': {}}, scope)


def _add_grid(THREE, scene, spec):
    if not spec.get('grid', True):
        return
    size = spec.get('grid_size', 10)
    scene.add(THREE.GridHelper.new(size, size, 0x4b5563, 0x1f2937))
    scene.add(THREE.AxesHelper.new(size / 2))


def _build_surface(THREE, scene, spec):
    x0, x1 = spec.get('x', [-3, 3])
    y0, y1 = spec.get('y', [-3, 3])
    n = spec.get('n', 48)
    z_scale = spec.get('z_scale', 1)
    expr = spec.get('expr', '0')

    geometry = THREE.PlaneGeometry.new(x1 - x0, y1 - y0, n, n)
    positions = geometry.attributes.position
    center_x = (x0 + x1) / 2
    center_y = (y0 + y1) / 2
    for i in range(positions.count):
        x = positions.getX(i) + center_x
        y = positions.getY(i) + center_y
        positions.setZ(i, _eval_expr(expr, x=x, y=y) * z_scale)
    geometry.computeVertexNormals()

    material = THREE.MeshPhongMaterial.new({
        'color': spec.get('color', 0x6366f1),
        'side': THREE.DoubleSide,
        'shininess': 60,
    })
    mesh = THREE.Mesh.new(geometry, material)
    mesh.rotation.x = -math.pi / 2
    scene.add(mesh)

    if spec.get('wireframe', True):
        wire_material = THREE.MeshBasicMaterial.new({
            'color': 0x818cf8,
            'wireframe': True,
            'transparent': True,
            'opacity': 0.25,
        })
        wire = THREE.Mesh.new(geometry, wire_material)
        wire.rotation.x = -math.pi / 2
        scene.add(wire)


def _build_bars(THREE, scene, spec):
    values = spec.get('values', [])
    z_scale = spec.get('z_scale', 1)
    gap = spec.get('gap', 0.15)
    rows = len(values)
    cols = len(values[0]) if rows else 0

    material = THREE.MeshPhongMaterial.new({'color': spec.get('color', 0x6366f1)})
    for r in range(rows):
        for c in range(cols):
            bar_height = values[r][c] * z_scale
            if bar_height <= 0:
                continue
            geometry = THREE.BoxGeometry.new(1 - gap, bar_height, 1 - gap)
            bar = THREE.Mesh.new(geometry, material)
            bar.position.set(c - (cols - 1) / 2, bar_height / 2, r - (rows - 1) / 2)
            scene.add(bar)


def _build_points(THREE, scene, spec):
    pts = spec.get('points', [])
    flat = [coord for p in pts for coord in p]
    array = window.Float32Array.new(flat)
    geometry = THREE.BufferGeometry.new()
    geometry.setAttribute('position', THREE.BufferAttribute.new(array, 3))
    material = THREE.PointsMaterial.new({
        'color': spec.get('color', 0xf59e0b),
        'size': spec.get('size', 0.12),
    })
    scene.add(THREE.Points.new(geometry, material))

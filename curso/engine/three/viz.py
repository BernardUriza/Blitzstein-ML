# cwc - Declarative 3D Viz Builders
# Traduce specs JSON de content/ a escenas three.js. El contenido declara
# QUÉ visualizar (superficie, barras, puntos); el motor decide CÓMO.

import math

from browser import document, window

from engine.three.scene import ThreeScene

_SAFE_MATH = {name: getattr(math, name) for name in dir(math) if not name.startswith('_')}


def build_viz(spec):
    """
    Crea un ThreeScene a partir de un spec declarativo.

    Spec común: kind (surface|bars|points), height, camera, grid, grid_size,
                labels ([{text, pos, scale, color}]).
    surface: expr (en x, y), x [min,max], y [min,max], n, z_scale, color, wireframe
    bars:    values (matriz 2D), z_scale, gap, color,
             highlight ([[fila, col], ...]), highlight_color
    points:  points ([[x,y,z], ...]), size, color,
             point_colors ([hex, ...] por punto), edges ([[i,j], ...]), edge_color
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
        _add_labels(THREE, scene, spec)

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
    highlight = {(cell[0], cell[1]) for cell in spec.get('highlight', [])}

    base_material = THREE.MeshPhongMaterial.new({'color': spec.get('color', 0x6366f1)})
    highlight_material = THREE.MeshPhongMaterial.new({
        'color': spec.get('highlight_color', 0xf59e0b),
        'emissive': spec.get('highlight_color', 0xf59e0b),
        'emissiveIntensity': 0.25,
    })
    for r in range(rows):
        for c in range(cols):
            bar_height = values[r][c] * z_scale
            if bar_height <= 0:
                continue
            geometry = THREE.BoxGeometry.new(1 - gap, bar_height, 1 - gap)
            material = highlight_material if (r, c) in highlight else base_material
            bar = THREE.Mesh.new(geometry, material)
            bar.position.set(c - (cols - 1) / 2, bar_height / 2, r - (rows - 1) / 2)
            scene.add(bar)


def _build_points(THREE, scene, spec):
    pts = spec.get('points', [])
    flat = [coord for p in pts for coord in p]
    array = window.Float32Array.new(flat)
    geometry = THREE.BufferGeometry.new()
    geometry.setAttribute('position', THREE.BufferAttribute.new(array, 3))

    point_colors = spec.get('point_colors')
    if point_colors:
        rgb = []
        for hex_color in point_colors:
            rgb.extend([
                ((hex_color >> 16) & 0xff) / 255,
                ((hex_color >> 8) & 0xff) / 255,
                (hex_color & 0xff) / 255,
            ])
        geometry.setAttribute('color', THREE.BufferAttribute.new(window.Float32Array.new(rgb), 3))
        material = THREE.PointsMaterial.new({
            'vertexColors': True,
            'size': spec.get('size', 0.12),
        })
    else:
        material = THREE.PointsMaterial.new({
            'color': spec.get('color', 0xf59e0b),
            'size': spec.get('size', 0.12),
        })
    scene.add(THREE.Points.new(geometry, material))

    edges = spec.get('edges', [])
    if edges:
        edge_flat = []
        for a, b in edges:
            edge_flat.extend(pts[a])
            edge_flat.extend(pts[b])
        edge_geometry = THREE.BufferGeometry.new()
        edge_geometry.setAttribute(
            'position', THREE.BufferAttribute.new(window.Float32Array.new(edge_flat), 3))
        edge_material = THREE.LineBasicMaterial.new({
            'color': spec.get('edge_color', 0x4b5563),
            'transparent': True,
            'opacity': 0.7,
        })
        scene.add(THREE.LineSegments.new(edge_geometry, edge_material))


def _add_labels(THREE, scene, spec):
    for label in spec.get('labels', []):
        text = label.get('text', '')
        pos = label.get('pos', [0, 0, 0])
        scale = label.get('scale', 0.9)
        color = label.get('color', '#e5e7eb')

        canvas = document.createElement('canvas')
        canvas.width = 256
        canvas.height = 128
        ctx = canvas.getContext('2d')
        ctx.font = 'bold 56px Inter, system-ui, sans-serif'
        ctx.fillStyle = color
        ctx.textAlign = 'center'
        ctx.textBaseline = 'middle'
        ctx.fillText(text, 128, 64)

        texture = THREE.CanvasTexture.new(canvas)
        material = THREE.SpriteMaterial.new({'map': texture, 'transparent': True})
        sprite = THREE.Sprite.new(material)
        sprite.position.set(pos[0], pos[1], pos[2])
        sprite.scale.set(scale * 2, scale, 1)
        scene.add(sprite)

# cwc - ThreeScene Component
# Canvas 3D interactivo: cámara en perspectiva, órbita con damping,
# luces estándar y loop de animación con cleanup en unmount.

from browser import window, html

from engine.components.base import Component
from engine.three.loader import ensure_three


class ThreeScene(Component):
    """
    Componente de escena three.js.

    Props:
        height: alto en px (default 380)
        background: color hex del fondo (default gris-900)
        camera: posición inicial [x, y, z]
        build: callable(THREE, scene) que puebla la escena
    """

    def render(self):
        height = self.props.get('height', 380)
        self.container = html.DIV(
            Class="three-scene relative w-full rounded-xl overflow-hidden bg-gray-900",
            style={'height': f'{height}px'}
        )
        self.container <= html.DIV(
            "Cargando visualización 3D…",
            Class="absolute inset-0 flex items-center justify-center text-gray-400 text-sm"
        )
        return self.container

    def on_mount(self):
        self._frame = None
        self._renderer = None
        ensure_three(self._init_scene)

    def _init_scene(self):
        if not self._mounted:
            return

        THREE = window.THREE
        height = self.props.get('height', 380)
        width = self.container.offsetWidth or 640

        self.container.innerHTML = ""

        self.scene = THREE.Scene.new()
        self.scene.background = THREE.Color.new(self.props.get('background', 0x111827))

        self.camera = THREE.PerspectiveCamera.new(50, width / height, 0.1, 1000)
        cam = self.props.get('camera', [7, 6, 9])
        self.camera.position.set(cam[0], cam[1], cam[2])

        self._renderer = THREE.WebGLRenderer.new({'antialias': True})
        self._renderer.setSize(width, height)
        self._renderer.setPixelRatio(window.devicePixelRatio or 1)
        self.container <= self._renderer.domElement

        self.controls = THREE.OrbitControls.new(self.camera, self._renderer.domElement)
        self.controls.enableDamping = True
        self.controls.target.set(0, 0.5, 0)

        self.scene.add(THREE.AmbientLight.new(0xffffff, 0.55))
        key_light = THREE.DirectionalLight.new(0xffffff, 0.9)
        key_light.position.set(5, 10, 7)
        self.scene.add(key_light)

        build = self.props.get('build')
        if build:
            build(THREE, self.scene)

        self._animate(0)

    def _animate(self, _timestamp):
        if not self._mounted or self._renderer is None:
            return
        self.controls.update()
        self._renderer.render(self.scene, self.camera)
        self._frame = window.requestAnimationFrame(self._animate)

    def on_unmount(self):
        if self._frame is not None:
            window.cancelAnimationFrame(self._frame)
            self._frame = None
        if self._renderer is not None:
            self._renderer.dispose()
            self._renderer = None

# cwc - Three.js Loader
# Carga perezosa de three.js: los 600KB del vendor solo se descargan
# cuando una lección monta su primera escena 3D.

from browser import document, window

_SOURCES = ['vendor/three/three.min.js', 'vendor/three/OrbitControls.js']
_state = {'status': 'idle', 'callbacks': []}


def ensure_three(callback):
    """
    Garantiza que window.THREE (+ OrbitControls) esté disponible y
    luego invoca callback. Idempotente: múltiples escenas comparten
    una sola carga.
    """
    if _state['status'] == 'ready':
        callback()
        return
    _state['callbacks'].append(callback)
    if _state['status'] == 'loading':
        return
    _state['status'] = 'loading'
    _load_script(0)


def _load_script(index):
    if index >= len(_SOURCES):
        _state['status'] = 'ready'
        pending = _state['callbacks'][:]
        _state['callbacks'] = []
        for cb in pending:
            cb()
        return

    script = document.createElement('script')
    script.src = _SOURCES[index]
    script.bind('load', lambda evt, i=index: _load_script(i + 1))
    script.bind('error', lambda evt, src=_SOURCES[index]: _on_error(src))
    document.head.appendChild(script)


def _on_error(src):
    _state['status'] = 'error'
    window.console.error(f"[engine.three] No se pudo cargar {src}")

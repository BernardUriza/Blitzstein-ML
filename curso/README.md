# curso/ — Blitzstein Bootcamp interactivo

Instancia de [cwc-cool-workshop-course](https://github.com/BernardUriza/cwc-cool-workshop-course)
para el bootcamp. Las lecciones reflejan el material YA cubierto en sesiones de
estudio y el quiz de repaso es el ritual de retrieval practice.

```bash
cd curso && python3 -m http.server 8000
open http://localhost:8000
```

El contenido se edita en `content/` (una lección por capítulo/sección cubierta +
banco de preguntas en `quizzes.json`). El motor en `engine/` se actualiza desde
el template, nunca a mano.

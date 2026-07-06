# Quiz HTML interactivo para retrieval practice

Status: Done
Proposed: 2026-07-05 by Bernard

## What it is

Formularios HTML self-contained (estilo PROGRESO.html) para el ritual de retrieval
practice: Claude genera un quiz por sesión con las preguntas del material cubierto,
Bernard responde en el browser, el form califica y muestra la corrección. Resuelve de
paso el problema de notación: la terminal no renderiza LaTeX, pero un HTML con KaTeX/
MathJax embebido sí muestra A ∩ B, C(n,k), integrales, etc. como fórmulas reales.

## Canonical path to reuse (Art. 6)

Mismo patrón que PROGRESO.html: HTML self-contained en el repo, datos del quiz en un
bloque `<script type="application/json">`, render con vanilla JS, paleta y dark mode
del dashboard. KaTeX embebido (self-hosted, sin CDN) para las fórmulas. Un archivo por
quiz en `quizzes/chXX-<slug>.html`, resultados anotados de vuelta en el JSON de
PROGRESO.html.

## The decision that's the owner's

Ninguna irreversible. Detalle a decidir en la primera implementación: si el resultado
del quiz se registra a mano en PROGRESO.html o el quiz genera un blob para pegar.

## Status / next step

Done (2026-07-05, mismo día): se construyó como parte del template
cwc-cool-workshop-course (github.com/BernardUriza/cwc-cool-workshop-course) y vive
instanciado en `curso/` — quiz con muestreo 1+2+2, KaTeX self-hosted, XP y registro
de runs. Superó la propuesta original: en vez de un HTML suelto por quiz, es el
módulo retrieval del motor del curso.

# Blitzstein-ML

Probability bootcamp (jul–dic 2026) → prep para **CS 391L Machine Learning**, UT Austin MSAI
(Spring 2027 cohort). Plan maestro: `SerenityOps/msai-application-2027/PLAN_CURSOS.md`.

**Regla del repo: nada pasivo.** Cada capítulo produce artefactos: notas propias, ejercicios
resueltos a mano, y el algoritmo de ML correspondiente implementado desde cero en numpy.

## El curso con exámenes (lo joinable)

**[edX HarvardX Stat110x — Introduction to Probability](https://www.edx.org/learn/probability/harvard-university-introduction-to-probability)**
— del propio Blitzstein, self-paced, con ejercicios calificados y exámenes.
Audit gratis; certificado verificado $209 (decidir al llegar a mitad — solo si el
proof-of-work del certificado vale más que el papel).

Mapeo directo libro ↔ curso: mismo autor, mismos capítulos.

## Estructura

| Carpeta | Libro | Produce |
|---|---|---|
| `ch01-probability-counting/` | Cap 1 | notas + ejercicios |
| `ch02-conditional-probability/` | Cap 2 (Bayes) | notas + ejercicios |
| `ch03-random-variables/` | Cap 3 | notas + ejercicios |
| `ch04-expectation/` | Cap 4 | notas + ejercicios + **regresión logística en numpy** |
| `ch05-continuous/` | Cap 5 (normal, exponencial) | notas + ejercicios + **MLE en numpy** |
| `ch07-joint-distributions/` | Cap 7 (joint, covarianza) | notas + ejercicios + **GMM/EM en numpy** |
| `implementations/` | — | los algoritmos de CS 391L desde cero (numpy puro, sin sklearn) |
| `mock-exams/` | — | exámenes reales de MIT auto-aplicados, con timer de 2h |

## Mock exams (condiciones de examen real)

[MIT 18.600 Fall 2019](https://ocw.mit.edu/courses/18-600-probability-and-random-variables-fall-2019/pages/exams/)
publica midterms y final **con soluciones**. Checkpoints:

- **Fin de oct 2026**: Midterm 1 de 18.600 (caps 1-4) — 2 horas, sin pausa, notas impresas (simula el formato CS 391L)
- **Fin de dic 2026**: Midterm 2 + secciones de probabilidad del final

Aprobado = >70% honesto. Reprobado = re-estudiar el capítulo débil antes de avanzar.

## Cadencia

~2 capítulos/mes, jul→oct 2026. Ejercicios: los "Strategic Practice" de
[stat110.hsites.harvard.edu](https://stat110.hsites.harvard.edu/) + impares del libro
(tienen solución pública para verificar).

## Spice opcional (sin compromiso)

[Jane Street monthly puzzle](https://www.janestreet.com/puzzles/) — puzzle mensual con sabor
probabilístico, respuesta objetiva, lista pública de solvers. Si un mes el puzzle cae en tema
ya estudiado, intentarlo. NO es meta — es termómetro.

## Recursos

- Libro: [Introduction to Probability, Blitzstein & Hwang](http://probabilitybook.net/) (PDF oficial gratis)
- Curso edX: [Stat110x](https://www.edx.org/learn/probability/harvard-university-introduction-to-probability)
- Mock exams: [MIT 18.600](https://ocw.mit.edu/courses/18-600-probability-and-random-variables-fall-2019/) · [MIT 6.041SC](https://ocw.mit.edu/courses/6-041sc-probabilistic-systems-analysis-and-applied-probability-fall-2013/)
- Siguiente fase (nov-dic 2026): ALAFF caps 1,2,9 → PCA/SVD

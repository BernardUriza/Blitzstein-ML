# PromptCraft - Playground Page
# Página del playground de prompts

from browser import document, html, timer
from ..state import get_state
from ..components.code_editor import PromptEditor
from ..components.tabs import Tabs
from ..components.button import Button
from ..components.toast import success, info
from ..gamification.achievements import check_achievements


def playground_page(params):
    """
    Renderiza la página del playground.

    Args:
        params: Parámetros de la ruta

    Returns:
        Elemento DOM de la página
    """
    state = get_state()

    # Registrar uso del playground
    check_achievements(state, 'playground_use', {})

    container = html.DIV(Class="max-w-6xl mx-auto")

    # Header
    header = html.DIV(Class="mb-6")
    header <= html.H1("🎮 Playground", Class="text-3xl font-bold text-gray-100 mb-2")
    header <= html.P(
        "Experimenta con diferentes técnicas de prompting en un ambiente seguro.",
        Class="text-gray-400"
    )
    container <= header

    # Layout principal
    main_layout = html.DIV(Class="grid grid-cols-1 lg:grid-cols-3 gap-6")

    # Editor (2/3)
    editor_section = _render_editor_section()
    main_layout <= editor_section

    # Sidebar (1/3)
    sidebar = _render_sidebar()
    main_layout <= sidebar

    container <= main_layout

    # Templates
    templates = _render_templates()
    container <= templates

    return container


def _render_editor_section():
    """Renderiza la sección del editor."""
    section = html.DIV(Class="lg:col-span-2 space-y-4")

    # Editor de prompt
    editor_card = html.DIV(Class="bg-gray-800 rounded-xl p-4 border border-gray-700")
    editor_card <= html.H3("Tu Prompt", Class="font-medium text-gray-300 mb-3")

    editor = PromptEditor(
        value="",
        placeholder="Escribe tu prompt aquí...\n\nPuedes experimentar con diferentes técnicas:\n- Zero-shot\n- Few-shot\n- Chain of Thought\n- Role-playing",
        min_height=200,
        show_run_button=True,
        on_run=_on_run_prompt,
        label=""
    )
    editor_card <= editor.render()
    section <= editor_card

    # Resultado
    result_card = html.DIV(Class="bg-gray-800 rounded-xl p-4 border border-gray-700")
    result_card <= html.H3("Resultado", Class="font-medium text-gray-300 mb-3")
    result_card <= html.DIV(
        html.P(
            "El resultado de tu prompt aparecerá aquí. Haz clic en 'Ejecutar' para ver la respuesta simulada.",
            Class="text-gray-400 italic"
        ),
        Class="min-h-[150px] p-4 bg-gray-900 rounded-lg",
        id="playground-result"
    )
    section <= result_card

    return section


def _render_sidebar():
    """Renderiza la barra lateral."""
    sidebar = html.DIV(Class="space-y-4")

    # Técnicas rápidas
    techniques_card = html.DIV(Class="bg-gray-800 rounded-xl p-4 border border-gray-700")
    techniques_card <= html.H3("Técnicas", Class="font-medium text-gray-300 mb-3")

    techniques = [
        ('zero-shot', 'Zero-Shot', 'Sin ejemplos previos'),
        ('few-shot', 'Few-Shot', 'Con ejemplos'),
        ('cot', 'Chain of Thought', 'Razonamiento paso a paso'),
        ('role', 'Role-Playing', 'Asignar un rol'),
    ]

    for tech_id, name, desc in techniques:
        tech_btn = html.DIV(
            html.SPAN(name, Class="font-medium text-gray-300 block") +
            html.SPAN(desc, Class="text-xs text-gray-400"),
            Class="p-3 border border-gray-700 rounded-lg hover:border-indigo-600 hover:bg-indigo-900/40 cursor-pointer transition-colors mb-2"
        )
        tech_btn.bind('click', lambda e, t=tech_id: _insert_technique(t))
        techniques_card <= tech_btn

    sidebar <= techniques_card

    # Consejos
    tips_card = html.DIV(Class="bg-amber-950/40 rounded-xl p-4 border border-amber-800")
    tips_card <= html.H3("💡 Consejos", Class="font-medium text-amber-300 mb-3")

    tips = [
        "Sé específico sobre lo que quieres.",
        "Proporciona contexto relevante.",
        "Indica el formato de salida deseado.",
        "Usa ejemplos cuando sea posible.",
    ]

    tips_list = html.UL(Class="space-y-2 text-sm text-amber-200")
    for tip in tips:
        tips_list <= html.LI(f"• {tip}")
    tips_card <= tips_list

    sidebar <= tips_card

    # Historial
    history_card = html.DIV(Class="bg-gray-800 rounded-xl p-4 border border-gray-700")
    history_card <= html.H3("Historial", Class="font-medium text-gray-300 mb-3")
    history_card <= html.P(
        "Tu historial de prompts aparecerá aquí.",
        Class="text-sm text-gray-400 italic"
    )
    sidebar <= history_card

    return sidebar


def _render_templates():
    """Renderiza templates de ejemplo."""
    section = html.DIV(Class="mt-8")
    section <= html.H2("📋 Templates de Ejemplo", Class="text-xl font-semibold text-gray-100 mb-4")

    templates = [
        {
            'name': 'Resumen de Texto',
            'icon': '📝',
            'prompt': 'Resume el siguiente texto en 3 puntos principales:\n\n[Tu texto aquí]'
        },
        {
            'name': 'Generación de Código',
            'icon': '💻',
            'prompt': 'Actúa como un desarrollador senior.\n\nEscribe una función en Python que:\n- [Requisito 1]\n- [Requisito 2]\n\nIncluye comentarios y manejo de errores.'
        },
        {
            'name': 'Análisis de Problema',
            'icon': '🔍',
            'prompt': 'Analiza el siguiente problema paso a paso:\n\n[Problema]\n\n1. Primero, identifica...\n2. Luego, considera...\n3. Finalmente, propón...'
        },
        {
            'name': 'Revisión de Contenido',
            'icon': '✅',
            'prompt': 'Revisa el siguiente texto y sugiere mejoras:\n\n[Texto]\n\nEnfócate en:\n- Claridad\n- Gramática\n- Fluidez'
        },
    ]

    grid = html.DIV(Class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4")

    for template in templates:
        card = html.DIV(
            html.SPAN(template['icon'], Class="text-2xl mb-2 block") +
            html.SPAN(template['name'], Class="font-medium text-gray-300"),
            Class="p-4 bg-gray-800 border border-gray-700 rounded-lg text-center hover:border-indigo-600 hover:bg-indigo-900/40 cursor-pointer transition-colors"
        )
        card.bind('click', lambda e, p=template['prompt']: _load_template(p))
        grid <= card

    section <= grid

    return section


def _on_run_prompt(prompt):
    """Ejecuta el prompt (simulado)."""
    result_elem = document.getElementById("playground-result")
    if not result_elem:
        return

    result_elem.innerHTML = ""
    result_elem.className = "min-h-[150px] p-4 bg-gray-900 rounded-lg"
    result_elem <= html.P("⏳ Procesando prompt...", Class="text-gray-400")

    def show_result():
        result_elem.innerHTML = ""

        if not prompt.strip():
            result_elem <= html.P(
                "Por favor, escribe un prompt para ver el resultado.",
                Class="text-gray-400 italic"
            )
            return

        # Simular respuesta basada en el prompt
        response = _generate_mock_response(prompt)

        result_elem.className = "min-h-[150px] p-4 bg-green-950/40 rounded-lg border border-green-800"
        result_elem <= html.P("✅ Respuesta simulada:", Class="text-green-300 font-medium mb-2")
        result_elem <= html.P(response, Class="text-gray-300 whitespace-pre-wrap")

        info("Prompt ejecutado exitosamente")

    timer.set_timeout(show_result, 1500)


def _generate_mock_response(prompt):
    """Genera una respuesta simulada."""
    prompt_lower = prompt.lower()

    if 'resume' in prompt_lower or 'resumen' in prompt_lower:
        return "Aquí está el resumen en 3 puntos:\n\n1. Punto principal identificado del texto.\n2. Segundo aspecto relevante mencionado.\n3. Conclusión o llamada a la acción."

    elif 'código' in prompt_lower or 'python' in prompt_lower or 'función' in prompt_lower:
        return "```python\ndef ejemplo_funcion(parametro):\n    \"\"\"\n    Función de ejemplo.\n    \"\"\"\n    resultado = parametro * 2\n    return resultado\n```\n\nEsta función toma un parámetro y retorna su doble."

    elif 'analiza' in prompt_lower or 'problema' in prompt_lower:
        return "Análisis del problema:\n\n1. **Identificación**: El problema principal es...\n2. **Causas**: Las posibles causas incluyen...\n3. **Soluciones**: Se proponen las siguientes alternativas..."

    elif 'revisa' in prompt_lower or 'mejora' in prompt_lower:
        return "Sugerencias de mejora:\n\n- ✓ La estructura es clara\n- → Considera usar oraciones más cortas\n- → Añade conectores entre párrafos\n- ✓ El tono es apropiado"

    else:
        return f"He procesado tu prompt de {len(prompt)} caracteres.\n\nEn una implementación real, aquí aparecería la respuesta del modelo de IA basada en tu instrucción.\n\n💡 Tip: Prueba ser más específico para mejores resultados."


def _insert_technique(technique):
    """Inserta un template de técnica."""
    templates = {
        'zero-shot': "Realiza la siguiente tarea:\n\n[Descripción de la tarea]\n\nResponde de manera clara y concisa.",
        'few-shot': "Ejemplos:\n\nEntrada: ejemplo1\nSalida: resultado1\n\nEntrada: ejemplo2\nSalida: resultado2\n\nAhora procesa:\nEntrada: [tu caso]\nSalida:",
        'cot': "Resuelve el siguiente problema paso a paso:\n\n[Problema]\n\nPiensa en voz alta y muestra tu razonamiento antes de dar la respuesta final.",
        'role': "Actúa como un [rol específico] con experiencia en [área].\n\nTu tarea es:\n[Descripción]\n\nResponde desde la perspectiva de ese rol."
    }

    prompt = templates.get(technique, "")
    if prompt:
        # En una implementación real, esto llenaría el editor
        info(f"Template '{technique}' listo para usar")


def _load_template(prompt):
    """Carga un template en el editor."""
    # En una implementación real, esto llenaría el editor
    info("Template cargado. Personalízalo según tus necesidades.")

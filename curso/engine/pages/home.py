# CWC - Home Page

from browser import html, window
from ..state import get_state
from ..router import navigate
from ..config import get_config, feature_enabled
from ..lessons.loader import get_loader


def home_page(params):
    state = get_state()
    level_info = state.get_level_info()

    container = html.DIV(Class="space-y-8")
    container <= _render_hero(state, level_info)
    container <= _render_quick_actions()
    container <= _render_progress_overview(state)
    container <= _render_continue_learning(state)

    return container


def _render_hero(state, level_info):
    config = get_config()
    hero = html.DIV(Class="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-2xl p-8 text-white")

    hour = window.Date.new().getHours()
    if hour < 12:
        greeting = "¡Buenos días"
    elif hour < 18:
        greeting = "¡Buenas tardes"
    else:
        greeting = "¡Buenas noches"

    username = state.data.get('user', {}).get('username', 'estudiante')
    hero <= html.H1(f"{greeting}, {username}! 👋", Class="text-2xl font-bold mb-2")
    hero <= html.P(config['tagline'], Class="text-indigo-100 mb-6")

    stats_row = html.DIV(Class="grid grid-cols-3 gap-4")
    stats_row <= html.DIV(
        html.SPAN(f"Nivel {level_info['level']}", Class="block text-2xl font-bold") +
        html.SPAN(level_info['title'], Class="text-indigo-200 text-sm"),
        Class="text-center"
    )
    xp_total = state.data.get('progress', {}).get('xp', 0)
    stats_row <= html.DIV(
        html.SPAN(str(xp_total), Class="block text-2xl font-bold") +
        html.SPAN("XP Total", Class="text-indigo-200 text-sm"),
        Class="text-center"
    )
    streak = state.data.get('streak', {}).get('current', 0)
    stats_row <= html.DIV(
        html.SPAN("🔥 " + str(streak), Class="block text-2xl font-bold") +
        html.SPAN("Días de racha", Class="text-indigo-200 text-sm"),
        Class="text-center"
    )
    hero <= stats_row

    xp_section = html.DIV(Class="mt-6")
    xp_section <= html.DIV(
        html.DIV(
            Class="h-full bg-white/30 rounded-full transition-all",
            style=f"width: {level_info['progress']}%"
        ),
        Class="w-full h-3 bg-white/20 rounded-full overflow-hidden"
    )
    xp_section <= html.P(
        f"{level_info['xp_in_level']} / {level_info['xp_for_next']} XP para nivel {level_info['level'] + 1}",
        Class="text-sm text-indigo-200 mt-2 text-center"
    )
    hero <= xp_section

    return hero


def _render_quick_actions():
    section = html.DIV(Class="space-y-4")
    section <= html.H2("Explora el Curso", Class="text-lg font-semibold text-gray-100")

    actions = []
    if feature_enabled('lessons'):
        actions.append(('📚', 'Lecciones', 'lessons', 'bg-blue-950/40 hover:bg-blue-900/60 border-blue-800'))
    if feature_enabled('practice'):
        actions.append(('✍️', 'Práctica', 'practice', 'bg-teal-950/40 hover:bg-teal-900/60 border-teal-800'))
    if feature_enabled('retrieval'):
        actions.append(('🧠', 'Quiz de Repaso', 'quiz', 'bg-rose-950/40 hover:bg-rose-900/60 border-rose-800'))
    if feature_enabled('puzzles'):
        actions.append(('🧩', 'Puzzles', 'puzzles', 'bg-purple-950/40 hover:bg-purple-900/60 border-purple-800'))
    if feature_enabled('playground'):
        actions.append(('🎮', 'Playground', 'playground', 'bg-green-950/40 hover:bg-green-900/60 border-green-800'))
    if feature_enabled('assessment'):
        actions.append(('📝', 'Test Inicial', 'assessment', 'bg-orange-950/40 hover:bg-orange-900/60 border-orange-800'))
    if feature_enabled('final_project'):
        actions.append(('🎓', 'Proyecto Final', 'final-project', 'bg-indigo-950/40 hover:bg-indigo-900/60 border-indigo-800'))
    actions.append(('🏆', 'Badges', 'badges', 'bg-yellow-950/40 hover:bg-yellow-900/60 border-yellow-800'))

    grid = html.DIV(Class="grid grid-cols-2 md:grid-cols-4 gap-4")
    for icon, label, route, colors in actions:
        card = html.DIV(
            html.SPAN(icon, Class="text-3xl mb-2 block") +
            html.SPAN(label, Class="font-medium text-gray-300"),
            Class=f"p-6 rounded-xl border text-center cursor-pointer transition-colors {colors}"
        )
        card.bind('click', lambda e, r=route: navigate(r))
        grid <= card
    section <= grid

    return section


def _render_progress_overview(state):
    from ..config import http_get_json

    section = html.DIV(Class="bg-gray-800 rounded-xl p-6 border border-gray-700")
    section <= html.H2("Tu Progreso", Class="text-lg font-semibold text-gray-100 mb-4")

    progress_grid = html.DIV(Class="grid grid-cols-1 md:grid-cols-3 gap-4")

    lessons_completed = len(state.data.get('progress', {}).get('lessons_completed', []))
    total_lessons = get_loader().get_lesson_count()

    puzzles_solved = len(state.data.get('progress', {}).get('puzzles_solved', {}))
    puzzle_index = http_get_json('content/puzzles/index.json') or {}
    total_puzzles = len(puzzle_index.get('puzzles', []))

    badges_unlocked = len(state.data.get('badges', []))
    from ..gamification.badges import get_all_badges
    total_badges = len(get_all_badges())

    tiles = [
        ('📖', lessons_completed, total_lessons, 'Lecciones', 'bg-blue-500', 'bg-blue-950/40'),
        ('🧩', puzzles_solved, total_puzzles, 'Puzzles', 'bg-purple-500', 'bg-purple-950/40'),
        ('🏆', badges_unlocked, total_badges, 'Badges', 'bg-yellow-500', 'bg-yellow-950/40'),
    ]

    for icon, done, total, label, bar_color, tile_color in tiles:
        pct = (done / total * 100) if total else 0
        progress_grid <= html.DIV(
            html.DIV(
                html.SPAN(icon, Class="text-2xl") +
                html.DIV(
                    html.SPAN(f"{done}/{total}", Class="font-bold text-gray-100") +
                    html.SPAN(f" {label}", Class="text-gray-400 text-sm"),
                    Class="ml-3"
                ),
                Class="flex items-center mb-2"
            ) +
            html.DIV(
                html.DIV(Class=f"h-full {bar_color} rounded-full", style=f"width: {pct}%"),
                Class="w-full h-2 bg-gray-700 rounded-full overflow-hidden"
            ),
            Class=f"p-4 {tile_color} rounded-lg"
        )

    section <= progress_grid
    return section


def _render_continue_learning(state):
    section = html.DIV(Class="bg-gray-800 rounded-xl p-6 border border-gray-700")
    section <= html.H2("Continuar Aprendiendo", Class="text-lg font-semibold text-gray-100 mb-4")

    suggestions = html.DIV(Class="grid grid-cols-1 md:grid-cols-2 gap-4")

    completed = set(state.data.get('progress', {}).get('lessons_completed', []))
    next_lesson = None
    for lesson in get_loader().get_all_lessons():
        if lesson['id'] not in completed:
            next_lesson = lesson
            break

    if next_lesson:
        lesson_card = html.DIV(
            html.DIV(
                html.SPAN("📚", Class="text-xl") +
                html.SPAN("Próxima Lección", Class="ml-2 font-medium text-gray-300"),
                Class="flex items-center mb-2"
            ) +
            html.P(next_lesson['title'], Class="text-gray-400 text-sm mb-3") +
            html.BUTTON("Continuar →", Class="text-sm text-indigo-400 font-medium hover:text-indigo-200"),
            Class="p-4 border border-gray-700 rounded-lg hover:border-indigo-600 cursor-pointer transition-colors"
        )
        lesson_card.bind('click', lambda e, lid=next_lesson['id']: navigate('lesson/:id', {'id': lid}))
        suggestions <= lesson_card
    else:
        suggestions <= html.DIV(
            html.P("🎉 Completaste todas las lecciones.", Class="text-gray-400"),
            Class="p-4 border border-green-800 bg-green-950/40 rounded-lg"
        )

    if feature_enabled('retrieval'):
        quiz_card = html.DIV(
            html.DIV(
                html.SPAN("🧠", Class="text-xl") +
                html.SPAN("Quiz de Repaso", Class="ml-2 font-medium text-gray-300"),
                Class="flex items-center mb-2"
            ) +
            html.P("Recuerda lo que ya cubriste: 5 preguntas mezclando reciente y antiguo.", Class="text-gray-400 text-sm mb-3") +
            html.BUTTON("Empezar →", Class="text-sm text-rose-400 font-medium hover:text-rose-200"),
            Class="p-4 border border-gray-700 rounded-lg hover:border-rose-600 cursor-pointer transition-colors"
        )
        quiz_card.bind('click', lambda e: navigate('quiz'))
        suggestions <= quiz_card

    section <= suggestions
    return section

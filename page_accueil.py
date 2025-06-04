from flet import*
from datetime import datetime

BG = "#041955"
FWG = "#FFFFFF"
FG = "#3450a1"
PINK = "#eb06ff"

def page_accueil(page: Page):
    page.bgcolor = BG

    # Check if user is teacher
    user = page.session.get("user") or {"profession": "Inconnu", "nom": "Inconnu"}
    if user["profession"] != "Enseignant":
        return [Text("Accès réservé aux enseignants", color="red", size=20)]

    menu_items = [
        PopupMenuItem(icon=icons.HOME, text="Accueil", on_click=lambda _: page.go('/page_accueil')),
        PopupMenuItem(icon=icons.WIDGETS, text="À propos de", on_click=lambda _: page.go('/page_a_propos')),
        PopupMenuItem(icon=icons.PERSON, text="Profil", on_click=lambda _: page.go('/page_profil')),
        PopupMenuItem(icon=icons.EXIT_TO_APP, text="Déconnexion", on_click=lambda _: page.go('/page1')),
    ]

    page.appbar = AppBar(
        leading=PopupMenuButton(icon=icons.MENU, icon_color="white", items=menu_items),
        leading_width=40,
        bgcolor=colors.INDIGO,
        actions=[IconButton(icons.NOTIFICATION_ADD_OUTLINED, icon_color="WHITE", on_click=lambda _: page.go('/page_notif'))],
    )

    def navigation_changed(e):
        if e.control.selected_index == 0:
            page.go("/page_accueil")
        elif e.control.selected_index == 1:
            page.go("/page_emploi_temps")
        elif e.control.selected_index == 2:
            page.go("/page_statistiques")
        elif e.control.selected_index == 3:
            page.go("/page_profil")
        elif e.control.selected_index == 4:
            page.go("/page_liste_etudiants")

    navigation_bar = CupertinoNavigationBar(
        bgcolor=colors.WHITE,
        inactive_color=colors.BLACK,
        active_color=colors.BLUE,
        on_change=navigation_changed,
        destinations=[
            NavigationBarDestination(icon=Icon(icons.HOME_ROUNDED, color="black"), selected_icon=Icon(icons.HOME_ROUNDED, color="BLUE"), label="Accueil"),
            NavigationBarDestination(icon=Icon(icons.CALENDAR_TODAY, color="black"), selected_icon=Icon(icons.CALENDAR_TODAY, color="BLUE"), label="Emploi du temps"),
            NavigationBarDestination(icon=Icon(icons.SHOW_CHART, color="black"), selected_icon=Icon(icons.SHOW_CHART, color="BLUE"), label="Statistiques"),
            NavigationBarDestination(icon=Icon(icons.PERSON_2, color="black"), selected_icon=Icon(icons.PERSON_2, color="BLUE"), label="Profil"),
            NavigationBarDestination(icon=Icon(icons.LIST, color="black"), selected_icon=Icon(icons.LIST, color="BLUE"), label="Étudiants"),
        ],
    )

    content1 = Column(
        controls=[
            Text(
                spans=[TextSpan("PAGE D'ACCUEIL", TextStyle(size=24, weight=FontWeight.BOLD, foreground=Paint(gradient=PaintLinearGradient((0, 20), (150, 20), [colors.PURPLE, colors.WHITE]))))],
            ),
            Text(f"Bienvenue {user['nom']}", color=FWG, size=20, weight=FontWeight.BOLD),
            Row(
                [
                    Container(
                        content=Column([Text("LISTE DES ÉTUDIANTS", color=FWG, size=12, weight=FontWeight.BOLD), Container(width=160, height=5, bgcolor=PINK, border_radius=20)]),
                        border_radius=20,
                        bgcolor=BG,
                        height=171,
                        width=170,
                        padding=15,
                        ink=True,
                        on_click=lambda _: page.go('/page_liste_etudiants')
                    ),
                    Container(
                        content=Column([Text("VOIR LISTE DE PRÉSENCE", color=FWG, size=12, weight=FontWeight.BOLD), Container(width=160, height=5, bgcolor=PINK, border_radius=20)]),
                        border_radius=20,
                        bgcolor=BG,
                        height=171,
                        width=170,
                        padding=15,
                        ink=True,
                        on_click=lambda _: page.go('/page_liste_de_presence')
                    ),
                    Container(
                        content=Column([Text("GÉNÉRER PRÉSENCE", color=FWG, size=12, weight=FontWeight.BOLD), Container(width=160, height=5, bgcolor=PINK, border_radius=20)]),
                        border_radius=20,
                        bgcolor=BG,
                        height=171,
                        width=170,
                        padding=15,
                        ink=True,
                        on_click=lambda _: page.go('/page_generer_liste')
                    ),
                ], expand=True
            ),
            FloatingActionButton(icon=icons.ADD, bgcolor=colors.WHITE, on_click=lambda _: page.go('/page_generer_liste'))
        ]
    )

    return [content1, navigation_bar, page.appbar]
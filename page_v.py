import flet as ft

BG = "#041955"
BULLE = '#2BC2A9'
TEXT_WHITE = 'white'
TEXT_BLACK = 'black'

def page_v(page: ft.Page):
    page.bgcolor = BG
    page.adaptive = True

    # Vérifier si l'utilisateur est un administrateur
    user = page.session.get("user") or {"profession": "Inconnu"}
    if user["profession"] != "Administrateur":
        return [ft.Text("Accès réservé aux administrateurs", color="red", size=20)]

    # Navigation
    def navigation_changed(e):
        if e.control.selected_index == 0:
            page.go("/page_c")  # Accueil admin
        elif e.control.selected_index == 1:
            page.go("/page_d")  # Gestion utilisateurs
        elif e.control.selected_index == 2:
            page.go("/page_statistiques_admin")  # Statistiques
        elif e.control.selected_index == 3:
            page.go("/page_v")  # À propos

    navigation_bar = ft.CupertinoNavigationBar(
        bgcolor=ft.colors.WHITE,
        inactive_color=ft.colors.BLACK,
        active_color=ft.colors.BLUE,
        on_change=navigation_changed,
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icon(ft.icons.HOME_ROUNDED, color="black"),
                selected_icon=ft.Icon(ft.icons.HOME_ROUNDED, color="BLUE"),
                label="Accueil"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icon(ft.icons.PEOPLE, color="black"),
                selected_icon=ft.Icon(ft.icons.PEOPLE, color="BLUE"),
                label="Utilisateurs"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icon(ft.icons.SHOW_CHART, color="black"),
                selected_icon=ft.Icon(ft.icons.SHOW_CHART, color="BLUE"),
                label="Statistiques"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icon(ft.icons.INFO, color="black"),
                selected_icon=ft.Icon(ft.icons.INFO, color="BLUE"),
                label="À propos"
            ),
        ],
    )

    about_content = ft.Column(
        controls=[
            ft.Text(
                "À propos de l'application",
                color=BULLE,
                size=24,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Text(
                "Cette application est conçue pour simplifier la gestion des listes de présence et des emplois du temps.",
                color=TEXT_WHITE,
                size=16,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Text(
                "Fonctionnalités principales :",
                color=TEXT_WHITE,
                size=16,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.LEFT,
            ),
            ft.ListView(
                controls=[
                    ft.ListTile(title=ft.Text("Gestion des listes de présence", color=TEXT_WHITE)),
                    ft.ListTile(title=ft.Text("Génération de rapports", color=TEXT_WHITE)),
                    ft.ListTile(title=ft.Text("Visualisation des statistiques", color=TEXT_WHITE)),
                    ft.ListTile(title=ft.Text("Gestion des emplois du temps", color=TEXT_WHITE)),
                ],
                expand=True,
            ),
            ft.Text(
                "Version : 1.0.0",
                color=TEXT_WHITE,
                size=14,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Text(
                "Développé par :",
                color=TEXT_WHITE,
                size=16,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Text(
                "Étudiants Licence 3 SI",
                color=TEXT_WHITE,
                size=14,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Text(
                "Contact : 0101625160 / 0141973436 / 0707779756 / 0502081881",
                color=TEXT_WHITE,
                size=14,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Text(
                "© 2025 Tous droits réservés.",
                color=TEXT_WHITE,
                size=12,
                text_align=ft.TextAlign.CENTER,
            ),
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        scroll='auto'
    )

    tout = ft.Column(
        controls=[
            ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color=TEXT_WHITE, on_click=lambda _: page.go('/page_c')),
            about_content,
            navigation_bar
        ],
        expand=True
    )

    return [tout]
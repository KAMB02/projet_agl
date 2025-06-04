import flet as ft

BG = "#041955"
BULLE = '#2BC2A9'
TEXT_WHITE = 'white'

def page_a_propos(page: ft.Page):
    page.title = "À propos"
    page.bgcolor = BG

    # Check if user is teacher
    user = page.session.get("user") or {"profession": "Inconnu"}
    if user["profession"] != "Enseignant":
        return [ft.Text("Accès réservé aux enseignants", color="red", size=20)]

    about_content = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=20,
        controls=[
            ft.Text("À propos de l'application", size=30, weight=ft.FontWeight.BOLD, color=TEXT_WHITE),
            ft.Text("Cette application est conçue pour simplifier la gestion des listes de présence et des emplois du temps.", color=TEXT_WHITE, size=16),
            ft.Text("Fonctionnalités principales", size=24, weight=ft.FontWeight.BOLD, color=BULLE),
            ft.ListView(
                controls=[
                    ft.ListTile(title=ft.Text("Pointage des étudiants", color=TEXT_WHITE), bgcolor=ft.colors.WHITE),
                    ft.ListTile(title=ft.Text("Gestion de la liste de présence", color=TEXT_WHITE), bgcolor=ft.colors.WHITE),
                    ft.ListTile(title=ft.Text("Visualisation des statistiques", color=TEXT_WHITE), bgcolor=ft.colors.WHITE),
                    ft.ListTile(title=ft.Text("Gestion des emplois du temps", color=TEXT_WHITE), bgcolor=ft.colors.WHITE),
                ],
                spacing=10,
            ),
            ft.Text("Notre équipe", size=24, weight=ft.FontWeight.BOLD, color=BULLE),
            ft.Row(
                controls=[
                    ft.Column(
                        controls=[ft.Text("DAO KARIM", size=16, weight=ft.FontWeight.BOLD, color=TEXT_WHITE), ft.Text("Développeur principal", size=14, color=TEXT_WHITE)],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Column(
                        controls=[ft.Text("Gneto Grace", size=16, weight=ft.FontWeight.BOLD, color=TEXT_WHITE), ft.Text("Designer UX/UI", size=14, color=TEXT_WHITE)],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Column(
                        controls=[ft.Text("Hamed Meloua", size=16, weight=ft.FontWeight.BOLD, color=TEXT_WHITE), ft.Text("Chef de Projet", size=14, color=TEXT_WHITE)],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Column(
                        controls=[ft.Text("Kadjo Bienvenue", size=16, weight=ft.FontWeight.BOLD, color=TEXT_WHITE), ft.Text("Analyste", size=14, color=TEXT_WHITE)],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                spacing=50,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Text("Contactez-nous", size=24, weight=ft.FontWeight.BOLD, color=BULLE),
            ft.Text("Pour toute question, contactez-nous à : projetpointage@gmail.com", size=16, color=TEXT_WHITE),
            ft.Text("© 2025 Tous droits réservés.", size=12, color=TEXT_WHITE, text_align=ft.TextAlign.CENTER),
        ],
    )

    # Navigation bar
    navigation_bar = ft.CupertinoNavigationBar(
        bgcolor=ft.colors.WHITE,
        inactive_color=ft.colors.BLACK,
        active_color=ft.colors.BLUE,
        on_change=lambda e: (
            page.go("/page_accueil") if e.control.selected_index == 0 else
            page.go("/page_emploi_temps") if e.control.selected_index == 1 else
            page.go("/page_statistiques") if e.control.selected_index == 2 else
            page.go("/page_profil") if e.control.selected_index == 3 else
            page.go("/page_liste_etudiants") if e.control.selected_index == 4 else None
        ),
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icon(ft.icons.HOME_ROUNDED, color="black"), selected_icon=ft.Icon(ft.icons.HOME_ROUNDED, color="BLUE"), label="Accueil"),
            ft.NavigationBarDestination(icon=ft.Icon(ft.icons.CALENDAR_TODAY, color="black"), selected_icon=ft.Icon(ft.icons.CALENDAR_TODAY, color="BLUE"), label="Emploi du temps"),
            ft.NavigationBarDestination(icon=ft.Icon(ft.icons.SHOW_CHART, color="black"), selected_icon=ft.Icon(ft.icons.SHOW_CHART, color="BLUE"), label="Statistiques"),
            ft.NavigationBarDestination(icon=ft.Icon(ft.icons.PERSON_2, color="black"), selected_icon=ft.Icon(ft.icons.PERSON_2, color="BLUE"), label="Profil"),
            ft.NavigationBarDestination(icon=ft.Icon(ft.icons.LIST, color="black"), selected_icon=ft.Icon(ft.icons.LIST, color="BLUE"), label="Étudiants"),
        ],
    )

    return [
        ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color=TEXT_WHITE, on_click=lambda _: page.go('/page_accueil')),
        about_content,
        navigation_bar
    ]
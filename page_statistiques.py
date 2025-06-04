import flet as ft
import mysql.connector
from mysql.connector import Error

BG = "#041955"
BULLE = '#2BC2A9'
TEXT_WHITE = 'white'

def fetch_statistics(teacher_email):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='donnee_app',
            user='root',
            password='Kamssone25',
            port='3308'
        )
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT u.nom, u.prenom, COUNT(pl.is_present) as nb_presences
            FROM presence_list pl
            JOIN utilisateurs u ON pl.student_email = u.email
            WHERE pl.teacher_email = %s AND pl.is_present = TRUE
            GROUP BY u.email
            """,
            (teacher_email,)
        )
        stats = cursor.fetchall()
        cursor.close()
        connection.close()
        return stats
    except Error as e:
        print(f"Erreur lors de la récupération des statistiques: {e}")
        return None

def page_statistiques(page: ft.Page):
    page.bgcolor = BG

    # Check if user is teacher
    user = page.session.get("user") or {"profession": "Inconnu", "email": "inconnu@example.com"}
    if user["profession"] != "Enseignant":
        return [ft.Text("Accès réservé aux enseignants", color="red", size=20)]

    title = ft.Text("STATISTIQUES", size=30, color=TEXT_WHITE, weight=ft.FontWeight.BOLD)
    content = ft.Column(
        controls=[title, ft.Text("Choisissez une option :", color=TEXT_WHITE)],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    stat1 = ft.ElevatedButton(text="STATISTIQUE EN COURBE", on_click=lambda e: page.go('/page_stat1'), bgcolor=BULLE, color=TEXT_WHITE)
    stat2 = ft.ElevatedButton(text="STATISTIQUE EN DIAGRAMME", on_click=lambda e: page.go('/page_stat2'), bgcolor=BULLE, color=TEXT_WHITE)

    def handle_expansion_tile_change(e):
        page.open(ft.SnackBar(ft.Text(f"ExpansionTile was {'expanded' if e.data=='true' else 'collapsed'}"), duration=1000))
        if e.control.trailing:
            e.control.trailing.name = ft.icons.ARROW_DROP_DOWN if e.control.trailing.name == ft.icons.ARROW_DROP_DOWN_CIRCLE else ft.icons.ARROW_DROP_DOWN_CIRCLE
            page.update()

    expansion_tiles = [
        ft.ExpansionTile(
            title=ft.Text("RÉSUMÉ DES STATISTIQUES", color=TEXT_WHITE),
            subtitle=ft.Text("Cliquez pour voir les détails", color=TEXT_WHITE),
            controls=[ft.ListTile(title=ft.Text("Résumé des présences", color=TEXT_WHITE))],
        ),
        ft.ExpansionTile(
            title=ft.Text("Présences", color=TEXT_WHITE),
            subtitle=ft.Text("Détails des présences", color=TEXT_WHITE),
            trailing=ft.Icon(ft.icons.ARROW_DROP_DOWN, color=TEXT_WHITE),
            on_change=handle_expansion_tile_change,
            controls=[ft.ListTile(title=ft.Text("Présences enregistrées", color=TEXT_WHITE))],
        ),
    ]

    list_view = ft.ListView(controls=expansion_tiles, expand=True)

    def update_statistics():
        stats = fetch_statistics(user["email"])
        if stats:
            content.controls.clear()
            content.controls.append(title)
            for stat in stats:
                content.controls.append(ft.Text(f"{stat[0]} {stat[1]} - Présences: {stat[2]}", color=TEXT_WHITE))
        else:
            content.controls.append(ft.Text("Erreur lors de la récupération des données", color="red"))
        page.update()

    update_statistics()

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

    return [ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color=TEXT_WHITE, on_click=lambda _: page.go('/page_accueil')), content, stat1, stat2, navigation_bar, list_view]
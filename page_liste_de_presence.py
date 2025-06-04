import flet as ft
import mysql.connector
from mysql.connector import Error

BG = "#041955"
BULLE = '#2BC2A9'
TEXT_WHITE = 'white'

def page_liste_de_presence(page: ft.Page):
    page.bgcolor = BG

    # Check if user is teacher
    user = page.session.get("user") or {"profession": "Inconnu", "email": "inconnu@example.com"}
    if user["profession"] != "Enseignant":
        return [ft.Text("Accès réservé aux enseignants", color="red", size=20)]

    # Database connection
    db_config = {
        'host': 'localhost',
        'database': 'donnee_app',
        'user': 'root',
        'password': 'Kamssone25',
        'port': '3308'
    }

    search_visible = False

    def toggle_search(e):
        nonlocal search_visible
        search_visible = not search_visible
        search_field.visible = search_visible
        task_list.visible = search_visible and bool(search_field.value)
        page.update()

    def perform_search(e):
        search_text = search_field.value.lower()
        if search_text:
            filtered_dates = [date[0] for date in dates_presence if search_text in str(date[0]).lower()]
            task_list.controls = [ft.Text(f"Liste de présence du {date}", color=TEXT_WHITE, size=16) for date in filtered_dates]
            task_list.visible = True
        else:
            task_list.visible = False
        page.update()

    search_field = ft.TextField(
        hint_text="Rechercher...",
        width=200,
        border_radius=10,
        bgcolor=ft.colors.WHITE,
        text_style=ft.TextStyle(color=ft.colors.BLUE_900),
        visible=False,
        on_change=perform_search
    )

    search_row = ft.Row(
        controls=[
            ft.IconButton(ft.icons.SEARCH, icon_color=TEXT_WHITE, on_click=toggle_search),
            search_field
        ],
        alignment=ft.MainAxisAlignment.END
    )

    # Fetch presence dates
    def fetch_presence_dates():
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            cursor.execute(
                "SELECT DISTINCT date_presence FROM presence_list WHERE teacher_email = %s ORDER BY date_presence DESC",
                (user["email"],)
            )
            dates = cursor.fetchall()
            cursor.close()
            connection.close()
            return dates
        except Error as e:
            print(f"Erreur lors de la récupération des dates: {e}")
            return []

    # Fetch presence details
    def afficher_contenu(date_presence):
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            cursor.execute(
                "SELECT u.nom, u.prenom, pl.is_present, c.course_name "
                "FROM presence_list pl JOIN utilisateurs u ON pl.student_email = u.email "
                "JOIN courses c ON pl.course_id = c.course_id "
                "WHERE pl.teacher_email = %s AND pl.date_presence = %s",
                (user["email"], date_presence)
            )
            presence_data = cursor.fetchall()
            contenu_container.controls.clear()
            contenu_container.controls.append(ft.Text(f"Liste de présence du {date_presence}:", size=20, color=TEXT_WHITE))
            for row in presence_data:
                status = "Présent" if row[2] else "Absent"
                contenu_container.controls.append(
                    ft.Text(f"{row[0]} {row[1]} - Cours: {row[3]} - Statut: {status}", color=TEXT_WHITE)
                )
            page.update()
        except Error as e:
            print(f"Erreur lors de la récupération des présences: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    dates_presence = fetch_presence_dates()
    tasks = [f"Liste de présence du {date[0]}" for date in dates_presence]
    buttons = [
        ft.FilledButton(
            text=f"Liste de présence du {date[0]}",
            color=TEXT_WHITE,
            on_click=lambda e, date_presence=date[0]: afficher_contenu(date_presence)
        ) for date in dates_presence
    ]

    task_list = ft.Column(
        controls=[ft.Text(task, color=TEXT_WHITE, size=16) for task in tasks],
        visible=False
    )

    contenu_container = ft.Column()

    title = ft.Text("Liste de présence", size=30, color=TEXT_WHITE)
    back_button = ft.ElevatedButton("Retour", on_click=lambda _: page.go("/page_accueil"), bgcolor=BULLE, color=TEXT_WHITE)

    content = ft.Column(
        controls=[title, back_button, search_row, *buttons, task_list, contenu_container],
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

    return [content, navigation_bar]
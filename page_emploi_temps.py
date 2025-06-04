import flet as ft
import mysql.connector
from mysql.connector import Error

def page_emploi_temps(page: ft.Page):
    BG = '#041955'
    BULLE = '#2BC2A9'
    TEXT_WHITE = 'white'
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

    def fetch_schedule():
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            cursor.execute(
                "SELECT cs.date, cs.heure_debut, cs.heure_fin, c.course_name, cs.matiere "
                "FROM courses_schedule cs JOIN courses c ON cs.course_id = c.course_id "
                "WHERE cs.teacher_email = %s ORDER BY cs.date, cs.heure_debut",
                (user["email"],)
            )
            schedule = cursor.fetchall()
            schedule_table.rows.clear()
            for row in schedule:
                schedule_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(row[0]), color=TEXT_WHITE)),
                            ft.DataCell(ft.Text(str(row[1])[:5], color=TEXT_WHITE)),
                            ft.DataCell(ft.Text(str(row[2])[:5], color=TEXT_WHITE)),
                            ft.DataCell(ft.Text(row[3], color=TEXT_WHITE)),
                            ft.DataCell(ft.Text(row[4], color=TEXT_WHITE)),
                        ],
                    )
                )
            page.update()
        except Error as e:
            print(f"Erreur lors de la récupération de l'emploi du temps: {e}")
            content.controls.append(ft.Text(f"Erreur: {e}", color="red"))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    title = ft.Text("Emploi du temps", size=30, color=TEXT_WHITE)
    back_button = ft.ElevatedButton("Retour", on_click=lambda _: page.go("/page_accueil"), bgcolor=BULLE, color=TEXT_WHITE)

    schedule_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Jour", color=TEXT_WHITE)),
            ft.DataColumn(ft.Text("Heure début", color=TEXT_WHITE)),
            ft.DataColumn(ft.Text("Heure fin", color=TEXT_WHITE)),
            ft.DataColumn(ft.Text("Cours", color=TEXT_WHITE)),
            ft.DataColumn(ft.Text("Matière", color=TEXT_WHITE)),
        ],
        rows=[],
        border=ft.border.all(2, BULLE),
        border_radius=10,
        bgcolor=BG,
    )

    scrollable_content = ft.ListView(
        controls=[title, back_button, ft.Container(height=20), schedule_table],
        expand=True,
    )

    content = ft.Column(
        controls=[scrollable_content],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )

    fetch_schedule()

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
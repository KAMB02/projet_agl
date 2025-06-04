import flet as ft
import mysql.connector
from mysql.connector import Error

BG = "#041955"
BULLE = '#2BC2A9'
TEXT_WHITE = 'white'

def page_notif(page: ft.Page):
    page.bgcolor = BG

    # Check if user is teacher
    user = page.session.get("user") or {"profession": "Inconnu"}
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

    def fetch_notifications():
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            cursor.execute("SELECT message, date FROM notifications ORDER BY date DESC")
            notifications = cursor.fetchall()
            notifications_container.controls.clear()
            for notification in notifications:
                notifications_container.controls.append(
                    ft.Text(f"{notification[1]}: {notification[0]}", color=TEXT_WHITE)
                )
            page.update()
        except Error as e:
            print(f"Erreur lors de la récupération des notifications: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    title = ft.Text("Notifications", size=30, color=TEXT_WHITE)
    back_button = ft.ElevatedButton("Retour", on_click=lambda _: page.go("/page_accueil"), bgcolor=BULLE, color=TEXT_WHITE)

    notifications_container = ft.Column()
    fetch_notifications()

    special_alert = ft.Container(
        content=ft.Text("⚠️ Alerte spéciale : Veuillez vérifier vos emails", color="red", size=18),
        padding=10,
        bgcolor="white",
        border_radius=10,
    )

    content = ft.Column(
        controls=[title, back_button, special_alert, notifications_container],
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
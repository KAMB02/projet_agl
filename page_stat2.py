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
            SELECT COUNT(*) as total, SUM(is_present) as presences
            FROM presence_list
            WHERE teacher_email = %s
            """,
            (teacher_email,)
        )
        stats = cursor.fetchone()
        cursor.close()
        connection.close()
        return stats
    except Error as e:
        print(f"Erreur lors de la récupération des statistiques: {e}")
        return None

def page_stat2(page: ft.Page):
    page.bgcolor = BG

    # Check if user is teacher
    user = page.session.get("user") or {"profession": "Inconnu", "email": "inconnu@example.com"}
    if user["profession"] != "Enseignant":
        return [ft.Text("Accès réservé aux enseignants", color="red", size=20)]

    title = ft.Text("STATISTIQUES EN DIAGRAMME", size=30, color=TEXT_WHITE, weight=ft.FontWeight.BOLD)
    stats = fetch_statistics(user["email"])
    if stats:
        total_presences = stats[1]
        total_absences = stats[0] - stats[1]
        total = stats[0]
        presence_percent = (total_presences / total * 100) if total > 0 else 0
        absence_percent = (total_absences / total * 100) if total > 0 else 0
    else:
        total_presences = 0
        total_absences = 0
        presence_percent = 0
        absence_percent = 0

    chart = ft.PieChart(
        sections=[
            ft.PieChartSection(
                presence_percent,
                title=f"{round(presence_percent)}% Présence",
                title_style=ft.TextStyle(size=16, color=TEXT_WHITE, weight=ft.FontWeight.BOLD),
                color=ft.colors.BLUE,
                radius=50,
            ),
            ft.PieChartSection(
                absence_percent,
                title=f"{round(absence_percent)}% Absence",
                title_style=ft.TextStyle(size=16, color=TEXT_WHITE, weight=ft.FontWeight.BOLD),
                color=ft.colors.PURPLE,
                radius=50,
            ),
        ],
        sections_space=0,
        center_space_radius=40,
        expand=True,
    )

    return [
        ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color=TEXT_WHITE, on_click=lambda _: page.go('/page_statistiques')),
        title,
        chart
    ]
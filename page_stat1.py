import flet as ft
import mysql.connector
from mysql.connector import Error

BG = "#041955"
FWG = "#FFFFFF"
FG = "#3450a1"
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

class State:
    toggle = True

s = State()

def page_stat1(page: ft.Page):
    page.bgcolor = BG

    # Check if user is teacher
    user = page.session.get("user") or {"profession": "Inconnu", "email": "inconnu@example.com"}
    if user["profession"] != "Enseignant":
        return [ft.Text("Accès réservé aux enseignants", color="red", size=20)]

    title = ft.Text("STATISTIQUES EN COURBE", size=30, color=TEXT_WHITE, weight=ft.FontWeight.BOLD)
    stats = fetch_statistics(user["email"])
    if stats:
        data_points = [ft.LineChartDataPoint(idx, stat[2]) for idx, stat in enumerate(stats)]
        data_1 = [
            ft.LineChartData(
                data_points=data_points,
                stroke_width=8,
                color=ft.colors.LIGHT_GREEN,
                curved=True,
                stroke_cap_round=True,
            )
        ]
    else:
        data_1 = []

    chart_1 = ft.LineChart(
        data_series=data_1,
        border=ft.Border(bottom=ft.BorderSide(4, ft.colors.with_opacity(0.5, ft.colors.ON_SURFACE))),
        left_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(value=1, label=ft.Text("1", size=14, weight=ft.FontWeight.BOLD)),
                ft.ChartAxisLabel(value=2, label=ft.Text("2", size=14, weight=ft.FontWeight.BOLD)),
                ft.ChartAxisLabel(value=3, label=ft.Text("3", size=14, weight=ft.FontWeight.BOLD)),
            ],
            labels_size=40,
        ),
        bottom_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(
                    value=2,
                    label=ft.Container(ft.Text("ÉTUDIANT", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.with_opacity(0.5, ft.colors.ON_SURFACE)), margin=ft.margin.only(top=10)),
                ),
            ],
            labels_size=32,
        ),
        tooltip_bgcolor=ft.colors.with_opacity(0.8, ft.colors.BLUE_GREY),
        min_y=0,
        max_y=4,
        min_x=0,
        max_x=len(stats) if stats else 1,
        expand=True,
    )

    def toggle_data(e):
        if s.toggle:
            chart_1.data_series = data_1[:1]
            chart_1.max_y = 6
            chart_1.interactive = False
        else:
            chart_1.data_series = data_1
            chart_1.max_y = 4
            chart_1.interactive = True
        s.toggle = not s.toggle
        chart_1.update()

    return [
        ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color=TEXT_WHITE, on_click=lambda _: page.go('/page_statistiques')),
        title,
        ft.IconButton(ft.icons.REFRESH, icon_color=TEXT_WHITE, on_click=toggle_data),
        chart_1,
    ]
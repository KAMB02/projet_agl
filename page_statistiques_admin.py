import flet as ft
import mysql.connector
from mysql.connector import Error

BG = "#041955"
BULLE = '#2BC2A9'
TEXT_WHITE = 'white'
TEXT_BLACK = 'black'

def page_statistiques_admin(page: ft.Page):
    page.bgcolor = BG
    page.adaptive = True

    # Vérifier si l'utilisateur est un administrateur
    user = page.session.get("user") or {"profession": "Inconnu"}
    if user["profession"] != "Administrateur":
        return [ft.Text("Accès réservé aux administrateurs", color="red", size=20)]

    # Configuration de la connexion à la base de données
    db_config = {
        'host': 'localhost',
        'database': 'donnee_app',
        'user': 'root',
        'password': 'Kamssone25',
        'port': '3308'
    }

    # Récupérer les statistiques des enseignants
    def fetch_teacher_stats():
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            cursor.execute("""
                SELECT e.Nom, e.Prenoms, COUNT(pe.Id_pres) as nb_presences,
                       (SELECT COUNT(*) FROM Emploi_du_temps et 
                        JOIN Enseignant ens ON et.Id_cours = ens.Id_cours 
                        WHERE ens.Id_ens = e.Id_ens) as total_cours,
                       IFNULL((COUNT(pe.Id_pres) / (SELECT COUNT(*) FROM Emploi_du_temps et 
                                                   JOIN Enseignant ens ON et.Id_cours = ens.Id_cours 
                                                   WHERE ens.Id_ens = e.Id_ens) * 100), 0) as pourcentage
                FROM Enseignant e
                LEFT JOIN Presence_ens pe ON e.Id_ens = pe.Id_ens
                GROUP BY e.Id_ens, e.Nom, e.Prenoms
            """)
            stats = cursor.fetchall()
            cursor.close()
            connection.close()
            return stats
        except Error as e:
            print(f"Erreur lors de la récupération des statistiques enseignants: {e}")
            return []

    # Récupérer les statistiques des étudiants
    def fetch_student_stats():
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            cursor.execute("""
                SELECT e.Nom, e.Prenoms, COUNT(pe.Id_pres) as nb_presences,
                       (SELECT COUNT(*) FROM Emploi_du_temps) as total_cours,
                       IFNULL((COUNT(pe.Id_pres) / (SELECT COUNT(*) FROM Emploi_du_temps) * 100), 0) as pourcentage
                FROM Etudiant e
                LEFT JOIN Presence_etu pe ON e.IP = pe.IP
                GROUP BY e.IP, e.Nom, e.Prenoms
            """)
            stats = cursor.fetchall()
            cursor.close()
            connection.close()
            return stats
        except Error as e:
            print(f"Erreur lors de la récupération des statistiques étudiants: {e}")
            return []

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

    # Statistiques enseignants
    teacher_stats = fetch_teacher_stats()
    teacher_container = ft.Column(scroll='auto')
    for stat in teacher_stats:
        teacher_container.controls.append(
            ft.Container(
                content=ft.Text(
                    f"{stat[0]} {stat[1]} : {stat[2]} présences sur {stat[3]} cours ({stat[4]:.2f}%)",
                    color=TEXT_WHITE
                ),
                bgcolor=BULLE,
                padding=10,
                border_radius=10,
                margin=5
            )
        )

    # Statistiques étudiants
    student_stats = fetch_student_stats()
    student_container = ft.Column(scroll='auto')
    for stat in student_stats:
        student_container.controls.append(
            ft.Container(
                content=ft.Text(
                    f"{stat[0]} {stat[1]} : {stat[2]} présences sur {stat[3]} cours ({stat[4]:.2f}%)",
                    color=TEXT_WHITE
                ),
                bgcolor=BULLE,
                padding=10,
                border_radius=10,
                margin=5
            )
        )

    # Graphique pour enseignants (courbe)
    teacher_chart_data = [
        ft.LineChartData(
            data_points=[ft.LineChartDataPoint(idx, stat[2]) for idx, stat in enumerate(teacher_stats)],
            stroke_width=8,
            color=ft.colors.LIGHT_GREEN,
            curved=True,
            stroke_cap_round=True,
        )
    ]

    teacher_chart = ft.LineChart(
        data_series=teacher_chart_data,
        border=ft.Border(bottom=ft.BorderSide(4, ft.colors.with_opacity(0.5, ft.colors.ON_SURFACE))),
        left_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(value=i, label=ft.Text(str(i), size=14, weight=ft.FontWeight.BOLD))
                for i in range(0, max([stat[2] for stat in teacher_stats] + [1]) + 1, 5)
            ],
            labels_size=40,
        ),
        bottom_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(
                    value=idx,
                    label=ft.Container(
                        ft.Text(f"{stat[0]}", size=12, weight=ft.FontWeight.BOLD),
                        margin=ft.margin.only(top=10)
                    )
                )
                for idx, stat in enumerate(teacher_stats)
            ],
            labels_size=32,
        ),
        tooltip_bgcolor=ft.colors.with_opacity(0.8, ft.colors.BLUE_GREY),
        min_y=0,
        max_y=max([stat[2] for stat in teacher_stats] + [1]),
        min_x=0,
        max_x=len(teacher_stats),
        expand=True,
    )

    # Graphique pour étudiants (diagramme)
    total_student_presences = sum([stat[2] for stat in student_stats])
    total_student_sessions = sum([stat[3] for stat in student_stats])
    presence_percent = (total_student_presences / total_student_sessions * 100) if total_student_sessions > 0 else 0
    absence_percent = 100 - presence_percent

    student_chart = {
        "type": "pie",
        "data": {
            "labels": ["Présences", "Absences"],
            "datasets": [{
                "data": [presence_percent, absence_percent],
                "backgroundColor": ["#36A2EB", "#FF6384"],
                "hoverOffset": 4
            }]
        },
        "options": {
            "responsive": True,
            "plugins": {
                "legend": {
                    "position": "top",
                    "labels": {
                        "color": "#FFFFFF"
                    }
                },
                "title": {
                    "display": True,
                    "text": "Pourcentage global des présences étudiants",
                    "color": "#FFFFFF"
                }
            }
        }
    }

    content = ft.Column(
        controls=[
            ft.Text("STATISTIQUES GLOBALES", size=30, color=TEXT_WHITE, weight=ft.FontWeight.BOLD),
            ft.Text("Statistiques des enseignants", size=20, color=BULLE),
            teacher_container,
            ft.Text("Présences par enseignant", size=16, color=TEXT_WHITE),
            teacher_chart,
            ft.Text("Statistiques des étudiants", size=20, color=BULLE),
            student_container,
            ft.Text("Pourcentage global des présences étudiants", size=16, color=TEXT_WHITE),
            ft.Container(
                content=ft.Text("Graphique en cours de développement", color=TEXT_WHITE),
                height=300,
                bgcolor=BULLE,
                alignment=ft.alignment.center
            ),  # Placeholder pour le graphique (Chart.js non pris en charge nativement par Flet)
            ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color=TEXT_WHITE, on_click=lambda _: page.go('/page_c')),
            navigation_bar
        ],
        scroll='auto',
        expand=True
    )

    return [content]
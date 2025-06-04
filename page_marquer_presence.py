import flet as ft
from datetime import datetime
import mysql.connector
from mysql.connector import Error

BG = "#041955"
BULLE = '#2BC2A9'
TEXT_WHITE = 'white'

def page_marquer_presence(page: ft.Page):
    page.bgcolor = BG

    # Vérifier si l'utilisateur est un étudiant
    user = page.session.get("user") or {"profession": "Inconnu", "email": "inconnu@example.com"}
    if user["profession"] != "Etudiant":
        return [ft.Text("Accès réservé aux étudiants", color="red", size=20)]

    # Configuration de la connexion à la base de données
    db_config = {
        'host': 'localhost',
        'database': 'donnee_app',
        'user': 'root',
        'password': 'Kamssone25',
        'port': '3308'
    }

    # Récupérer l'IP de l'étudiant à partir de l'email
    def get_student_ip(email):
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            cursor.execute("SELECT IP FROM Etudiant WHERE Email = %s", (email,))
            ip = cursor.fetchone()
            cursor.close()
            connection.close()
            return ip[0] if ip else None
        except Error as e:
            print(f"Erreur lors de la récupération de l'IP: {e}")
            return None

    # Récupérer les cours disponibles pour aujourd'hui
    def get_today_courses():
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            cursor.execute("""
                SELECT c.Id_cours, c.Libelle 
                FROM Cours c
                JOIN Emploi_du_temps et ON c.Id_cours = et.Id_cours
                WHERE et.Date_cours = CURDATE()
            """)
            courses = cursor.fetchall()
            cursor.close()
            connection.close()
            return courses
        except Error as e:
            print(f"Erreur lors de la récupération des cours: {e}")
            return []

    # Vérifier et enregistrer la présence
    def checkbox_changed(e):
        if e.control.value and course_dropdown.value:
            try:
                connection = mysql.connector.connect(**db_config)
                cursor = connection.cursor()
                student_ip = get_student_ip(user["email"])
                if not student_ip:
                    t.value = "Erreur : Étudiant non trouvé."
                    t.color = 'red'
                    page.update()
                    return

                # Vérifier si la présence existe déjà
                cursor.execute("""
                    SELECT * FROM Presence_etu 
                    WHERE IP = %s AND DATE(Date_presence) = CURDATE()
                """, (student_ip,))
                result = cursor.fetchone()

                if result:
                    t.value = "Vous avez déjà marqué votre présence aujourd'hui !"
                    t.color = 'orange'
                else:
                    # Insérer une nouvelle présence
                    cursor.execute("""
                        INSERT INTO Presence_etu (IP, Date_presence, Heure_debut, Heure_fin) 
                        VALUES (%s, %s, %s, %s)
                    """, (student_ip, datetime.now(), datetime.now().time(), datetime.now().time()))
                    connection.commit()
                    t.value = "Présence marquée avec succès !"
                    t.color = 'green'
                    checkbox.disabled = True
                    course_dropdown.disabled = True

            except Error as e:
                print(f"Erreur lors de l'enregistrement de la présence: {e}")
                t.value = f"Erreur : {e}"
                t.color = 'red'
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()
            page.update()

    t = ft.Text(weight=ft.FontWeight.BOLD)
    courses = get_today_courses()
    course_dropdown = ft.Dropdown(
        label="Sélectionner un cours",
        options=[ft.dropdown.Option(key=str(c[0]), text=c[1]) for c in courses],
        label_style=ft.TextStyle(color=TEXT_WHITE),
        bgcolor=BULLE,
        border_color=BULLE,
        border_radius=25,
        width=300
    )
    checkbox = ft.Checkbox(label="Marquer ma présence", on_change=checkbox_changed)

    return [
        ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color=TEXT_WHITE, on_click=lambda _: page.go('/page_6')),  # Ajustez selon la page d'accueil étudiant
        ft.Text(value="MARQUER MA PRÉSENCE", color=TEXT_WHITE, weight=ft.FontWeight.BOLD, size=18),
        ft.Container(content=course_dropdown, alignment=ft.alignment.center),
        ft.Container(content=checkbox, alignment=ft.alignment.center),
        t,
    ]
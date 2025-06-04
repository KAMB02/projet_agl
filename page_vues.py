from flet import *
import mysql.connector
from mysql.connector import Error

def page_vues_etu(page: Page, name):
    BG = '#041955'
    BULLE = '#2BC2A9'
    TEXT_WHITE = 'white'
    TEXT_BLACK = 'black'
    page.bgcolor = BG

    # Database connection
    db_config = {
        'host': 'localhost',
        'database': 'donnee_app',
        'user': 'root',
        'password': 'Kamssone25',
        'port': '3308'
    }

    # Check if user is teacher
    user = page.session.get("user") or {"profession": "Inconnu"}
    if user["profession"] != "Enseignant":
        return [Text("Accès réservé aux enseignants", color="red", size=20)]

    # Fetch students
    def get_students():
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            cursor.execute("SELECT email, nom, prenom, niveau, numero, adresse FROM utilisateurs WHERE profession = 'Etudiant'")
            students = cursor.fetchall()
            cursor.close()
            connection.close()
            return students
        except Error as e:
            print(f"Erreur lors de la récupération des étudiants: {e}")
            return []

    # Fetch student stats
    def get_student_stats(student_email):
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM attendance WHERE student_email = %s", (student_email,))
            attended = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM courses_schedule")
            total = cursor.fetchone()[0]
            percentage = (attended / total * 100) if total > 0 else 0
            cursor.close()
            connection.close()
            return [student_email, round(percentage, 2), attended, total]
        except Error as e:
            print(f"Erreur lors de la récupération des statistiques: {e}")
            return [student_email, 0, 0, 0]

    students = get_students()
    student_names = [f"{s[1]} {s[2]}" for s in students]

    def affiche(name):
        index = student_names.index(name)
        return [students[index][3], students[index][4], students[index][0], students[index][5]]

    def home(e):
        page.go('/page_accueil')

    def etudi(e):
        page.go('/page_liste_etudiants')

    infos = affiche(name)
    stats = get_student_stats(infos[2])

    retour = IconButton(icon=icons.ARROW_BACK, on_click=etudi, icon_color=TEXT_WHITE)

    return Column(
        controls=[
            retour,
            Container(
                content=Column(
                    controls=[
                        Text(f"Nom & Prénoms : {name}", size=20, weight="bold", color=TEXT_WHITE),
                        Text(f"Profession : Étudiant", size=16, color=TEXT_WHITE),
                        Text(f"Niveau d'étude : {infos[0]}", size=16, color=TEXT_WHITE),
                        Text(f"Numéro de téléphone : {infos[1]}", size=16, color=TEXT_WHITE),
                        Text(f"Email : {infos[2]}", size=16, color=TEXT_WHITE),
                        Text(f"Adresse : {infos[3]}", size=16, color=TEXT_WHITE),
                        Text(f"Statistiques : {stats[2]} présence(s) sur {stats[3]} soit {stats[1]} % de présence", size=16, color=TEXT_WHITE) if stats[2] > 0 else Text("Statistiques : Aucune présence", size=16, color=TEXT_WHITE),
                    ],
                    spacing=10,
                ),
                padding=20,
                border_radius=10,
                bgcolor=BULLE,
                margin=10,
            ),
            ElevatedButton("Retour", on_click=etudi)
        ]
    )
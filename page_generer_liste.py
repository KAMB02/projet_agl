import flet as ft
from datetime import datetime
import mysql.connector
from mysql.connector import Error

BG = '#041955'
BULLE = '#2BC2A9'
TEXT_WHITE = 'white'

def page_generer_liste(page: ft.Page):
    page.bgcolor = BG

    # Vérifier si l'utilisateur est un enseignant
    user = page.session.get("user") or {"profession": "Inconnu", "email": "inconnu@example.com"}
    if user["profession"] != "Enseignant":
        return [ft.Text("Accès réservé aux enseignants", color="red", size=20)]

    # Configuration de la connexion à la base de données
    db_config = {
        'host': 'localhost',
        'database': 'donnee_app',
        'user': 'root',
        'password': 'Kamssone25',
        'port': '3308'
    }

    # Récupérer l'Id_ens à partir de l'email
    def get_teacher_id(email):
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            cursor.execute("SELECT Id_ens FROM Enseignant WHERE Email = %s", (email,))
            id_ens = cursor.fetchone()
            cursor.close()
            connection.close()
            return id_ens[0] if id_ens else None
        except Error as e:
            print(f"Erreur lors de la récupération de l'Id_ens: {e}")
            return None

    # Récupérer les cours de l'enseignant
    def get_teacher_courses(teacher_id):
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            cursor.execute(
                "SELECT Id_cours, Libelle FROM Cours WHERE Id_cours IN "
                "(SELECT Id_cours FROM Enseignant WHERE Id_ens = %s)",
                (teacher_id,)
            )
            courses = cursor.fetchall()
            cursor.close()
            connection.close()
            return courses
        except Error as e:
            print(f"Erreur lors de la récupération des cours: {e}")
            return []

    # Récupérer les étudiants
    def get_students():
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            cursor.execute("SELECT IP, Nom, Prenoms FROM Etudiant")
            students = cursor.fetchall()
            cursor.close()
            connection.close()
            return students
        except Error as e:
            print(f"Erreur lors de la récupération des étudiants: {e}")
            return []

    # Enregistrer la liste de présence
    def save_presence_list(teacher_id, course_id, date_presence, presence_data):
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            for student_ip, is_present in presence_data.items():
                if is_present:
                    cursor.execute(
                        "INSERT INTO Presence_etu (IP, Date_presence, Heure_debut, Heure_fin) "
                        "VALUES (%s, %s, %s, %s)",
                        (student_ip, date_presence, datetime.now().time(), datetime.now().time())
                    )
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Error as e:
            print(f"Erreur lors de l'enregistrement de la liste de présence: {e}")
            return False

    def button_clicked(e):
        if not course_dropdown.value or not date_field.value:
            t.value = "Erreur : Veuillez sélectionner un cours et une date !"
            t.color = 'red'
        else:
            try:
                date_presence = datetime.strptime(date_field.value, "%d/%m/%Y").date()
                teacher_id = get_teacher_id(user["email"])
                presence_data = {student[0]: checkboxes[student[0]].value for student in students}
                if save_presence_list(teacher_id, int(course_dropdown.value), date_presence, presence_data):
                    t.value = "Liste de présence enregistrée avec succès !"
                    t.color = 'green'
                    form_container.visible = False
                else:
                    t.value = "Erreur lors de l'enregistrement de la liste de présence."
                    t.color = 'red'
            except ValueError:
                t.value = "Erreur : Format de date incorrect (jj/mm/aaaa)."
                t.color = 'red'
        page.update()

    t = ft.Text(weight=ft.FontWeight.BOLD)
    teacher_id = get_teacher_id(user["email"])
    courses = get_teacher_courses(teacher_id)
    course_dropdown = ft.Dropdown(
        label="Cours",
        options=[ft.dropdown.Option(key=str(c[0]), text=c[1]) for c in courses],
        label_style=ft.TextStyle(color=TEXT_WHITE),
        bgcolor=BULLE,
        border_color=BULLE,
        border_radius=25,
        width=300
    )

    date_field = ft.TextField(
        label="Date (jj/mm/aaaa)",
        label_style=ft.TextStyle(color=TEXT_WHITE),
        color=TEXT_WHITE,
        bgcolor=BULLE,
        border_color=BULLE,
        border_radius=25,
        width=300,
        on_change=lambda e: (
            setattr(date_field, 'error_text', None) if e.control.value and 
            (len(e.control.value) == 10 and e.control.value[2] == '/' and e.control.value[5] == '/') else
            setattr(date_field, 'error_text', "Format incorrect ! Utilisez jj/mm/aaaa")
        )
    )

    students = get_students()
    checkboxes = {s[0]: ft.Checkbox(label=f"{s[1]} {s[2]}") for s in students}
    student_checkboxes = ft.Column(controls=[checkboxes[s[0]] for s in students], scroll='auto')

    b = ft.ElevatedButton("Valider", on_click=button_clicked)

    form_container = ft.Column(
        controls=[
            course_dropdown,
            date_field,
            student_checkboxes,
            b
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return [
        ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color=TEXT_WHITE, on_click=lambda _: page.go('/page_accueil')),
        ft.Text(value="GÉNÉRER LA LISTE DE PRÉSENCE", color=TEXT_WHITE, weight=ft.FontWeight.BOLD, size=18),
        ft.Container(content=form_container, alignment=ft.alignment.center),
        t,
    ]
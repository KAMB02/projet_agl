import flet as ft
import mysql.connector
from mysql.connector import Error

BG = "#041955"
BULLE = '#2BC2A9'
TEXT_WHITE = 'white'

def page_9(page: ft.Page):
    page.bgcolor = BG
    page.adaptive = True

    # Vérifier si l'utilisateur est connecté et est un étudiant
    user = page.session.get("user") or {"profession": "Inconnu", "email": "inconnu@example.com"}
    if user["profession"] != "Etudiant":
        page.go("/page_b")  # Rediriger vers la page de connexion
        return [ft.Text("Redirection vers la page de connexion...", color=TEXT_WHITE)]

    # Configuration de la connexion à la base de données
    db_config = {
        'host': 'localhost',
        'database': 'donnee_app',  # Corrigé pour correspondre à page_1.py et page_2.py
        'user': 'root',
        'password': 'Kamssone25',
        'port': '3308'
    }

    # Récupérer les informations de l'étudiant
    def get_student_info(email):
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            cursor.execute("""
                SELECT e.IP, e.Nom, e.Prenoms, e.Niveau, e.Numero, e.Email, e.Adresse
                FROM Etudiant e
                WHERE e.Email = %s
            """, (email,))
            student = cursor.fetchone()
            cursor.close()
            connection.close()
            return student if student else None
        except Error as e:
            print(f"Erreur lors de la récupération des infos étudiant : {e}")
            return None

    # Fonction de déconnexion
    def logout(e):
        try:
            # Supprimer la session utilisateur
            if "user" in page.session.get_keys():
                page.session.remove("user")  # Utiliser "user" au lieu de "user_id"
            page.session.clear()  # Nettoyer toute la session
            # Rediriger vers la page de connexion
            t.value = "Déconnexion réussie ! Redirection..."
            t.color = "green"
            page.views.clear()  # Vider les vues pour éviter les conflits
            page.go("/page_1")
            page.update()
        except Exception as e:
            print(f"Erreur lors de la déconnexion : {e}")
            t.value = f"Erreur lors de la déconnexion : {e}"
            t.color = "red"
            page.update()

    # Récupérer les informations de l'étudiant
    student = get_student_info(user["email"])
    if not student:
        page.go("/page_b")  # Rediriger si l'étudiant n'est pas trouvé
        return [ft.Text("Erreur : Étudiant non trouvé.", color="red")]

    # Contenu de la page (profil étudiant)
    t = ft.Text(weight=ft.FontWeight.BOLD)
    profile_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(f"Profil de {student[1]} {student[2]}", size=24, color=BULLE, weight=ft.FontWeight.BOLD),
                ft.Text(f"Niveau : {student[3]}", size=16, color=TEXT_WHITE),
                ft.Text(f"Email : {student[5]}", size=16, color=TEXT_WHITE),
                ft.Text(f"Numéro : {student[4]}", size=16, color=TEXT_WHITE),
                ft.Text(f"Adresse : {student[6] or 'Non spécifiée'}", size=16, color=TEXT_WHITE),
                ft.ElevatedButton("Déconnexion", on_click=logout, bgcolor="red", color=TEXT_WHITE),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            scroll='auto'
        ),
        padding=20,
        border_radius=10,
        bgcolor=BULLE,
        margin=10,
    )

    # Barre de navigation pour étudiant
    navigation_bar = ft.CupertinoNavigationBar(
        bgcolor=ft.colors.WHITE,
        inactive_color=ft.colors.BLACK,
        active_color=ft.colors.BLUE,
        on_change=lambda e: (
            page.go("/page_6") if e.control.selected_index == 0 else  # Accueil étudiant
            page.go("/page_7") if e.control.selected_index == 1 else  # Emploi du temps
            page.go("/page_marquer_presence") if e.control.selected_index == 2 else  # Marquer présence
            page.go("/page_9") if e.control.selected_index == 3 else None  # Profil
        ),
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icon(ft.icons.HOME_ROUNDED, color="black"),
                selected_icon=ft.Icon(ft.icons.HOME_ROUNDED, color="BLUE"),
                label="Accueil"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icon(ft.icons.CALENDAR_TODAY, color="black"),
                selected_icon=ft.Icon(ft.icons.CALENDAR_TODAY, color="BLUE"),
                label="Emploi du temps"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icon(ft.icons.CHECK, color="black"),
                selected_icon=ft.Icon(ft.icons.CHECK, color="BLUE"),
                label="Présence"
            ),
            ft.NavigationBarDestination(
                icon=ft.Icon(ft.icons.PERSON, color="black"),
                selected_icon=ft.Icon(ft.icons.PERSON, color="BLUE"),
                label="Profil"
            ),
        ],
    )

    return [
        ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color=TEXT_WHITE, on_click=lambda e: page.go("/page_6")),  # Retour à l'accueil étudiant
        ft.Text("PAGE PROFIL", color=TEXT_WHITE, weight=ft.FontWeight.BOLD, size=18),
        profile_container,
        navigation_bar,
        t,
    ]
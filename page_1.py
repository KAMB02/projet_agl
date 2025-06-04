import flet as ft
import mysql.connector
from mysql.connector import Error
import bcrypt
from fonction import *
import time

# Fonction pour créer une connexion à la base de données
def create_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='donnee_app',
            user='root',
            password='Kamssone25',
            port='3308',
            charset='utf8mb4'
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Erreur lors de la connexion: {e}")
    return None

# Message pour afficher les erreurs ou les succès
message = ft.Text("", size=20, weight='bold')

# Page de connexion
def page_1(page: ft.Page):
    page.title = "PAGE DE CONNEXION"
    page.vertical_alignment = 'center'

    # Navigation vers les autres pages
    def s_inscrire(e):
        page.go("/page2")

    def oublier(e):
        page.go('/page3')

    # Récupérer les utilisateurs depuis la table `utilisateurs`
    def get_users():
        try:
            connection = create_connection()
            if connection:
                cursor = connection.cursor()
                cursor.execute("SELECT nom, prenom, numero, email, profession, mot_passe FROM utilisateurs")
                result = cursor.fetchall()
                cursor.close()
                connection.close()
                return result
            return []
        except Error as e:
            print(f"Erreur lors de la récupération des utilisateurs: {e}")
            return []

    list_users = get_users()
    list_numero = [str(user[2]) for user in list_users]
    list_mot_passe = [user[5] for user in list_users]  # Hashed passwords
    list_profession = [str(user[4]) for user in list_users]
    list_nomComplet = [f"{user[0]} {user[1]}" for user in list_users]
    list_email = [str(user[3]) for user in list_users]

    # Vérification des identifiants
    def identite(numero, mot_passe):
        if numero in list_numero:
            index = list_numero.index(numero)
            # Vérifier le mot de passe haché
            stored_password = list_mot_passe[index].encode('utf-8')
            if bcrypt.checkpw(mot_passe.encode('utf-8'), stored_password):
                return index
        return None

    # Gestion de la connexion
    def connexion(e):
        num = numero.value.strip()
        mdp = mot_de_passe.value.strip()
        if not num or not mdp:
            message.value = "Veuillez remplir tous les champs."
            message.color = "red"
        else:
            index = identite(num, mdp)
            if index is not None:
                # Stocker les informations de l'utilisateur dans la session
                page.session.set("user", {
                    "nom": list_users[index][0],
                    "prenom": list_users[index][1],
                    "email": list_users[index][3],
                    "profession": list_users[index][4],
                    "numero": list_users[index][2]
                })
                message.value = f"Connexion réussie en tant que {list_profession[index]}"
                message.color = "green"
                page.update()
                time.sleep(1)
                if list_profession[index] == 'Etudiant':
                    page.go('/page6')
                elif list_profession[index] == 'Enseignant':
                    page.go('/page_accueil')
                elif list_profession[index] == 'Administration':
                    page.go('/pageb')
            else:
                message.value = "Numéro ou mot de passe incorrect."
                message.color = "red"
        page.update()

    # Champs de saisie
    numero = ft.TextField(label="NUMERO", border_radius=20, border_color='white', bgcolor="white", width=400, color='black')
    mot_de_passe = ft.TextField(label="MOT DE PASSE", password=True, border_radius=20, border_color='white', can_reveal_password=True, bgcolor='white', width=400, color='black')

    # Boutons
    btn_connexion = ft.ElevatedButton("CONNEXION", animate_size=20, bgcolor='#90EE90', color='black', on_click=connexion)
    btn_inscrire = ft.ElevatedButton("S'INSCRIRE", on_click=s_inscrire, animate_size=50, bgcolor='lightblue', color='black')
    btn_oublier = ft.TextButton("MOT DE PASSE OUBLIÉ", on_click=oublier, style=ft.ButtonStyle(color='black'))
    btn_retour = ft.ElevatedButton("RETOUR", on_click=lambda _: page.go("/page5"), animate_size=50, bgcolor='white', color='black')

    # Agencement de la page
    champ = [
        ft.Column([
            ft.Text("Se connecter pour continuer", size=25, weight="bold", color='white'),
            numero,
            mot_de_passe,
            ft.Row([btn_connexion, btn_inscrire], alignment=ft.MainAxisAlignment.CENTER, spacing=30),
            ft.Row([btn_oublier], alignment=ft.MainAxisAlignment.CENTER)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        btn_retour,
        message
    ]

    return [
        ft.Column(
            champ,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )
    ]
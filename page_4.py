import flet as ft
import mysql.connector
from mysql.connector import Error
import bcrypt
import time

# Configuration de la base de données
db_config = {
    'host': 'localhost',
    'database': 'donnee_app',
    'user': 'root',
    'password': 'Kamssone25',
    'port': '3308'
}

# Fonction pour créer les colonnes si elles n'existent pas
def create_columns_if_not_exist():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Vérifier et ajouter la colonne 'mot_de_passe' si elle n'existe pas
        cursor.execute("SHOW COLUMNS FROM utilisateurs LIKE 'mot_de_passe'")
        result = cursor.fetchone()
        if not result:
            cursor.execute("ALTER TABLE utilisateurs ADD COLUMN mot_de_passe VARCHAR(255)")
            print("Colonne 'mot_de_passe' ajoutée à la table 'utilisateurs'.")

        # Vérifier et ajouter la colonne 'recovery_code' si elle n'existe pas
        cursor.execute("SHOW COLUMNS FROM utilisateurs LIKE 'recovery_code'")
        result = cursor.fetchone()
        if not result:
            cursor.execute("ALTER TABLE utilisateurs ADD COLUMN recovery_code VARCHAR(6)")
            print("Colonne 'recovery_code' ajoutée à la table 'utilisateurs'.")

        connection.commit()
    except Error as e:
        print(f"Erreur lors de la modification de la table : {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Appeler la fonction pour créer les colonnes si elles n'existent pas
create_columns_if_not_exist()

# Fonction pour réinitialiser le mot de passe dans la base de données
def reset_password(email, entered_code, new_password):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Vérifier si le code de récupération est correct
        check_query = "SELECT * FROM utilisateurs WHERE email = %s AND recovery_code = %s"
        cursor.execute(check_query, (email, entered_code))
        result = cursor.fetchone()

        if result:
            # Hacher le nouveau mot de passe
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            # Mettre à jour le mot de passe et effacer le code de récupération
            update_query = "UPDATE utilisateurs SET mot_passe = %s, recovery_code = NULL WHERE email = %s"
            cursor.execute(update_query, (hashed_password, email))
            connection.commit()
            print(f"Mot de passe mis à jour pour l'email : {email}")
            return True
        else:
            print("Code de récupération incorrect.")
            return False
    except Error as e:
        print(f"Erreur lors de la réinitialisation du mot de passe : {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Page de confirmation de mot de passe
def page_4(page: ft.Page):
    page.title = 'CONFIRMATION DE MOT DE PASSE'

    def VALIDER(e):
        # Récupérer l'email depuis la session
        email = page.session.get("recovery_email")
        if not email:
            message.value = "Erreur : Email non défini. Veuillez recommencer le processus de récupération."
            message.color = "red"
            page.update()
            return

        # Vérifier si les champs sont remplis
        if not all([code.value, nouveau.value, confirmer.value]):
            message.value = "Veuillez remplir tous les champs."
            message.color = "red"
            page.update()
            return

        # Vérifier si les mots de passe correspondent
        if nouveau.value != confirmer.value:
            message.value = "Les mots de passe ne correspondent pas."
            message.color = "red"
            page.update()
            return

        # Vérifier si le code est correct et réinitialiser le mot de passe
        if reset_password(email, code.value, nouveau.value):
            message.value = "Mot de passe mis à jour avec succès."
            message.color = "green"
            page.update()
            time.sleep(2)  # Attendre 2 secondes avant la redirection
            page.go('/page1')  # Rediriger vers la page de connexion
        else:
            message.value = "Code incorrect ou erreur lors de la réinitialisation."
            message.color = "red"
            page.update()

    def ANNULER(e):
        page.go('/page3')

    # Création des champs
    code = ft.TextField(label="CODE REÇU", border_radius=20, border_color='white', bgcolor='white')
    nouveau = ft.TextField(label='NOUVEAU MOT DE PASSE', password=True, can_reveal_password=True, border_radius=20, border_color='white', bgcolor='white')
    confirmer = ft.TextField(label='CONFIRMER MOT DE PASSE', password=True, can_reveal_password=True, border_radius=20, border_color='white', bgcolor='white')
    valider = ft.ElevatedButton("VALIDER", animate_size=50, bgcolor='lightblue', on_click=VALIDER)
    annuler = ft.ElevatedButton("ANNULER", animate_size=50, bgcolor='#90EE90', on_click=ANNULER)

    # Message d'information
    message = ft.Text("", size=18, weight="bold", color='white')

    # Disposition des éléments
    champ = [
        ft.Text('CONFIRMATION', size=22, weight='bold', color='white'),
        code,
        nouveau,
        confirmer,
        ft.Row([valider, annuler], alignment=ft.MainAxisAlignment.CENTER),
        message
    ]

    rectangle = ft.Container(
        content=ft.Column(champ, spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER),
        width=400,
        height=800,
        border_radius=20,
        bgcolor='#3450A1',
        padding=20
    )

    return [ft.Row([rectangle], alignment=ft.MainAxisAlignment.CENTER, expand=True)]
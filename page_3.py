import flet as ft
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import mysql.connector
from mysql.connector import Error
import time
from random import randint

# Configuration de la base de données
db_config = {
    'host': 'localhost',
    'database': 'donnee_app',
    'user': 'root',
    'password': 'Kamssone25',
    'port': '3308'
}

# Variables globales pour stocker le code de récupération et l'heure d'envoi
recovery_code = None
code_sent_time = None

# Fonction pour générer un code de récupération
def generate_recovery_code():
    return str(randint(100000, 999999))

# Fonction pour envoyer un email
def send_email(to_email, subject, body):
    try:
        # Configuration du serveur SMTP
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        from_email = "gnetoschiphra@gmail.com"  # Remplacez par votre email
        password = "iqrxihbpznmlsekl"  # Remplacez par votre mot de passe d'application

        # Création du message
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Connexion au serveur SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Activation du chiffrement TLS
        server.login(from_email, password)  # Connexion avec le mot de passe d'application

        # Envoi de l'email
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print("Email envoyé avec succès.")
        return True
    except smtplib.SMTPException as e:
        print(f"Erreur SMTP lors de l'envoi de l'email : {e}")
        return False
    except Exception as e:
        print(f"Erreur inattendue lors de l'envoi de l'email : {e}")
        return False

# Fonction pour vérifier si l'email existe dans la base de données
def check_email_exists(email):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM utilisateurs WHERE email = %s", (email,))
        result = cursor.fetchone()
        return result is not None
    except Error as e:
        print(f"Erreur lors de la vérification de l'email : {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Fonction pour mettre à jour le code de récupération dans la base de données
def update_recovery_code(email, recovery_code):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Mettre à jour le code de récupération dans la table
        update_query = "UPDATE utilisateurs SET recovery_code = %s WHERE email = %s"
        cursor.execute(update_query, (recovery_code, email))
        connection.commit()
        print(f"Code de récupération mis à jour pour l'email : {email}")
        return True
    except Error as e:
        print(f"Erreur lors de la mise à jour du code de récupération : {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Page de récupération de mot de passe
def page_3(page: ft.Page):
    page.title = 'RÉCUPÉRATION DE MOT DE PASSE'

    def ENVOYER(e):
        global recovery_code, code_sent_time

        if not email.value:
            message.value = "Veuillez entrer votre email."
            message.color = "red"
            page.update()
            return

        if not check_email_exists(email.value):
            message.value = "Email non trouvé."
            message.color = "red"
            page.update()
            return

        # Générer et enregistrer le code de récupération
        recovery_code = generate_recovery_code()
        code_sent_time = time.time()
        if update_recovery_code(email.value, recovery_code):
            # Stocker l'email dans la session pour page_4
            page.session.set("recovery_email", email.value)
            # Sujet et corps de l'email
            subject = "Code de récupération de mot de passe"
            body = (
                f"Bonjour cher utilisateur,\n\n"
                f"Voici votre code pour réinitialiser votre mot de passe : {recovery_code}.\n"
                f"Ce code est valable pendant 5 minutes et ne doit pas être partagé.\n"
                f"Si vous n'avez pas initié cette demande, contactez immédiatement notre support à contact@application.com.\n"
                f"Merci, l'équipe [Nom de l'application]."
            )

            # Envoyer l'email
            if send_email(email.value, subject, body):
                message.value = "Code de récupération envoyé à votre email."
                message.color = "green"
            else:
                message.value = "Erreur lors de l'envoi du code de récupération."
                message.color = "red"
        else:
            message.value = "Erreur lors de la génération du code de récupération."
            message.color = "red"
        page.update()

        # Rediriger vers la page de confirmation
        page.go('/page4')

    def RETOUR(e):
        page.go('/page1')

    # Création des champs
    email = ft.TextField(label="EMAIL", border_radius=20, border_color='white', bgcolor='white')
    envoyer = ft.ElevatedButton("ENVOYER", animate_size=50, bgcolor='lightblue', on_click=ENVOYER)
    retour = ft.ElevatedButton(text='RETOUR', bgcolor='lightblue', animate_size=20, on_click=RETOUR, color='black')

    # Message d'information
    message = ft.Text("", size=18, weight="bold", color='white')

    # Disposition des éléments
    champ = [
        ft.Text('RÉCUPÉRATION DE MOT DE PASSE', size=22, weight='bold', color='white'),
        email,
        ft.Row([envoyer, retour], alignment=ft.MainAxisAlignment.CENTER),
        message
    ]

    rectangle = ft.Container(
        content=ft.Column(champ, spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER),
        width=400,
        height=400,
        border_radius=20,
        bgcolor='#3450A1',
        padding=20
    )

    return [ft.Row([rectangle], alignment=ft.MainAxisAlignment.CENTER, expand=True)]
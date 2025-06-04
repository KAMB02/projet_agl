import flet as ft
import mysql.connector
from mysql.connector import Error
import bcrypt
import time

# Fonction pour récupérer les utilisateurs depuis la base de données
def liste_utilisateur(table_name):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='donnee_app',
            user='root',
            password='Kamssone25',
            port='3308'
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            result = cursor.fetchall()
            cursor.close()
            connection.close()
            return result
    except Error as e:
        print(f"Erreur lors de la récupération des données: {e}")
        return []

# Fonction pour normaliser une chaîne (convertir en minuscules et supprimer les espaces)
def normalize_text(text):
    if text:
        return text.lower().strip()
    return text

# Fonction principale pour la page d'inscription
def page_2(page: ft.Page):
    page.title = "PAGE D'INSCRIPTION"
    page.auto_scroll = True
    message = ft.Text("", size=20, weight='bold', color='green')

    # Récupérer les utilisateurs déjà inscrits
    inscrit = liste_utilisateur("utilisateurs")
    nom_inscrit = [normalize_text(str(user[1])) for user in inscrit]
    prenom_inscrit = [normalize_text(str(user[2])) for user in inscrit]

    # Récupérer les listes des étudiants, enseignants et administrateurs
    list_et = liste_utilisateur("etudiant")
    list_ens = liste_utilisateur("enseignant")
    list_admin = liste_utilisateur("administration")

    # Extraire les informations nécessaires et les normaliser
    list_nom_et = [normalize_text(str(et[3])) for et in list_et]
    list_prenom_et = [normalize_text(str(et[4])) for et in list_et]
    list_cart_etudiant = [str(et[1]) for et in list_et]
    list_email_et = [normalize_text(str(et[6])) for et in list_et]
    list_numero_et = [str(et[7]) for et in list_et]

    list_nom_ens = [normalize_text(str(ens[2])) for ens in list_ens]
    list_prenom_ens = [normalize_text(str(ens[3])) for ens in list_ens]
    list_Id_ens = [ens[0] for ens in list_ens]
    list_email_ens = [normalize_text(str(ens[4])) for ens in list_ens]
    list_numero_ens = [str(ens[5]) for ens in list_ens]

    list_nom_admin = [normalize_text(str(admin[1])) for admin in list_admin]
    list_prenom_admin = [normalize_text(str(admin[2])) for admin in list_admin]
    list_Id_admin = [admin[0] for admin in list_admin]
    list_email_admin = [normalize_text(str(admin[3])) for admin in list_admin]
    list_numero_admin = [str(admin[4]) for admin in list_admin]

    # Fonction pour vérifier si l'utilisateur est déjà inscrit
    def inscrits(name, prenom, nom_inscrit, prenom_inscrit):
        return name not in nom_inscrit and prenom not in prenom_inscrit

    # Fonction pour vérifier les informations de l'utilisateur
    def verification(id, name, prenom, numero, email, profession):
        # Normaliser les entrées avant la vérification
        name = normalize_text(name)
        prenom = normalize_text(prenom)
        email = normalize_text(email)
        
        if profession == "Administration":
            if (id in list_Id_admin and name in list_nom_admin and 
                prenom in list_prenom_admin and email in list_email_admin and 
                numero in list_numero_admin):
                return 1
        elif profession == "Enseignant":
            if (id in list_Id_ens and name in list_nom_ens and 
                prenom in list_prenom_ens and email in list_email_ens and 
                numero in list_numero_ens):
                return 2
        elif profession == "Etudiant":
            if (id in list_cart_etudiant and name in list_nom_et and 
                prenom in list_prenom_et and email in list_email_et and 
                numero in list_numero_et):
                return 3
        return 0  # Retourne 0 si la vérification échoue

    # Fonction pour enregistrer un nouvel utilisateur
    def enregistrer_insrit(name, prenom, numero, profession, mot_passe, email):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='donnee_app',
                user='root',
                password='Kamssone25',
                port='3308'
            )
            if connection.is_connected():
                cursor = connection.cursor()

                # Hacher le mot de passe
                hashed_password = bcrypt.hashpw(mot_passe.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

                # Vérifier si l'utilisateur existe déjà
                check_query = "SELECT * FROM utilisateurs WHERE nom = %s AND prenom = %s"
                cursor.execute(check_query, (name, prenom))
                existing_user = cursor.fetchone()

                if not existing_user:
                    # Insérer les données dans la table
                    insert_query = """
                    INSERT INTO utilisateurs (nom, prenom, numero, email, profession, mot_passe)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(insert_query, (name, prenom, numero, email, profession, hashed_password))
                    connection.commit()
                    print("Données insérées avec succès.")
                else:
                    print("L'utilisateur existe déjà.")

                cursor.close()
                connection.close()
        except Error as e:
            print(f"Erreur lors de la connexion à MySQL: {e}")

    # Gestion du changement de profession
    def on_profession_change(e):
        is_student = profession.value == "Etudiant"
        niveau.visible = is_student
        groupe_td.visible = is_student
        carte.visible = is_student
        num_carte.visible = not is_student
        page.update()

    # Bouton pour revenir à la page précédente
    def retour(e):
        page.go("/page1")

    # Bouton pour valider le formulaire
    def VALIDER(e):
        id_value = carte.value if profession.value == "Etudiant" else num_carte.value
        if not all([id_value, nom.value, prenom.value, numero.value, email.value, mot_de_passe.value, conf_mot_de_passe.value, profession.value]):
            message.value = "Veuillez remplir tous les champs"
            message.color = "red"
            page.update()
            return

        if mot_de_passe.value != conf_mot_de_passe.value:
            message.value = "Les mots de passe ne correspondent pas"
            message.color = "red"
            page.update()
            return

        verification_result = verification(id_value, nom.value, prenom.value, numero.value, email.value, profession.value)

        if verification_result == 0:
            message.value = "Échec de l'inscription, veuillez vérifier vos informations"
            message.color = "red"
            page.update()
            return

        if inscrits(nom.value, prenom.value, nom_inscrit, prenom_inscrit):
            enregistrer_insrit(nom.value, prenom.value, numero.value, profession.value, mot_de_passe.value, email.value)
            # Stocker les informations de l'utilisateur dans la session
            page.session.set("user", {
                "nom": nom.value,
                "prenom": prenom.value,
                "email": email.value,
                "profession": profession.value,
                "numero": numero.value
            })
            message.value = "Inscription réussie"
            message.color = "green"
            page.update()
            time.sleep(1)
            if profession.value == 'Etudiant':
                page.go('/page6')
            elif profession.value == 'Enseignant':
                page.go('/page_accueil')
            elif profession.value == 'Administration':
                page.go('/pageb')
        else:
            message.value = "Vous êtes déjà inscrit"
            message.color = "red"
            page.update()

    # Composants de l'interface utilisateur
    num_carte = ft.TextField(label="ID (Enseignant/Administration)", width=400, border_radius=20, bgcolor='white', color='black')
    carte = ft.TextField(label="NUMERO CARTE ETUDIANTE", width=400, border_radius=20, bgcolor='white', color='black', visible=False)
    groupe_td = ft.Dropdown(
        label="GROUPE DE TD",
        options=[ft.dropdown.Option(str(i)) for i in range(1, 16)] + [ft.dropdown.Option("SI"), ft.dropdown.Option("Mecanique")],
        width=400,
        visible=False, border_radius=20, bgcolor='white', color='black'
    )
    nom = ft.TextField(label="NOM", width=400, bgcolor='white', border_radius=20, color='black')
    prenom = ft.TextField(label="PRENOM", width=400, bgcolor='white', border_radius=20, color='black')
    niveau = ft.Dropdown(
        label="NIVEAU",
        options=[ft.dropdown.Option(f"Licence {i}") for i in range(1, 4)] + [ft.dropdown.Option(f"Master {i}") for i in range(1, 3)],
        width=400,
        visible=False, bgcolor='white', border_radius=20, color='black'
    )
    numero = ft.TextField(label="NUMERO", width=400, bgcolor='white', border_radius=20, color='black')
    email = ft.TextField(label="EMAIL", width=400, bgcolor='white', border_radius=20, color='black')
    mot_de_passe = ft.TextField(label="MOT DE PASSE", password=True, can_reveal_password=True, width=400, bgcolor='white', border_radius=20, color='black')
    conf_mot_de_passe = ft.TextField(label="CONFIRMER MOT DE PASSE", password=True, can_reveal_password=True, width=400, bgcolor='white', border_radius=20, color='black')
    profession = ft.Dropdown(
        label="PROFESSION",
        options=[ft.dropdown.Option("Administration"), ft.dropdown.Option("Enseignant"), ft.dropdown.Option("Etudiant")],
        on_change=on_profession_change,
        width=400, border_radius=20, bgcolor='white', color='black'
    )
    revenir = ft.ElevatedButton("RETOUR", on_click=retour, width=170, bgcolor='blue', style=ft.ButtonStyle(color='black'))
    valider = ft.ElevatedButton("VALIDER", on_click=VALIDER, width=170, bgcolor='green', style=ft.ButtonStyle(color='black'))

    # Structure de la page
    return [
        ft.Column([
            ft.Text("Veuillez renseigner le formulaire", size=22, weight="bold"),
            ft.Text("Veuillez choisir votre profession avant toute éventualité", size=15, weight="bold"),
            num_carte, carte, nom, prenom, niveau, groupe_td, numero, email, mot_de_passe, conf_mot_de_passe, profession,
            ft.Row([revenir, valider], alignment=ft.MainAxisAlignment.CENTER, spacing=30),
            message
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True, scroll='auto')
    ]
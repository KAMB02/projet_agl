import flet as ft
from flet import *
import mysql.connector
from mysql.connector import Error
from functools import partial
from datetime import datetime

def create_table_if_not_exists():
    try:
        # Connexion à la base de données
        connection = mysql.connector.connect(
            host='localhost',  # adresse de serveur MySQL
            database='donnee_app',  # base de données à utiliser
            user='root',  # nom d'utilisateur MySQL
            password='Kamssone25',port='3308'  # Remplacez par votre mot de passe MySQL
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            # Requête SQL pour créer la table si elle n'existe pas
            create_table_query = """
            CREATE TABLE IF NOT EXISTS presence_etu_archive (
                IP VARCHAR(255) NOT NULL,
                Date_presence DATE NOT NULL,
                Heure_debut TIME NOT NULL,
                Heure_fin TIME NOT NULL,
                PRIMARY KEY (IP, Date_presence)
            )
            """
            cursor.execute(create_table_query)
            connection.commit()

    except Error as e:
        print(f"Erreur lors de la création de la table: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connexion MySQL fermée")

def page_boite_de_reception(page: ft.Page):
    #===============================================================
    try:
        # Connexion à la base de données
        connection = mysql.connector.connect(
            host='localhost',  # adresse de serveur MySQL
            database='donnee_app',  # base de données à utiliser
            user='root',  # nom d'utilisateur MySQL
            password='Kamssone25',port='3308'  # Remplacez par votre mot de passe MySQL
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            # Requête SQL pour récupérer les données
            cursor.execute("SELECT * FROM presence_etu")
            liste_pres = list(cursor.fetchall())
            
            cursor.execute("SELECT * FROM etudiant")
            liste_etu = list(cursor.fetchall())
            
            connection.commit()

    except Error as e:
        print(f"Erreur lors de la connexion à MySQL: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connexion MySQL fermée")
            
    # LISTE DES ETUDIANTS          
    list_ip_etudiant = [str(etu[0]) for etu in liste_etu]
        
    # LISTE DE PRESENCE DES ETUDIANTS
    liste_presence = [str(pres[1]) for pres in liste_pres]

    def infos_presence(ip):
        index = list_ip_etudiant.index(ip)
        nom = liste_etu[index][3]
        prenoms = liste_etu[index][4]
        return f"{nom} {prenoms}"
       
    #===============================================================

    def button_clicked(e):
        try:
            # Connexion à la base de données
            connection = mysql.connector.connect(
                host='localhost',  # adresse de serveur MySQL
                database='donnee_app',  # base de données à utiliser
                user='root',  # nom d'utilisateur MySQL
                password='Kamssone25',port='3308'  # Remplacez par votre mot de passe MySQL
            )
            
            if connection.is_connected():
                cursor = connection.cursor()
                # Créer la table si elle n'existe pas
                create_table_if_not_exists()
                # Enregistrer les présences avec la date et l'heure
                for ip in liste_presence:
                    # Vérifier si l'entrée existe déjà
                    cursor.execute(
                        "SELECT COUNT(*) FROM presence_etu_archive WHERE IP = %s AND Date_presence = %s",
                        (ip, datetime.now().date())
                    )
                    count = cursor.fetchone()[0]
                    if count == 0:
                        cursor.execute(
                            "INSERT INTO presence_etu_archive (IP, Date_presence, Heure_debut, Heure_fin) VALUES (%s, %s, %s, %s)",
                            (ip, datetime.now().date(), datetime.now().time(), datetime.now().time())
                        )
                connection.commit()
                # Vider la liste des présences pour empêcher les étudiants de pointer à nouveau
                liste_presence.clear()
                panel.controls.clear()
                exp = ft.ExpansionPanel(
                    header=ft.ListTile(title=ft.Text("AUCUNE PRESENCE !")),
                    content=ft.ListTile(
                        title=ft.Text("Veuillez revenir plus tard", size=20),
                    ),
                )
                panel.controls.append(exp)
                # Afficher un message de succès
                success_message.value = "Liste du jour enregistrée avec succès !"
                page.update()

        except Error as e:
            print(f"Erreur lors de la connexion à MySQL: {e}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("Connexion MySQL fermée")

    enregistrer = ft.ElevatedButton(text="Enregistrer", on_click=button_clicked)

    def handle_change(e: ft.ControlEvent):
        print(f"Liste de présence du {e.data}")

    def handle_delete(e: ft.ControlEvent, num):
        panel.controls.remove(e.control.data)
        
        try:
            # Connexion à la base de données
            connection = mysql.connector.connect(
                host='localhost',  # adresse de serveur MySQL
                database='donnee_app',  # base de données à utiliser
                user='root',  # nom d'utilisateur MySQL
                password='Kamssone25',port='3308'  # Remplacez par votre mot de passe MySQL
            )
            
            if connection.is_connected():
                cursor = connection.cursor()
                # Requête SQL pour supprimer l'étudiant
                cursor.execute(f"DELETE FROM presence_etu WHERE IP = '{liste_presence[num]}'")
                connection.commit()

        except Error as e:
            print(f"Erreur lors de la connexion à MySQL: {e}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("Connexion MySQL fermée")        
        
        page.update()

    panel = ft.ExpansionPanelList(
        expand_icon_color=ft.colors.BLUE_500,
        elevation=8,
        divider_color=ft.colors.PURPLE,
        on_change=handle_change,
        controls=[]
    )

    colors = ["WHITE", "WHITE", "WHITE", "WHITE", "WHITE"]
    if not liste_presence:
        exp = ft.ExpansionPanel(
            header=ft.ListTile(title=ft.Text("AUCUNE PRESENCE !")),
            content=ft.ListTile(
                title=ft.Text("Veuillez revenir plus tard", size=20),
            ),
        )
        panel.controls.append(exp)
    else:                
        for i in range(len(liste_presence)):
            exp = ft.ExpansionPanel(
                bgcolor=colors[i % len(colors)],
                header=ft.ListTile(title=ft.Text(f"{infos_presence(liste_presence[i])}")),
                content=ft.ListTile(
                    title=ft.Text("SUPPRESSION"),
                    subtitle=ft.Text("Toucher l'icône pour enlever cet étudiant de la liste"),
                    trailing=ft.IconButton(ft.icons.DELETE, on_click=partial(handle_delete, num=i)),
                ),
            )
            exp.content.trailing.data = exp  # Associer l'expansion panel à l'icône de suppression
            panel.controls.append(exp)

    # Message de succès
    success_message = ft.Text(value="", color="GREEN", weight=ft.FontWeight.BOLD, size=18)

    # Organisation des éléments dans une colonne avec défilement
    content = ft.Column(
        controls=[
            ft.Divider(height=20, color=ft.colors.WHITE),
            panel,
            enregistrer,
            success_message,
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    # Retourner une liste de widgets
    return [
        ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color="WHITE", on_click=lambda _: page.go('/page_accueil')),
        ft.Text(value="VERIFICATION DE LA LISTE DU JOUR", color="WHITE", weight=ft.FontWeight.BOLD, size=18),
        content,
    ]
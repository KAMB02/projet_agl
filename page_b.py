from flet import *
import mysql.connector
from mysql.connector import Error

def page_b(page: Page):
    BG = '#041955'
    fond = '#3450a1'
    couleur_icone = fond  # Couleur des icônes (bleu)
    couleur_icone_actif = 'black'  # Couleur pour l'icône active
    page.adaptive = True
    # Les couleurs de la page

    def enseig(e):
        page.go('/pagec')

    def etudi(e):
        page.go('/paged')

    def profi(e):
        page.go('/pagee')

    def home(e):
        page.go('/pageb')

    def a_propos(e):
        page.go('/pagev')

    # Fonction pour calculer le taux de présence
    def calculer_taux_presence():
        try:
            # Connexion à la base de données
            connection = mysql.connector.connect(
                host='localhost',  # adresse de serveur MySQL
                database='donnee_app',  # base de données utiliser
                user='root',  # nom d'utilisateur MySQL
                password='Kamssone25',port='3308'  # Remplacez par votre mot de passe MySQL
            )
            
            if connection.is_connected():
                cursor = connection.cursor()
                # Requête SQL pour obtenir les données de présence
                cursor.execute("SELECT COUNT(*) FROM Presence_ens WHERE statut = 'Présent'")
                total_present = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM Presence_ens")
                total_seances = cursor.fetchone()[0]
                
                taux_presence = (total_present / total_seances) * 100 if total_seances > 0 else 0
                return taux_presence

        except Error as e:
            print(f"Erreur lors de la connexion à MySQL: {e}")
            return 0

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("Connexion MySQL fermée")

    # Calculer le taux de présence
    taux_presence = calculer_taux_presence()

    # Définition des icônes et textes
    rech = Icon(icons.SEARCH)
    noti = Icon(icons.NOTIFICATIONS_OUTLINED)

    # Menu déroulant
    menu_deroulant = PopupMenuButton(
        items=[
            PopupMenuItem(
                content=Text("Accueil"),
                on_click=home,
            ),
            PopupMenuItem(
                content=Text("Profil"),
                on_click=profi,
            ),
            PopupMenuItem(
                content=Text("À propos de"),
                on_click=a_propos,
            ),
        ],
        icon=icons.MENU,  # Icône du menu
    )

    # En-tête avec logo et titre
    header = Row(
        controls=[
            Icon(icons.HOME, size=40, color=couleur_icone),
            Text("Bienvenue sur l'application", size=30, color=couleur_icone),
        ],
        alignment=MainAxisAlignment.CENTER,
        spacing=10,
    )

    # Message de bienvenue
    welcome_message = Text(
        "Bienvenue, utilisateur !",
        size=24,
        color=fond,
        weight="bold",
        text_align="center",
    )

    # Section du taux de présence
    taux_presence_section = Column(
        controls=[
            Text("Taux de présence", size=20, color=couleur_icone, weight="bold"),
            Text(f"{taux_presence:.2f}%", size=18, color=couleur_icone),
        ],
        alignment=MainAxisAlignment.CENTER,
        spacing=10,
    )

    # Cartes cliquables pour les sections
    card_enseignants = Container(
        content=Column(
            controls=[
                Icon(icons.PERSON, size=50, color=couleur_icone),
                Text("Enseignants", size=20, color=couleur_icone),
            ],
            alignment=MainAxisAlignment.CENTER,
            spacing=10,
        ),
        width=200,
        height=150,
        bgcolor=BG,
        border_radius=20,
        on_click=enseig,
        alignment=alignment.center,
    )

    card_etudiants = Container(
        content=Column(
            controls=[
                Icon(icons.LIST_OUTLINED, size=50, color=couleur_icone),
                Text("Etudiants", size=20, color=couleur_icone),
            ],
            alignment=MainAxisAlignment.CENTER,
            spacing=10,
        ),
        width=200,
        height=150,
        bgcolor=BG,
        border_radius=20,
        on_click=etudi,
        alignment=alignment.center,
    )

#-----------------------------------------------

    def navigation_changed(e):
        if e.control.selected_index == 0:
            page.go("/pageb")  # Accueil
        elif e.control.selected_index == 1:
            page.go("/pagec")  # Emploi du temps
        elif e.control.selected_index == 2:
            page.go("/paged")  # Statistiques
        elif e.control.selected_index == 3:
            page.go("/pagee")  # Profil
    # Barre de navigation
    navigation_bar = CupertinoNavigationBar(
        bgcolor=colors.WHITE,
        inactive_color=colors.BLACK,
        active_color=colors.BLUE,
        on_change=navigation_changed,
        destinations=[
            NavigationBarDestination(
                icon=Icon(icons.HOME_ROUNDED, color="black"),
                selected_icon=Icon(icons.HOME_ROUNDED, color="BLUE"),
                label="Accueil"
            ),
            NavigationBarDestination(
                icon=Icon(icons.CALENDAR_TODAY, color="black"),
                selected_icon=Icon(icons.CALENDAR_TODAY, color="BLUE"),
                label="Enseignants"
            ),
            NavigationBarDestination(
                icon=Icon(icons.SHOW_CHART, color="black"),
                selected_icon=Icon(icons.SHOW_CHART, color="BLUE"),
                label="Etudiants"
            ),
            NavigationBarDestination(
                icon=Icon(icons.PERSON_2, color="black"),
                selected_icon=Icon(icons.PERSON_2, color="BLUE"),
                label="Profil"
            ),
        ],
    )

#------------------------------------------------

    # Structure principale de la page
    contenu_page_1 = Column(
        controls=[
            # Barre du haut avec les icônes
            Row(
                controls=[
                    menu_deroulant,  # Remplacement de `men` par le menu déroulant
                    Row([rech, noti], spacing=10),
                ],
                alignment=MainAxisAlignment.SPACE_BETWEEN,
            ),
            header,
            welcome_message,
            taux_presence_section,  # Ajout de la section du taux de présence
            Row(
                controls=[card_enseignants, card_etudiants],
                alignment=MainAxisAlignment.CENTER,
                spacing=20,
            ),
            Container(expand=True),  # Espace vide pour pousser state vers le bas
            Container(
                # Container pour centrer state en bas
                alignment=alignment.center,
                padding=padding.only(bottom=20)  # Petit espace en bas
            ), # Ajout de la barre de navigation
        ],
        expand=True  # Permet au Column de remplir la hauteur
    )

    return [contenu_page_1,navigation_bar]
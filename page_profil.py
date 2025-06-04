from flet import *
import mysql.connector
from mysql.connector import Error

# Page de profil pour les enseignants
def page_profil(page: Page):
    page.adaptive = True
    # Les couleurs de la page
    bulle = "#2BC2A9"
    text_1 = "white"
    text_2 = "black"

    # Récupérer les informations de l'utilisateur depuis la session
    user = page.session.get("user") or {
        "nom": "Inconnu",
        "prenom": "Inconnu",
        "email": "inconnu@example.com",
        "numero": "0000000000",
        "adresse": "N/A",
        "profession": "Enseignant"
    }

    # Fonction pour gérer les clics sur la barre de navigation
    def navigation_changed(e):
        if e.control.selected_index == 0:
            page.go("/page_accueil")  # Accueil
        elif e.control.selected_index == 1:
            page.go("/page_emploi_temps")  # Emploi du temps
        elif e.control.selected_index == 2:
            page.go("/page_statistiques")  # Statistiques
        elif e.control.selected_index == 3:
            page.go("/page_profil")  # Profil

    # Barre de navigation
    navigation_bar = CupertinoNavigationBar(
        bgcolor=colors.WHITE,
        inactive_color=colors.BLACK,
        active_color=colors.BLUE,
        on_change=navigation_changed,
        destinations=[
            NavigationBarDestination(
                icon=Icon(Icons.HOME_ROUNDED, color="black"),
                selected_icon=Icon(Icons.HOME_ROUNDED, color="BLUE"),
                label="Accueil"
            ),
            NavigationBarDestination(
                icon=Icon(Icons.CALENDAR_TODAY, color="black"),
                selected_icon=Icon(Icons.CALENDAR_TODAY, color="BLUE"),
                label="Emploi du temps"
            ),
            NavigationBarDestination(
                icon=Icon(Icons.SHOW_CHART, color="black"),
                selected_icon=Icon(Icons.SHOW_CHART, color="BLUE"),
                label="Statistiques"
            ),
            NavigationBarDestination(
                icon=Icon(Icons.PERSON_2, color="black"),
                selected_icon=Icon(Icons.PERSON_2, color="BLUE"),
                label="Profil"
            ),
        ],
    )

    # Fonction pour gérer la déconnexion
    def deconnecter(e):
        def close_dialog(e):
            page.dialog.open = False
            page.update()

        page.dialog = AlertDialog(
            title=Text("Confirmation"),
            content=Text("Voulez-vous vraiment vous déconnecter ?"),
            actions=[
                TextButton("Annuler", on_click=close_dialog),
                TextButton("Oui", on_click=lambda _: page.go('/page1'))  # Rediriger vers la page de connexion
            ],
            actions_alignment=MainAxisAlignment.END,
        )
        page.dialog.open = True
        page.update()

    # Les informations de l'enseignant depuis la session
    infos_admin = [
        user["nom"],
        user["prenom"],
        user["numero"],
        user["email"],
        user["adresse"]
    ]
    det_infos_admin = ["Nom", "Prénoms", "Numéro de téléphone", "Email", "Adresse"]
    conteneur1 = Column(height=500, scroll='auto')

    # Ajout des informations à la colonne
    conteneur1.controls.append(
        Container(
            height=55,
            padding=15,
            content=Row(controls=[Icon(name='PERSON', color='white', size=50)])
        )
    )
    for i, j in zip(infos_admin, det_infos_admin):
        conteneur1.controls.append(Text(f"{j} :", color=text_2, weight=FontWeight.BOLD))
        conteneur1.controls.append(
            Container(
                adaptive=True,
                border_radius=10,
                bgcolor=bulle,
                height=50,
                width=1500,
                padding=15,
                content=Row(controls=[Text(i, color=text_1)], scroll='auto')
            )
        )

    retour = IconButton(icon=icons.ARROW_BACK, on_click=lambda _: page.go('/page_accueil'), icon_color='black')
    retour2 = TextButton("Se déconnecter", on_click=deconnecter, style=ButtonStyle(color='white'))

    # Structure principale de la page
    tout = Column(
        controls=[
            Column(controls=[retour]),
            Container(expand=True),
            conteneur1,
            Container(Row(controls=[retour2])),
            navigation_bar,
        ],
        alignment=MainAxisAlignment.END,
        expand=True,
    )

    return [tout]
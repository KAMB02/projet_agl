from flet import *

# Page de profil pour les administrateurs
def page_e(page: Page):
    BG = '#041955'
    FG = '#3450a1'
    couleur_icone = '#3450CB'
    couleur_icone_act = 'black'
    page.adaptive = True
    bulle = '#2BC2A9'
    text_1 = "white"
    text_2 = "black"

    # Récupérer les informations de l'utilisateur depuis la session
    user = page.session.get("user") or {
        "nom": "Inconnu",
        "prenom": "Inconnu",
        "email": "inconnu@example.com",
        "numero": "0000000000",
        "adresse": "N/A",
        "profession": "Administration"
    }

    def enseig(e):
        page.go('/pagec')

    def etudi(e):
        page.go('/paged')

    def profi(e):
        page.go('/pagee')

    def home(e):
        page.go('/pageb')

    def deconnecter(e):
        def close_dialog(e):
            page.dialog.open = False
            page.update()

        page.dialog = AlertDialog(
            title=Text("Confirmation"),
            content=Text("Voulez-vous vraiment vous déconnecter ?"),
            actions=[
                TextButton("Annuler", on_click=close_dialog),
                TextButton("Oui", on_click=lambda _: page.go('/page1'))
            ],
            actions_alignment=MainAxisAlignment.END,
        )
        page.dialog.open = True
        page.update()

    # Les informations de l'administrateur depuis la session
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
            content=Row(controls=[Icon(name='PERSON', color='black', size=50)])
        )
    )
    for i, j in zip(infos_admin, det_infos_admin):
        conteneur1.controls.append(Text(f"{j} :", color=text_2))
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

    retour = IconButton(icon=icons.ARROW_BACK, on_click=home)
    retour2 = TextButton("Se déconnecter", on_click=deconnecter, style=ButtonStyle(color='black'))

    # Barre de navigation avec texte sous les icônes
    nav_bar = Container(
        content=Row(
            controls=[
                Container(
                    content=Column(
                        controls=[
                            Icon(icons.HOME, color=couleur_icone_act if page.route == '/pageb' else couleur_icone),
                            Text("Accueil", size=12, color=couleur_icone_act if page.route == '/pageb' else couleur_icone),
                        ],
                        spacing=5,
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                    ),
                    on_click=home,
                    padding=10,
                ),
                Container(
                    content=Column(
                        controls=[
                            Icon(icons.PERSON, color=couleur_icone_act if page.route == '/pagec' else couleur_icone),
                            Text("Enseignants", size=12, color=couleur_icone_act if page.route == '/pagec' else couleur_icone),
                        ],
                        spacing=5,
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                    ),
                    on_click=enseig,
                    padding=10,
                ),
                Container(
                    content=Column(
                        controls=[
                            Icon(icons.LIST_OUTLINED, color=couleur_icone_act if page.route == '/paged' else couleur_icone),
                            Text("Etudiants", size=12, color=couleur_icone_act if page.route == '/paged' else couleur_icone),
                        ],
                        spacing=5,
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                    ),
                    on_click=etudi,
                    padding=10,
                ),
                Container(
                    content=Column(
                        controls=[
                            Icon(icons.PERSON, color=couleur_icone_act if page.route == '/pagee' else couleur_icone),
                            Text("Profil", size=12, color=couleur_icone_act if page.route == '/pagee' else couleur_icone),
                        ],
                        spacing=5,
                        horizontal_alignment=CrossAxisAlignment.CENTER,
                    ),
                    on_click=profi,
                    padding=10,
                ),
            ],
            alignment=MainAxisAlignment.SPACE_AROUND,
        ),
        bgcolor='white',
        padding=10,
        border_radius=20,
    )

    # Structure principale de la page
    tout = Column(
        controls=[
            Column(controls=[retour]),
            Container(expand=True),
            conteneur1,
            Container(Row(controls=[retour2])),
            nav_bar,
        ],
        alignment=MainAxisAlignment.END,
        expand=True,
    )

    return [tout]
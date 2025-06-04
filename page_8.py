from flet import *


def page_8(page: Page):

    BG = '#041955'
    FG = '#3450a1'
    ICON_COLOR = FG  # Couleur des icônes (bleu)
    FOCUS_COLOR = 'black'  # Couleur pour l'icône active

    def change(e):
        page.go('/page6')

    def aller(e):
        page.go('/page7')

    def profi(e):
        page.go('/page8')

    def home(e):
        page.go('/page9')

    def parametres(e):
        page.go('/page10')  # Ajoutez une route pour les paramètres

    def a_propos(e):
        page.go('/page11')  # Ajoutez une route pour "À propos de"
    txt1 = Text('Récapitulatif des stats', size=20, color="white")
    retour= IconButton(icon=icons.ARROW_BACK,on_click=change)
    
    # Barre de navigation avec texte sous les icônes
    nav_bar = Container(
    content=Row(
        controls=[
            Container(
                content=Column(
                    controls=[
                        Icon(icons.HOME, color=FOCUS_COLOR if page.route == '/page6' else ICON_COLOR),
                        Text("Accueil", size=12, color=FOCUS_COLOR if page.route == '/page6' else ICON_COLOR),
                    ],
                    spacing=5,  # Espace entre l'icône et le texte
                    horizontal_alignment=CrossAxisAlignment.CENTER,  # Centrer horizontalement
                ),
                on_click=lambda e: page.go('/page6'),  # Redirige vers la page d'accueil
                padding=10,
            ),
            Container(
                content=Column(
                    controls=[
                        Icon(icons.BAR_CHART, color=FOCUS_COLOR if page.route == '/page8' else ICON_COLOR),
                        Text("Stats", size=12, color=FOCUS_COLOR if page.route == '/page8' else ICON_COLOR),
                    ],
                    spacing=5,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                ),
                on_click=lambda e: page.go('/page8'),  # Redirige vers la page des stats
                padding=10,
            ),
            Container(
                content=Column(
                    controls=[
                        Icon(icons.PERSON, color=FOCUS_COLOR if page.route == '/page9' else ICON_COLOR),
                        Text("Profil", size=12, color=FOCUS_COLOR if page.route == '/page9' else ICON_COLOR),
                    ],
                    spacing=5,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                ),
                on_click=lambda e: page.go('/page9'),  # Redirige vers la page de profil
                padding=10,
            ),
            Container(
                content=Column(
                    controls=[
                        Icon(icons.FINGERPRINT, color=FOCUS_COLOR if page.route == '/page7' else ICON_COLOR),
                        Text("Pointage", size=12, color=FOCUS_COLOR if page.route == '/page7' else ICON_COLOR),
                    ],
                    spacing=5,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                ),
                on_click=lambda e: page.go('/page7'),  # Redirige vers la page de pointage
                padding=10,
            ),
        ],
        alignment=MainAxisAlignment.SPACE_AROUND,
    ),
    bgcolor='white',  # Fond de la barre en blanc
    padding=5,
    border_radius=20,
)

    

    # Structure de la page avec la barre de navigation en bas
    tout = Column(
        controls=[
            retour,  # Contenu principal
            Container(expand=True),
            nav_bar,   # Barre de navigation
        ],
        expand=True,  # Permet à la colonne de remplir toute la hauteur
    )
    
    return [tout]
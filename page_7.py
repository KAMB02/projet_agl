from flet import *

def page_7(page: Page):
    BG = '#041955'
    FWG = '#97b4ff'
    FG = '#3450a1'
    PINK = '#eb06ff'
    ICON_COLOR = FG  # Couleur des icônes (bleu)
    FOCUS_COLOR = 'black'  # Couleur pour l'icône active
    page.bgcolor = BG

    # Variable pour stocker la valeur de la case cochée
    selected_index = Ref[int]()  # Référence pour stocker l'index sélectionné

    # Fonction pour gérer le changement d'état des cases à cocher
    def checkbox_changed(e, index):
        if e.control.value:  # Si la case est cochée
            if selected_index.current is not None:
                # Décocher la case précédemment cochée
                Etu.controls[selected_index.current].content.controls[0].value = False
            selected_index.current = index  # Mettre à jour l'index sélectionné
        page.update()

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
    # Texte et conteneurs
    txt1 = Text('Pointage', size=30, color='white')
    txt2 = Text('Liste de Présence', color=PINK, size=20)
    txt3 = Text('Ok', text_align='center', color='white')
    saut = Column(height=10)
    retour= IconButton(icon=icons.ARROW_BACK,on_click=change)
    env = Container(
        width=50,
        height=50,
        bgcolor=PINK,
        border_radius=30,
        on_click=change,
        content=Row([txt3], alignment=MainAxisAlignment.CENTER)
    )

    # Liste des étudiants avec des cases à cocher
    Etu = Column(
        height=500,
        scroll='auto',
        controls=[]
    )
    for i in range(15):
        checkbox = Checkbox(
            on_change=lambda e, idx=i: checkbox_changed(e, idx) ) # Associer l'index à la case
        Etu.controls.append(
            Container(
                expand=True,
                height=50,
                bgcolor='white',
                border_radius=30,
                padding=padding.only(top=10, left=10, right=10),
                content=Row(
                    controls=[
                        checkbox,  # Ajouter la case à cocher
                        Text('Étudiant', color='#000000', text_align='center')
                    ],
                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                )
            )
        )

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

    # Structure principale de la page
    tout = Column(
        controls=[
            Column(
                controls=[
                    retour,txt1, txt2, Etu,
                ]
            ),
            Container(expand=True),
            Container(
                content=env,
                alignment=alignment.center,
                padding=padding.only(bottom=20)
            ),
            nav_bar,  # Ajout de la barre de navigation
        ],
        expand=True  # Permet au Column de remplir la hauteur
    )

    return [tout]
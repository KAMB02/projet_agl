from flet import *

def page_10(page: Page):
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


    # Contenu de la page
    txt1 = Text('Bienvenue sur la page 5', size=30)
    txt2 = Text('Basculer entre le mode clair et sombre', size=20)
    retour= IconButton(icon=icons.ARROW_BACK,on_click=change)
    sauti = Container(height=3)

    

    # Conteneur principal
    content = Container(
        content=Column(
            controls=[
                retour,
                sauti,
                txt1,
                txt2,
                
            ],
            horizontal_alignment=CrossAxisAlignment.START,  # Alignement à gauche
        ),
        padding=20,
        border_radius=10,
    )



    # Conteneur pour centrer à gauche
    main_container = Container(
        content=content,
        alignment=alignment.top_left,  # Centre à gauche
        expand=True,  # Prend toute la largeur disponible
    )

    return [main_container]
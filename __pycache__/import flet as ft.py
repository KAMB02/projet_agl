import flet as ft

def main(page: ft.Page):
    # Fonction appelée lorsque la route change
    def on_route_change(e):
        page.views.clear()
        if page.route == "/page1":  # Page 1 : Connexion
            page.views.append(ft.View(route="/page1", controls=page_1(page)))
        elif page.route == "/page2":  # Page 2 : Inscription
            page.views.append(ft.View(route="/page2", controls=page_2(page)))
        page.update()

    # Configuration initiale
    page.on_route_change = on_route_change
    page.go("/page1")  # On démarre sur la page de connexion

# Définition de la page 1 (connexion)
def page_1(page: ft.Page):
    # Fonction pour naviguer vers la page 2 (inscription)
    def s_inscrire(e):
        page.go("/page2")

    # Champs pour l'identifiant et le mot de passe
    identifiant = ft.TextField(label="IDENTIFIANT", border_radius=20, border_color='blue')
    mot_de_passe = ft.TextField(label="MOT DE PASSE", password=True, border_radius=20, border_color='blue')

    # Boutons
    connexion = ft.ElevatedButton("CONNEXION", bgcolor='green')
    inscrire = ft.ElevatedButton("S'INSCRIRE", on_click=s_inscrire, bgcolor='blue')

    # Contenu de la page dans un rectangle
    champ = [
        ft.Text("Se connecter pour continuer", size=25, weight="bold"),
        identifiant,
        mot_de_passe,
        ft.Row([connexion, inscrire], alignment=ft.MainAxisAlignment.CENTER, spacing=30),
    ]

    rectangle = ft.Container(
        content=ft.Column(champ, spacing=10),
        padding=20,
        border_radius=20,
        bgcolor='#e0f7fab',
        width=400,
        height=250,
    )

    return [rectangle]

# Définition de la page 2 (inscription)
def page_2(page: ft.Page):
    # Fonction pour revenir à la page 1
    def retour(e):
        page.go("/page1")

    # Fonction appelée lorsqu'on clique sur "VALIDER"
    def inscription(e):
        print("Inscription validée !")

    # Champs pour le formulaire d'inscription
    nom = ft.TextField(label="NOM", border_radius=20, border_color='blue')
    prenom = ft.TextField(label="PRENOM", border_radius=20, border_color='blue')
    date_naissance = ft.TextField(label="DATE DE NAISSANCE", border_radius=20, border_color='blue')
    profession = ft.TextField(label="PROFESSION", border_radius=20, border_color='blue')
    niveau = ft.TextField(label="NIVEAU", border_radius=20, border_color='blue')
    groupe_td = ft.TextField(label="GROUPE DE TD", border_radius=20, border_color='blue')
    identifiant = ft.TextField(label="IDENTIFIANT", border_radius=20, border_color='blue')
    mot_de_passe = ft.TextField(label="MOT DE PASSE", password=True, border_radius=20, border_color='blue')
    conf_mot_passe = ft.TextField(label="CONFIRMER MOT DE PASSE", password=True, border_radius=20, border_color='blue')

    # Boutons
    valider = ft.ElevatedButton("VALIDER", on_click=inscription, bgcolor='blue')
    retour_btn = ft.ElevatedButton("RETOUR", on_click=retour, bgcolor='green')

    # Contenu de la page dans un rectangle
    champ = [
        ft.Text("Veuillez renseigner le formulaire", size=22, weight="bold"),
        nom,
        prenom,
        date_naissance,
        profession,
        niveau,
        groupe_td,
        identifiant,
        mot_de_passe,
        conf_mot_passe,
        ft.Row([valider, retour_btn], alignment=ft.MainAxisAlignment.CENTER, spacing=30),
    ]

    rectangle = ft.Container(
        content=ft.Column(champ, spacing=10),
        padding=20,
        border_radius=20,
        bgcolor='#e0f7fab',
        width=400,
        height=650,
    )

    return [rectangle]

# Démarrage de l'application
ft.app(target=main)

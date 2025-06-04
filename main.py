import flet as ft
from page_accueil import page_accueil
from page_emploi_temps import page_emploi_temps
from page_statistiques import page_statistiques
from page_stat1 import page_stat1
from page_stat2 import page_stat2
from page_profil import page_profil
from page_generer_liste import page_generer_liste
from page_liste_de_presence import page_liste_de_presence
from page_boite_de_reception import page_boite_de_reception
from page_a_propos import page_a_propos
from page_notif import page_notif
from page_marquer_presence import page_marquer_presence

BG = "#041955"
FWG = "#FFFFFF"

def main(page: ft.Page):
    page.title = "Mon appli"
    page.bgcolor = BG      

    def on_route_change(route):
        page.views.clear()
        if page.route == "/page_accueil":
            page.views.append(ft.View(route="/page_accueil", controls=page_accueil(page), bgcolor='#3450A1'))
        elif page.route == "/page_emploi_temps":
            page.views.append(ft.View(route="/page_emploi_temps", controls=page_emploi_temps(page), bgcolor='#3450A1'))
       
        elif page.route == "/page_statistiques":
            page.views.append(ft.View(route="/page_statistiques", controls=page_statistiques(page), bgcolor='#3450A1'))
        elif page.route == "/page_stat1":
            page.views.append(ft.View(route="/page_stat1", controls=page_stat1(page), bgcolor='#3450A1'))
        elif page.route == "/page_stat2":
            page.views.append(ft.View(route="/page_stat2", controls=page_stat2(page), bgcolor='#3450A1'))
        elif page.route == "/page_profil":  
            page.views.append(ft.View(route="/page_profil", controls=page_profil(page, name="Bakayoko Alima"), bgcolor='#3450A1'))
        elif page.route == "/page_generer_liste":
            page.views.append(ft.View(route="/page_generer_liste", controls=page_generer_liste(page, utilisateur_connecte="ENS001"), bgcolor='#3450A1'))
        elif page.route == "/page_liste_de_presence":
            page.views.append(ft.View(route="/page_liste_de_presence", controls=page_liste_de_presence(page), bgcolor='#3450A1'))
        elif page.route == "/page_boite_de_reception":
            page.views.append(ft.View(route="/page_boite_de_reception", controls=page_boite_de_reception(page), bgcolor='#3450A1'))
        elif page.route == "/page_a_propos":
            page.views.append(ft.View(route="/page_a_propos", controls=page_a_propos(page), bgcolor='#3450A1'))
        elif page.route == "/page_notif":
            page.views.append(ft.View(route="/page_notif", controls=page_notif(page), bgcolor='#3450A1'))
        elif page.route == "/page_marquer_presence":
            page.views.append(ft.View(route="/page_marquer_presence", controls=page_marquer_presence(page, etudiant_connecte="YEOH0612860001"), bgcolor='#3450A1'))
        page.update()

    page.on_route_change = on_route_change
    page.go("/page_accueil")

ft.app(target=main)
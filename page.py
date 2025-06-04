import flet as ft
from page_1 import *
from page_2 import *
from page_3 import *
from page_4 import *
from page_5 import *
from page_v import *
from page_7 import *
from page_8 import *
from page_6 import *
from page_9 import *
from page_10 import *
from page_11 import *
from page_b import *
from page_c import *
from page_d import *
from page_e import *
from page_f import *
from page_g import *
from page_v import *
from page_accueil import *
from page_emploi_temps import *
from page_statistiques import *
from page_profil import *
from page_a_propos import *
from page_notif import *
from page_generer_liste import *
from page_liste_de_presence import *
from page_marquer_presence import *
from page_liste_etudiants import *
from page_statistiques_admin import *
from fonction import*


col='#3450A1'

def page(page: ft.Page):
    page.bgcolor='blue'
    
    # Configuration de la gestion des routes
    def on_route_change(e):
        page.views.clear()
        if page.route == "/page1":
            page.views.append(ft.View(route="/page1", controls=page_1(page),bgcolor=col))
        elif page.route == "/page2":
            page.views.append(ft.View(route="/page2", controls=page_2(page),bgcolor=col))
        elif page.route=="/page3":
            page.views.append(ft.View(route="/page3",controls=page_3(page),bgcolor=col))
        elif page.route=="/page4":
            page.views.append(ft.View(route="/page4",controls=page_4(page),bgcolor=col))
        elif page.route =="/page5":
            page.views.append(ft.View(route="/page5",controls=page_5(page),bgcolor=col)) 
        elif page.route =="/page7":
            page.views.append(ft.View(route="/page7",controls=page_7(page),bgcolor=col))    
        elif page.route =="/page8":
            page.views.append(ft.View(route="/page8",controls=page_8(page),bgcolor=col)) 
        elif page.route =="/page9":
            page.views.append(ft.View(route="/page9",controls=page_9(page),bgcolor=col)) 
        elif page.route =="/page10":
            page.views.append(ft.View(route="/page10",controls=page_10(page),bgcolor=col)) 
        elif page.route =="/page6":
            page.views.append(ft.View(route="/page6",controls=page_6(page),bgcolor=col)) 
        elif page.route =="/page11":
            page.views.append(ft.View(route="/page11",controls=page_11(page),bgcolor=col))
        elif page.route =="/pageb":
            page.views.append(ft.View(route="/pageb",controls=page_b(page),bgcolor=col))
        elif page.route =="/pagec":
            page.views.append(ft.View(route="/pagec",controls=page_c(page),bgcolor=col))
        elif page.route =="/paged":
            page.views.append(ft.View(route="/paged",controls=page_d(page),bgcolor=col))
        elif page.route =="/pagee":
            page.views.append(ft.View(route="/pagee",controls=page_e(page),bgcolor=col))
        elif page.route =="/pagef":
            page.views.append(ft.View(route="/pagef",controls=page_f(page),bgcolor=col))
        elif page.route =="/pageg":
            page.views.append(ft.View(route="/pageg",controls=page_g(page),bgcolor=col))
        elif page.route =="/pagev":
            page.views.append(ft.View(route="/pagev",controls=page_v(page),bgcolor=col))
        elif page.route =="/page_accueil":
            page.views.append(ft.View(route="/page_accueil",controls=page_accueil(page),bgcolor=col))
        elif page.route =="/page_emploi_temps":
            page.views.append(ft.View(route="/page_emploi_temps",controls=page_emploi_temps(page),bgcolor=col))
        elif page.route =="/page_statistiques":
            page.views.append(ft.View(route="/page_statistiques",controls=page_statistiques(page),bgcolor=col))
        elif page.route =="/page_profil":
            page.views.append(ft.View(route="/page_profil",controls=page_profil(page),bgcolor=col))
        elif page.route =="/page_a_propos":
            page.views.append(ft.View(route="/page_a_propos",controls=page_a_propos(page),bgcolor=col))
        elif page.route =="/page_notif":
            page.views.append(ft.View(route="/page_notif",controls=page_notif(page),bgcolor=col))
        elif page.route =="/page_generer_liste":
            page.views.append(ft.View(route="/page_generer_liste",controls=page_generer_liste(page),bgcolor=col))
        elif page.route =="/page_liste_de_presence":
            page.views.append(ft.View(route="/page_liste_de_presence",controls=page_liste_de_presence(page),bgcolor=col))
        elif page.route =="/page_marquer_presence":
           page.views.append(ft.View(route="/page_marquer_presence", controls=page_marquer_presence(page), bgcolor='#3450A1'))
        elif page.route == "/page_liste_etudiants":
            page.views.append(ft.View("/page_liste_etudiants", page_liste_etudiants(page),bgcolor=col))
        elif page.route == "/page_statistiques_admin":
            page.views.append(ft.View("/page_statistiques_admin", page_statistiques_admin(page),bgcolor=col))
        page.update()


    # Configuration initiale
    page.on_route_change = on_route_change
    page.go("/page5")  # Page de démarrage

ft.app(target=page)
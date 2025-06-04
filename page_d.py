from flet import *
from fonction import*

# La page de la liste des enseignants
def page_d(page: Page):

    BG = '#041955'
    fond = '#3450a1'
    couleur_icone = fond  # Couleur des icônes (bleu)
    couleur_icone_actif = 'black'  # Couleur pour l'icône active
    page.adaptive = True
    # Les couleurs de la page
    bulle='#2BC2A9'
    text_blank="white"
    text_noir="black"
#----------------------------------------------------
    list_et=liste_utilisateur("etudiant")        
    list_etudiant=[]
    for i in range(len(list_et)):
        ch=str(list_et[i][3])+' '+str( list_et[i][4])
        list_etudiant.append(ch)

#----------------------------------------------------   
    
    def enseig(e):
        page.go('/pagec')

    def etudi(e):
        page.go('/paged')

    def profi(e):
        page.go('/pagee')

    def home(e):
        page.go('/pageb')

    def affiche(name):
        index=list_etudiant.index(name)
        niveau= list_et[index][5]
        email= list_et[index][6]
        numero= list_et[index][7] 
        adresse= list_et[index][8]
        return [niveau,numero,email,adresse]
    
    list_statistique= stat_etu() 
    element_stat=[]     
    for i in range(len(list_statistique)):
        element_stat.append(list_statistique[i][0])
        
    # Fonction pour créer une vue étudiant            
    def vue_etudiant(name,chemin):          
            infos=affiche(name)
            if name in element_stat:
                index=element_stat.index(name)
            return Column(
                controls=[
                    Text(f"        Nom & Prenoms : {name} "),
                    Text(f"        Profession : Etudiant "),
                    Text(f"        Niveau d'etude : {infos[0]}"),
                    Text(f"        Numero de telephone : {infos[1]}"),
                    Text(f"        Email : {infos[2]}"),
                    Text(f"        Adresse : {infos[3]}"),
                    Text(f"        Statisque : {list_statistique[index][2]} presence(s) sur /  {list_statistique[index][3]} soit {list_statistique[index][1]} % de presence ") if name in element_stat else Text("        Statisque : Aucune presence ")  ,
                    ElevatedButton("        Retour       ", on_click=lambda _: page.go('/'))
                    
                ]
            )

    # Fonction pour créer une vue utilisateur

    def changement_route(event):
        route = event.route  # Accéder à l'attribut 'route' de l'objet 'RouteChangeEvent'

        if route.startswith('/etu/'):
            ens_name = route.split('/')[-1]
            page.views.append(
                View(route,
                    [Container(
                    on_click=lambda _: page.go('/pagee'),
                    height=40,
                    width=40,
                    ),],vue_etudiant(ens_name,'etu')
                )
                ) 
               
        # Si la route est '/create_task', afficher la vue de création de tâche    
        else:
            page.views.append(View(route="/paged",controls=page_d(page),bgcolor=fond))
            
        page.update()
                    
    # Fonction pour générer une liste d'étudiants
    def gener_cont_list(list, chemin):
        conteneur = Column(height=400, scroll='auto')
        # Ajout des tâches à la colonne
        for i in list:
            conteneur.controls.append(
                Container(adaptive=True,
                    border_radius=10,
                    bgcolor=bulle, height=50, width=1500,padding=15,
                    content=Row(controls=[Text(i,color=text_blank)], scroll='auto'),
                    on_click=lambda e, name=i: page.go(f"/{chemin}/{name}")
                )
            )
        return conteneur

    # Fonction de recherche
    def rechercher_etudiant(e):
        recherche = champ_recherche.value.lower()
        resultats = [etudiant for etudiant in list_etudiant if recherche in etudiant.lower()]
        cont_etu.controls.clear()
        if resultats:
            cont_etu.controls.extend(gener_cont_list(resultats, "etu").controls)
        else:
            cont_etu.controls.append(Text("Aucun Etudiant trouve ", color="red",size=15))
        page.update()

    
    # Champ de recherche et bouton de recherche
    champ_recherche = TextField(label="Rechercher un étudiant", width=300)
    bouton_recherche = ElevatedButton("Rechercher", on_click=rechercher_etudiant)

    # Créer le conteneur pour étudiant
    cont_etu = gener_cont_list(list_etudiant, "etu")
    
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

    # Structure de la page avec la barre de navigation en bas
    tout = Column(
        controls=[          
            Row(
                controls=[
                    champ_recherche,
                    bouton_recherche,
                ],
                alignment=MainAxisAlignment.CENTER,
                spacing=10,
            ),
            cont_etu, # Barre de navigation
        ],
        expand=True,
    )
    
    page.on_route_change = changement_route
    page.update()
    return [tout,navigation_bar]
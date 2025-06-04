from flet import *
from fonction import *

# La page de la liste des enseignants
def page_c(page: Page):

    BG = '#041955'
    fond = '#3450a1'
    couleur_icone = fond  # Couleur des icônes (bleu)
    couleur_icone_actif = 'black'  # Couleur pour l'icône active
    page.adaptive = True
    # Les couleurs de la page
    bulle='#2BC2A9'
    text_blank="white"
    text_noir="black"
    couleur_background='white'
    
    #===============================================================
    list_en=liste_utilisateur("enseignant")        
    list_enseignant=[]
    for i in range(len(list_en)):
        ch=str(list_en[i][2])+' '+str( list_en[i][3])
        list_enseignant.append(ch)

    def affiche(name):
        index=list_enseignant.index(name)
        email= list_en[index][4]
        numero= list_en[index][5] 
        adresse=list_en[index][6]
        return [numero,email,adresse]  
    
    #==============================================================+
    
     
        

    list_statistique= stat_ens() 
    element_stat=[]     
    for i in range(len(list_statistique)):
        element_stat.append(list_statistique[i][0])

    
    # Définir les colonnes de couleur rose
    green_columns = Row(
        controls=[
            Container(
                content=Text("Date", size=16, color=text_blank),
                bgcolor=bulle,
                padding=10,
                border_radius=5,
                expand=True,
            ),
            Container(
                content=Text("Matiere", size=16, color=text_blank),
                bgcolor=bulle,
                padding=10,
                border_radius=5,
                expand=True,
            ),
            Container(
                content=Text("Heure_debut", size=16, color=text_blank),
                bgcolor=bulle,
                padding=10,
                border_radius=5,
                expand=True,
            ),
            Container(
                content=Text("Heure_fin", size=16, color=text_blank),
                bgcolor=bulle,
                padding=10,
                border_radius=5,
                expand=True,
            ),
            Container(
                content=Text("Statut", size=16, color=text_blank),
                bgcolor=bulle,
                padding=10,
                border_radius=5,
                expand=True,
            ),                       
        ],
        spacing=10,
    )
    # Fonction pour générer une liste d'étudiants
    def gener_cont_matiere(name):
        
        index=list_enseignant.index(name)
        id=list_en[index][0]        
        conteneur = Column( scroll='auto')
        date_cours=emploi_du_temps_prof(id)[0]
        matiere=emploi_du_temps_prof(id)[1]
        heure_debut_cours=emploi_du_temps_prof(id)[2]
        heure_fin_cours=emploi_du_temps_prof(id)[3]
        
        list_id=infos_presence_enseignant()[0]
        date=infos_presence_enseignant()[1]
        heure_debut=infos_presence_enseignant()[2]  
        heure_fin=infos_presence_enseignant()[3]  
        heure_actuelle = datetime.now().time()
        date_actuelle = datetime.now().date()
        
        stat_cours=("En cours","Effectue","Non Effectue","A venir ")
        for i,j,k,l in zip(date_cours,matiere,heure_debut_cours,heure_fin_cours):
            conteneur.controls.append(
                Row(
                controls=[
                    Container(
                        content=Text(i, size=16, color=text_blank,),
                        bgcolor=bulle,
                        padding=10,
                        border_radius=5,
                        expand=True,
                    ),
                    Container(
                        content=Text(j, size=16, color=text_blank),
                        bgcolor=bulle,
                        padding=10,
                        border_radius=5,
                        expand=True,
                    ),
                    Container(
                        content=Text(k, size=16, color=text_blank),
                        bgcolor=bulle,
                        padding=10,
                        border_radius=5,
                        expand=True,
                    ),
                    Container(
                        content=Text(l, size=16, color=text_blank),
                        bgcolor=bulle,
                        padding=10,
                        border_radius=5,
                        expand=True,
                    ),
                    Container(
                        content=Text(stat_cours[0], size=16, color=text_blank) 
                        
                        if id in list_id and str(date[list_id.index(id)])[:10]== str(i)  and str(heure_debut)[:2]==str(heure_debut_cours)[:2] and str(heure_fin)[:2] > str(heure_actuelle)[:2]
                        else   Text(stat_cours[1], size=16, color=text_blank) if id in list_id and str(date[list_id.index(id)])[:10]== str(i)  and str(heure_debut)[:2]==str(heure_debut_cours)[:2] 
                        else  Text(stat_cours[3], size=16, color=text_blank) if id not in list_id   and str(i) > str(date_actuelle) 
                        else  Text(stat_cours[3], size=16, color=text_blank) if id in list_id   and str(i) > str(date_actuelle) 
                        else  Text(stat_cours[2], size=16, color=text_blank),
                        
                        bgcolor=bulle,
                        padding=10,
                        border_radius=5,
                        expand=True,
                    ),                       
                ],
                spacing=10,
            )                
            )
        return conteneur    
    # conteneur_infos_matiere=gener_cont_matiere()
    
    # Fonction pour créer une vue utilisateur            
    def vue_ulisateur(name, chemin):          
        infos = affiche(name)
        if name in element_stat:
            index = element_stat.index(name)
            stats = list_statistique[index]
        else:
            stats = None

        return Column(
            controls=[
                Container(
                    content=Column(width=1500,
                        controls=[
                            Text(f"Nom & Prenoms : {name}", size=20, weight="bold"),
                            Text(f"Profession : Professeur", size=16),
                            Text(f"Numero de telephone : {infos[0]}", size=16),
                            Text(f"Email : {infos[1]}", size=16),
                            Text(f"Adresse : {infos[2]}", size=16),
                            Text(f"Statistique : {stats[2]} presence(s) sur {stats[3]} soit {stats[1]} % de presence") if stats else Text("Statistique : Aucune presence", size=16),
                        ],
                        spacing=10,
                    ),
                    padding=20,
                    border_radius=10,
                    bgcolor=bulle,
                    margin=10,
                    
                ),
                Container(
                    content=Column( 
                        controls=[green_columns,gener_cont_matiere(name)],spacing=10,),
                        padding=5,
                        border_radius=10,
                        bgcolor=couleur_background,
                        margin=10,
                ),
                ElevatedButton("Retour", on_click=lambda _: page.go('/pagec')),
            ]
        )

    # Fonction pour créer une vue utilisateur

    def changement_route(event):
        route = event.route  # Accéder à l'attribut 'route' de l'objet 'RouteChangeEvent'

        if route.startswith('/ens/'):
            ens_name = route.split('/')[-1]
            page.views.append(
                View(route,
                    [Container(),],
                    vue_ulisateur(ens_name, 'ens')
                )
            ) 
        elif page.route == "/pageb":
            page.go('/pageb')       
        elif page.route == "/paged":
            page.go('/paged')       
        elif page.route == "/pagee":
            page.go('/pagee')       
        else:
            page.views.append(View(route="/pagec", controls=page_c(page), bgcolor=fond))
            
        page.update()
                    
    # Fonction pour générer une liste d'étudiants
    def gener_cont_list(list, chemin):
        conteneur = Column(height=400, scroll='auto')
        for i in list:
            conteneur.controls.append(
                Container(adaptive=True,
                    border_radius=10,
                    bgcolor=bulle, height=50, width=1500, padding=15,
                    content=Row(controls=[Text(i, color=text_blank)], scroll='auto'),
                    on_click=lambda e, name=i: page.go(f"/{chemin}/{name}")
                )
            )
        return conteneur

    # Fonction de recherche
    def rechercher_enseignant(e):
        recherche = champ_recherche.value.lower()
        resultats = [enseignant for enseignant in list_enseignant if recherche in enseignant.lower()]
        cont_ens.controls.clear()
        if resultats:
            cont_ens.controls.extend(gener_cont_list(resultats, "ens").controls)
        else:
            cont_ens.controls.append(Text("Aucun enseignant trouvé", color="red", size=15))
        page.update()

    # Champ de recherche et bouton de recherche
    champ_recherche = TextField(label="Rechercher un enseignant", width=300)
    bouton_recherche = ElevatedButton("Rechercher", on_click=rechercher_enseignant)

    # Créer le conteneur pour enseignant
    cont_ens = gener_cont_list(list_enseignant, "ens")
    
    # Barre de navigation avec texte sous les icônes
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
            cont_ens,
        ],
        expand=True,
    )
    
    page.on_route_change = changement_route
    page.update()
    return [tout,navigation_bar]
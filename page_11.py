from flet import*

def page_11(page:Page):
    def change(e):
        page.go('/page6')
    retour= IconButton(icon=icons.ARROW_BACK,on_click=change)
    saut=Container(height=50)

    # fonction a propos 
    about_content = Column(
        [
            Text(
                "À propos de l'application",
                color="BLUE",
                size=24,
                weight=FontWeight.BOLD,
                text_align=TextAlign.CENTER,
            ),
            Text(
                "Cette application est conçue pour simplifier la gestion des listes de présence et des emplois du temps.",
                color="WHITE",
                size=16,
                text_align=TextAlign.CENTER,
            ),
            Text(
                "Fonctionnalités principales :",
                color="WHITE",
                size=16,
                weight=FontWeight.BOLD,
                text_align=TextAlign.LEFT,
            ),
            ListView(
                [
                    ListTile(title=Text("Gestion des listes de présence", color="INDIGO" )),
                    ListTile(title=Text("Génération de rapports", color="INDIGO")),
                    ListTile(title=Text("Visualisation des statistiques", color="INDIGO")),
                    ListTile(title=Text("Gestion des emplois du temps", color="INDIGO")),
                ],
                expand=True,
            ),
            Text(
                "Version : 1.0.0",
                color="WHITE",
                size=14,
                text_align=TextAlign.CENTER,
            ),
            Text(
                "Développé par :",
                color="WHITE",
                size=16,
                weight=FontWeight.BOLD,
                text_align=TextAlign.CENTER,
            ),
            Text(
                "Équipe XYZ",
                color="WHITE",
                size=14,
                text_align=TextAlign.CENTER,
            ),
            Text(
                "Contact : contact@example.com",
                color="WHITE",
                size=14,
                text_align=TextAlign.CENTER,
            ),
            Text(
                "© 2023 Tous droits réservés.",
                color="WHITE",
                size=12,
                text_align=TextAlign.CENTER,
            ),
        ],
        spacing=20,
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
    )

    tout=Column(
        controls=[
            retour,
            about_content
        ]
    )

    return [tout]
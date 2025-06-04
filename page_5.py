import flet as ft 

def page_5(page:ft.Page):
    
    def COMMENCER(e):
        page.go("/page1")
        
    img = ft.Row([ft.Image(src="logo_sans_fond.png",color='white')],alignment=ft.MainAxisAlignment.CENTER)
    
    #texte=ft.Text("MI_POINT",size=40,weight="bold",color='#e0f7fa')
    
    text=ft.Row([ft.Text("Bienvenue sur MI_P🎯INT",size=26,weight="bold",color='white')],alignment=ft.MainAxisAlignment.CENTER)
   
    tex=ft.Row([ft.Text("L'application de pointage des etudiants,de verification des enseignants,et de supervision pour l'administration"
                ,size=18,color='white')],alignment=ft.MainAxisAlignment.CENTER)
    
    commencer=ft.Row([ft.ElevatedButton('COMMENCER',animate_size=50,bgcolor='#90EE90',width=200,height=50,on_click=COMMENCER,style=ft.ButtonStyle(color='black'))],alignment=ft.MainAxisAlignment.CENTER)
   
    saut=ft.Row(height=30)

    #champ=[ft.Column([img,text,tex,ft.Row([commencer],vertical_alignment = ft.MainAxisAlignment.CENTER)],alignment=ft.MainAxisAlignment.CENTER)]
    champ=[img,text,tex,saut,commencer]
    #return[ft.Row(champ,alignment=ft.MainAxisAlignment.CENTER,expand=True)]
    return champ
                           
                        
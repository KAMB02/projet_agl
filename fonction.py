import mysql.connector
from mysql.connector import Error
from datetime import datetime

# Fonction de connexion unique
def get_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='donnee_app',
            user='root',
            password='Kamssone25',
            port='3308',
            charset='utf8'
        )
        return connection
    except Error as e:
        print(f"Erreur lors de la connexion à MySQL: {e}")
        return None

# Cache pour la connexion
_connection = None

def get_db_connection():
    global _connection
    if _connection is None or not _connection.is_connected():
        _connection = get_connection()
    return _connection

def liste_utilisateur(user):  
    """
    cette fonction prends en parametre le type d'utilisateur 
    puis return la liste des elements de la base depuis la base de donnee
    
    exemple:
    
    resultat =liste_utilisateur(etudiant)
    
    retourne la liste des etudiants dans la variable resultat
    
    """
    try:
        connection = get_db_connection()
        if connection is None:
            return []
            
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {user}")
        liste_utilisateur = list(cursor.fetchall())
        connection.commit()
        return liste_utilisateur

    except Error as e:
        print(f"Erreur lors de la requête à MySQL: {e}")
        return []
    finally:
        cursor.close()

def stat_etu():
    """
    
    """
    try:
        # Connexion à la base de données
        connection = mysql.connector.connect(
            host='localhost',  # adresse de serveur MySQL
            database='donnee_app',  # base de données utiliser
            user='root',  # nom d'utilisateur MySQL
            password='Kamssone25',port='3308',  # Remplacez par votre mot de passe MySQL
            charset='utf8'
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            # Requête SQL pour insérer un nouveau etudiant
            
            cursor.execute("""
                        SELECT e.Nom, e.Prenoms, COUNT(p.IP) AS total_presences
                        FROM Etudiant e
                        JOIN Presence_etu p ON e.IP = p.IP
                        GROUP BY e.Nom, e.Prenoms;   
                    """)
            taux_presence = list(cursor.fetchall())
            
            
            cursor.execute("SELECT COUNT(*) FROM Presence_ens")
            total_seances = cursor.fetchone()[0]  
            
            connection.commit()

    except Error as e:
        print(f"Erreur lors de la connexion à MySQL: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connexion MySQL fermée")

    list_taux_presence=[]
    for i in range(len(taux_presence)):
        res=(taux_presence[i][2]/total_seances)*100 if total_seances > 0 else 0
        ch=str(taux_presence[i][0])+' '+str( taux_presence[i][1])
        list_taux_presence.append((ch,round(res, 2),taux_presence[i][2],total_seances))
    return list_taux_presence

def stat_ens():
    """
    
    """
    try:
        # Connexion à la base de données
        connection = mysql.connector.connect(
            host='localhost',  # Adresse du serveur MySQL
            database='donnee_app',  # Base de données à utiliser
            user='root',  # Nom d'utilisateur MySQL
            password='Kamssone25',port='3308',  # Remplacez par votre mot de passe MySQL
            charset='utf8'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            
            # Exécution de la première requête et lecture de tous les résultats
            cursor.execute("""
                    SELECT ens.Nom, ens.Prenoms, COUNT(p.Id_ens) AS total_presences
                    FROM Enseignant ens
                    JOIN Presence_ens p ON ens.Id_ens = p.Id_ens
                    GROUP BY ens.Nom, ens.Prenoms;
                    """)
            nbr_presence_ens = list(cursor.fetchall())
            
            # Exécution de la deuxième requête et lecture de tous les résultats
            cursor.execute("""                         
                    SELECT ens.Nom, ens.Prenoms, COUNT(emp.Id_cours) AS total_presence 
                    FROM emploi_du_temps emp
                    JOIN enseignant ens ON emp.Id_cours = ens.Id_cours
                    GROUP BY ens.Nom, ens.Prenoms;                           
                """)
            total_seances = cursor.fetchall()  
            
            connection.commit()

    except mysql.connector.Error as e:
        print(f"Erreur lors de la connexion à MySQL : {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connexion MySQL fermée")

    # Calcul de la liste des taux de présence
    list_taux_presence = []
    for i in range(len(nbr_presence_ens)):
        total_seances_ens = total_seances[i][2] if i < len(total_seances) else 0
        taux_presence = (nbr_presence_ens[i][2] / total_seances_ens) * 100 if total_seances_ens > 0 else 0
        nom_complet = f"{nbr_presence_ens[i][0]} {nbr_presence_ens[i][1]}"
        list_taux_presence.append((nom_complet, round(taux_presence, 2), nbr_presence_ens[i][2], total_seances_ens))
    return list_taux_presence

def emploi_du_temps_prof(id):  
    """
    renvoie l'emploi du temps de d'un enseignant 
    a partir de son identifiant
    Returns:
        list: Une liste contenant quatre listes :
            - date_cours (list): Les dates des cours.
            - matiere (list): Les noms des matières.
            - heure_debut (list): Les heures de début des cours.
            - heure_fin (list): Les heures de fin des cours.
    """   
    try:
        # Connexion à la base de données
        connection = mysql.connector.connect(
            host='localhost',  # adresse de serveur MySQL
            database='donnee_app',  # base de données utiliser
            user='root',  # nom d'utilisateur MySQL
            password='Kamssone25',port='3308',  # Remplacez par votre mot de passe MySQL
            charset='utf8'
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            # Requête SQL pour insérer un nouveau etudiant
            
            cursor.execute(f"""
                            SELECT 
                            e.Nom,e.Prenoms,c.Libelle AS Cours,
                            edt.Date_cours,edt.jours,edt.heure_deb,
                            edt.heure_fin,s.Libelle AS Salle
                            FROM Emploi_du_temps edt
                            JOIN Cours c ON edt.Id_cours = c.Id_cours
                            JOIN Enseignant e ON c.Id_cours = e.Id_cours
                            JOIN Salle s ON edt.Id_salle = s.Id_salle
                            WHERE e.Id_ens = '{id}';       
                            """)
            stat_cr = list(cursor.fetchall())
            connection.commit()

    except Error as e:
        print(f"Erreur lors de la connexion à MySQL: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connexion MySQL fermée")

    date_cours=[]
    matiere=[]        
    heure_debut=[]
    heure_fin=[]
    nom_prenoms=[]
    # ajout des element dans chaque liste 
    for i in range (len(stat_cr)):
        date_cours.append(stat_cr[i][3])
        matiere.append(stat_cr[i][2])
        heure_debut.append(stat_cr[i][5])
        heure_fin.append(stat_cr[i][6])  
        nom_prenoms.append(str(stat_cr[i][0])+" "+stat_cr[i][1])
        
    return [date_cours,matiere,heure_debut,heure_fin,nom_prenoms]

def infos_presence_enseignant():
    """
    
    """
    try:
        # Connexion à la base de données
        connection = mysql.connector.connect(
            host='localhost',  # Adresse du serveur MySQL
            database='donnee_app',  # Base de données à utiliser
            user='root',  # Nom d'utilisateur MySQL
            password='Kamssone25',port='3308',  # Remplacez par votre mot de passe MySQL
            charset='utf8'
        )

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM presence_ens;")
            list_presence = list(cursor.fetchall())  
            
            connection.commit()

    except mysql.connector.Error as e:
        print(f"Erreur lors de la connexion à MySQL : {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Connexion MySQL fermée")

    Id_ens=[]
    date=[]
    heure_debut=[]
    heure_fin=[]
    for i in range(len(list_presence)):
         Id_ens.append(list_presence[i][1]) 
         date.append(list_presence[i][3])
         heure_debut.append(list_presence[i][4])
         heure_fin.append(list_presence[i][5])
         
    return [Id_ens,date,heure_debut,heure_fin]

def comparer_dates(date1_str, date2_str):
    """
    Compare deux dates et affiche laquelle est antérieure, postérieure ou si elles sont égales.

    Args:
        date1_str (str): La première date sous forme de chaîne de caractères (format: 'YYYY-MM-DD').
        date2_str (str): La deuxième date sous forme de chaîne de caractères (format: 'YYYY-MM-DD').

    Returns:
        str: Un message indiquant le résultat de la comparaison.
    """
    # Convertir les chaînes de caractères en objets datetime
    date1 = datetime.strptime(date1_str, '%Y-%m-%d')
    date2 = datetime.strptime(date2_str, '%Y-%m-%d')

    # Comparer les dates
    if date1 < date2:
        return f"La date {date1_str} est antérieure à la date {date2_str}."
    elif date1 > date2:
        return f"La date {date1_str} est postérieure à la date {date2_str}."
    else:
        return f"La date {date1_str} est égale à la date {date2_str}."


def emploi_du_temps():  
    """
    renvoie l'emploi du temps 
    Returns:
        list: Une liste contenant quatre listes :
            - date_cours (list): Les dates des cours.
            - matiere (list): Les noms des matières.
            - heure_debut (list): Les heures de début des cours.
            - heure_fin (list): Les heures de fin des cours.
    """   
    try:
        connection = get_db_connection()
        if connection is None:
            return [[], [], [], []]
            
        cursor = connection.cursor()
        cursor.execute("""
                    SELECT Date_cours,Libelle,heure_deb,heure_fin
                    FROM emploi_du_temps emp,cours crs
                    WHERE crs.Id_cours=emp.Id_cours
                    order by Date_cours;      
                            """)
        stat_cr = list(cursor.fetchall())
        connection.commit()

        date_cours=[]
        matiere=[]        
        heure_debut=[]
        heure_fin=[]
        nom_prenoms=[]
        # ajout des element dans chaque liste 
        for i in range (len(stat_cr)):
            date_cours.append(stat_cr[i][0])
            matiere.append(stat_cr[i][1])
            heure_debut.append(stat_cr[i][2])
            heure_fin.append(stat_cr[i][3])  
            
        return [date_cours,matiere,heure_debut,heure_fin]

    except Error as e:
        print(f"Erreur lors de la requête à MySQL: {e}")
        return [[], [], [], []]
    finally:
        cursor.close()


heur=infos_presence_enseignant()[2]

# # Exemple d'utilisation
# date1 = "2025-03-13"
# date2 = "2025-03-13"

# resultat = comparer_dates(date1, date2)
# print(str(heur[0])[:2]<str(heur[0])[:2], "a"<"d")

# print(liste_utilisateur('enseignant'))
# res=statut_cours()
# print(statut_cours('ENS001'))
            
# print(Id_date_enseignant_present())
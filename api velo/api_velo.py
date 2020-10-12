import json
import requests
import pandas as pd

class api_connector():
    """
    Se connecte aux différentes API
    """
    def get_api(self,url):
        response = requests.request("GET",url)
        response_json = json.loads(response.text.encode('utf-8'))
        return response_json.get("records",[])
    
    def get_lille(self):
        url = "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&rows=2000&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion"
        return self.get_api(url)
    
    def get_rennes(self):
        url = "https://data.rennesmetropole.fr/api/records/1.0/search/?dataset=etat-des-stations-le-velo-star-en-temps-reel&q=&rows=2000&facet=nom&facet=etat&facet=nombreemplacementsactuels&facet=nombreemplacementsdisponibles&facet=nombrevelosdisponibles"
        return self.get_api(url)
    
    def get_lyon(self):
        url = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=station-velov-grand-lyon&q=&rows=2000&facet=name&facet=commune&facet=bonus&facet=status&facet=available&facet=availabl_1&facet=availabili&facet=availabi_1&facet=last_upd_1"
        return self.get_api(url)
    
    def get_paris(self):
        url = "https://opendata.paris.fr/api/records/1.0/search/?dataset=velib-disponibilite-en-temps-reel&q=&rows=2000&facet=name&facet=is_installed&facet=is_renting&facet=is_returning&facet=nom_arrondissement_communes"
        return self.get_api(url)
    
class data_cleaner_for_collection():
    """
    nettoie les différents datasets
    """
    def clean_all(self,dflille,dfrennes,dflyon,dfparis):
        dflilleclean = self.clean_lille(dflille)
        dfrennesclean = self.clean_rennes(dfrennes)
        dflyonclean = self.clean_lyon(dflyon)
        dfparisclean = self.clean_paris(dfparis)

        return(pd.concat([dflilleclean,dfrennesclean,dflyonclean,dfparisclean],ignore_index=True))
        
        
    def clean_lille(self,dflille):
        dflilleclean = dflille[['fields.nom','fields.geo','fields.type','fields.etat']].drop_duplicates(subset=['fields.nom'])
        dflilleclean = dflilleclean.rename(columns={'fields.nom':'Name','fields.geo':'Geo','fields.type':'TPE','fields.etat':'Available'})
        
        # get the size of Lille Stations by adding the number of availables places and bicycles
        size = []
        for i, row in dflille.iterrows():
            size.append(row['fields.nbvelosdispo']+row['fields.nbplacesdispo'])
    
        dflilleclean = pd.concat([dflilleclean,pd.DataFrame(size, columns = ['Size'])], axis=1, join='inner')
    
        # set the 'tpe' column with boolean
        dflilleclean['TPE'] = dflilleclean['TPE'].replace("AVEC TPE","True")
        dflilleclean['TPE'] = dflilleclean['TPE'].replace("SANS TPE","False")
    
        # set the 'Available' column with boolean
        dflilleclean['Available'] = dflilleclean['Available'].replace("EN SERVICE","True")
    
        for i, row in dflilleclean.iterrows():
            if not row['Available'] == 'True':
                dflilleclean['Available'].loc[i] = 'False'
                
        return(dflilleclean)
    
    def clean_rennes(self,dfrennes):
        dfrennesclean = dfrennes[["fields.nom","fields.coordonnees","fields.etat","fields.nombreemplacementsactuels"]].drop_duplicates(subset=['fields.nom'])
        dfrennesclean = dfrennesclean.rename(columns={'fields.nom':'Name','fields.coordonnees':'Geo','fields.type':'TPE','fields.etat':'Available','fields.nombreemplacementsactuels':'Size'})
    
        # set the 'Available' column with boolean
        dfrennesclean['Available'] = dfrennesclean['Available'].replace("En fonctionnement","True")
    
        for i, row in dfrennesclean.iterrows():
            if not row['Available'] == 'True':
                dfrennesclean['Available'].loc[i] = 'False'
            
        return(dfrennesclean)
    
    def clean_lyon(self,dflyon):
        dflyonclean = dflyon[["fields.name","fields.geo_shape.coordinates","fields.status","fields.bike_stand"]].drop_duplicates(subset=['fields.name'])
        dflyonclean = dflyonclean.rename(columns={'fields.name':'Name','fields.geo_shape.coordinates':'Geo','fields.status':'Available','fields.bike_stand':'Size'})
    
        # set the 'Available' column with boolean
        dflyonclean['Available'] = dflyonclean['Available'].replace("OPEN","True")
    
        for i, row in dflyonclean.iterrows():
            if not row['Available'] == 'True':
                dflyonclean['Available'].loc[i] = 'False'
        
        return(dflyonclean)
    
    def clean_paris(self,dfparis):
        dfparisclean = dfparis[["fields.name","fields.coordonnees_geo","fields.is_renting","fields.capacity"]].drop_duplicates(subset=['fields.name'])
        dfparisclean = dfparisclean.rename(columns={'fields.name':'Name','fields.coordonnees_geo':'Geo','fields.is_renting':'Available','fields.capacity':'Size'})
    
        # set the 'Available' column with boolean
        dfparisclean['Available'] = dfparisclean['Available'].replace("OUI","True")
    
        for i, row in dfparisclean.iterrows():
            if not row['Available'] == 'True':
                dfparisclean['Available'].loc[i] = 'False'
                
        return(dfparisclean)    

def send_collection():
    """
    se connecte aux API et renvoie de quoi remplir la table 'Collection' sous forme de JSON
    """
    # collect data
    ac = api_connector()
    
    dflille = pd.json_normalize(ac.get_lille())
    
    dfrennes = pd.json_normalize(ac.get_rennes())
    
    dflyon = pd.json_normalize(ac.get_lyon())
    
    dfparis = pd.json_normalize(ac.get_paris())
    
    #clean data
    dc = data_cleaner_for_collection()
    response = dc.clean_all(dflille, dfrennes, dflyon, dfparis)
    
    return(response.to_json(orient='records'))
    
if __name__ == '__main__':
    print(send_collection())
import json
import requests
import pandas as pd

class api_connector():
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
    
    
if __name__ == '__main__':
    ac = api_connector()
    
    dflille = pd.json_normalize(ac.get_lille())
    print(dflille.head())
    
    dfrennes = pd.json_normalize(ac.get_rennes())
    print(dfrennes.head())
    
    dflyon = pd.json_normalize(ac.get_lyon())
    print(dflyon.head())
    
    dfparis = pd.json_normalize(ac.get_paris())
    print(dfparis.head())
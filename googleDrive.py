from calendar import c
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

ITEM_SHEET = 'items' # Nombre de la ventana dentro de la hoja de calculo
CLIENT_SHEET = 'clients'
COMANDS_SHEET= 'comands'
WORKSHEET_ID = "1wyywvBKzlxxrvx6iFGOf4xBM3eKPHHJWdfoUG_livhc" # TROZO del url de la hoja de calculo

class shop_data:

    def __init__(self):
       
        scope = ["https://spreadsheets.google.com/feeds",
                 'https://www.googleapis.com/auth/spreadsheets',
                 "https://www.googleapis.com/auth/drive.file",
                 "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name('access_key.json', scope) # instanciar credenciales para tener acceso al google sheets
        
        self.client = gspread.authorize(creds) # Aplicar las credenciales
        self.sheet = self.client.open_by_key(WORKSHEET_ID)  # Abrir spreadhseet con el id de la hoja de google
    
    def get_items(self):
        print("ha entrado a productos")
        sheet = self.sheet.worksheet(ITEM_SHEET)
        items = pd.DataFrame(sheet.get_all_records())  # Obtener todos los registros
       
        return items
    
    def client_info(self, user_info):
        sheet = self.sheet.worksheet(CLIENT_SHEET)
        #comprobar que el usuario no exista en la hoja 
        # #Añadir usuario a la hoja
        sheet.add_rows(1)
        sheet.append_row([element for element in user_info])
       
        #items = pd.DataFrame(sheet.get_all_records())
        #print("-------------------------\n",items)
    
    def register_comanda(self, lista_comanda):
        print("atemto a enviar comanda")
        sheet = self.sheet.worksheet(COMANDS_SHEET)
        sheet.add_rows(1)
        sheet.append_row([element for element in lista_comanda])
        
       



        

#if __name__ == "__main__":
    #print(shop_data().get_items())

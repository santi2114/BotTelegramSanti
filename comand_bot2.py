import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from telebot.types import ForceReply
from googleDrive import shop_data
from telebot import types
import pandas as pd


bot = telebot.TeleBot("5714810199:AAEKWVMMG2OUz8VHR_CRhEXhIKUkHVapKLo")
shopdata= shop_data()
CHAT_ID = 902933215 #es necesario para poder enviar cualquier mensage dentro de un funcion sin parámetos de entrada
tomar_comanda=[]

@bot.message_handler(commands=['start']) #responder a al comandp /start
def start(message):
   
    markup = ForceReply()
    user_name=message.from_user.first_name
   
    msg = bot.send_message(message.chat.id, f"Hola {user_name}, bienvenido a pasteleria Cucurella 👋😄")
    
    CHAT_ID = message.chat.id
    bot.register_next_step_handler(msg, get_client_choice)
    
    
#mostrar botones realizar comanda y ver menú
def get_client_choice(message):
   
    markup= types.ReplyKeyboardMarkup(one_time_keyboard = True, input_field_placeholder= "Pulsa un botton: ", resize_keyboard = True)
    markup.add("Ver productos 👀","Realizar comanda 📝") #botones para eleguir si mostrar prductos o realizar comanda
    msg = bot.send_message(message.chat.id, "¿Que desear realizar ?", reply_markup = markup)

    bot.register_next_step_handler(msg, check_client_choice)

def check_client_choice(message):
    #comprobar entrada botón 
  
    if message.text == "Ver productos 👀":
         
         show_items(message)

    # ver productos
    if  message.text == "Realizar comanda 📝" :
       
         bot.send_message(message.chat.id, "Ha entrado en el proceso de realizar comanda..")
         register_comand(message)
    
@bot.message_handler(commands=['productos']) #responder a al comando /productos
def show_items(message):
   
    items=shopdata.get_items()
    it=items.to_string(index = False, header = False)
  
    bot.send_message(CHAT_ID, f"{it}") #esconder indice de la la tabla e imprimir
    bot.send_message(CHAT_ID, "Tiene a su disposición los comandos: \n /productos -> para ver productos \n /comanda -> para realizar compra ")
    


#Se realiza la comanda mediante botones
@bot.message_handler(commands=['comanda'])
def register_comand(message):

    keyboard_inline = InlineKeyboardMarkup(row_width = 2)
    button1 = InlineKeyboardButton("Crusanes normales 🥐 10un", callback_data="10 Cruanes normales")
    button2 = InlineKeyboardButton("Crusanes nocilla 🥐🍫 10un", callback_data="10 Crusanes nocilla")
    button3 = InlineKeyboardButton("Donuts choco con letche 🍩 20un", callback_data="20 Donus choco con letche")
    button4 = InlineKeyboardButton("Cupkakes variados 🧁 15un", callback_data="15 Cupkakes variados")
    button5 = InlineKeyboardButton("Pastel nata y fresa 🍰 1un", callback_data="Pastel nada y fresa")
    button6 = InlineKeyboardButton("Pastel chocolate 🎂🍫 1un", callback_data="Pastel chocolate")
    button7 = InlineKeyboardButton("Finalizar comanda", callback_data = "fin")

    keyboard_inline.add(button1, button2, button3, button4, button5, button6, button7)
    bot.send_message(message.chat.id, "Cada artículo que pulse se añadirá automáticamente a tu lista de comanda: ", reply_markup = keyboard_inline )

@bot.callback_query_handler(func = lambda x: True) #responder a al comandp /start
def responder_botones(call):
    
    cid = call.from_user.id
    mid= call.message.id

    if call.data == "fin":
        bot.send_message(CHAT_ID, f"<b>Revisando su comanda: </b>📝🔍", parse_mode = "html")
        
        #se le imprime la lista tomar_comanda al usuario con los productos que este ha eleguido
        for x in range(len(tomar_comanda)):
           comand = tomar_comanda[x] 
           bot.send_message(CHAT_ID,f"<i>{comand}</i>", parse_mode = "html")
       
        bot.delete_message(cid, mid) 
        confirm_comand() 

    #cada botón que el susuario pulse añadirà el producto correspondiente a la lista ->tomar_comanda[]
    if call.data == "10 Cruanes normales":
        tomar_comanda.append(call.data)
    if call.data == "10 Crusanes nocilla":
        tomar_comanda.append(call.data)
    if call.data == "20 Donus choco con letche":
        tomar_comanda.append(call.data)
    if call.data == "15 Cupkakes variados":
        tomar_comanda.append(call.data)
    if call.data == "1 Pastel nada y fresa":
        tomar_comanda.append(call.data)
    if call.data == "1 Pastel chocolate":
        tomar_comanda.append(call.data)


#confirmar comanda pulsando botones si o no
def confirm_comand():
   
    markup=ReplyKeyboardMarkup(one_time_keyboard = True, input_field_placeholder= "Pulsa un botton: ", resize_keyboard = True)
    markup.add("Sí ✅","No ❌") #botones para eleguir si mostrar prductos o realizar comanda
    msg = bot.send_message(CHAT_ID, "¿Quieres proceder con la comanda ?", reply_markup = markup)

    bot.register_next_step_handler(msg, responder_botones2)

def responder_botones2(message):

    if message.text == "Sí ✅":
      
        keyboard = types.ReplyKeyboardMarkup (row_width = 1, resize_keyboard = True) # Connect the keyboard
        button_phone = types.KeyboardButton (text = 'Númer de teléfono', request_contact = True) # crear boton para enviar número de teléfono
        keyboard.add (button_phone) #Aañadir el botón al teclado
        t = bot.send_message (CHAT_ID, 'Porfavor envie su número de teléfono \npara proceder con la comanda 📞', reply_markup = keyboard)
   
    # Duplicate with a message that the user will now send his phone number to the bot (just in case, but this is not necessary)
    if  message.text == "No ❌":
        bot.send_message(CHAT_ID, "Se ha <b>cancelalo</b> la comanda correctamente", parse_mode = "html")


#Acceder a la info del usuario e enviarla a googlesheets
@bot.message_handler (content_types = ['contact'])
def get_user_info(message):
   
    if message.contact is not None:     
        
        #crear una lista con la info del cliente
        user_info = [message.contact.phone_number, message.contact.first_name, message.contact.last_name, message.chat.id]
        #enviar la lista al método client_info que está en googleDrive que se encargará de subirlo     
        shopdata.client_info(user_info)
        
        #Añadir al principio de la comanda info del usuario
        tomar_comanda.insert(0,message.chat.id)
        tomar_comanda.insert(1,message.from_user.first_name)
        tomar_comanda.insert(2,message.from_user.last_name)
       
        bot.register_next_step_handler(message, get_data_comand) # obtener data de la comanda

    else: 
        bot.send_message("Tiene que introducir un número de teléfono válido")

def get_data_comand(message):
    
    bot.send_message (message.chat.id,"HORARIO 🕝 \nDe Lunes a Viernes 09.00 a 14.00")
    msg =  bot.send_message (message.chat.id," Introduzca la data de la recogida del pedido \n con el formato <b>dd/mm hh/mm</b> \n Ejeplo: 24/12 09:20", parse_mode = "html") 
    bot.register_next_step_handler(msg, check_data_comand)

def check_data_comand(message):
    
    date = message.text
   
    cont  = 0
    day = ""
    month = ""
    year = ""
    hour="" 
    min = ""
    hole_date=""
   
    for c in date:
        #obtener el día y dar foemato
       if cont <= 1:
        day += c
        hole_date+= c
       if cont == 2:
        hole_date+= "/"
       
       #obtener el mes y dar formato
       if cont >= 3 and cont <= 4:
        month += c
        hole_date+= c
       if cont == 5:
        hole_date+= " " 
      
       #obtener hora y dar formato
       if cont >= 6 and cont <= 7:
        hour += c
        hole_date+= c

       if cont == 8:
        hole_date+= ":"  
       if cont >= 9 and cont <= 10:
        min += c  
        hole_date+= c

       cont += 1
    
    #si se consigue convertir el texto de usuario a int y no peta comprobar si corresponde 
    try:
        tomar_comanda.insert(3,hole_date) #añadir la data a la lista[]
        shopdata.register_comanda(tomar_comanda)# enviar comanda del usuario a la funcion que se encarga de subir-la a googlesheets 
        bot.send_message(message.chat.id,"Comanda realizada correctamente!! 😁👍") #confirmar al usuario la comanda
    
    except:

       msg = bot.send_message (message.chat.id, "EL formato de data es incorrecto")
       bot.register_next_step_handler(msg, get_data_comand)


    

if __name__ == '__main__':
    print("inicindo bot...")
    bot.infinity_polling()
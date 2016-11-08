import sys
import time
import telepot
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardHide 
import  RPi.GPIO as GPIO
import picamera
import Adafruit_CharLCD as LCD
import pyqrcode
import qrtools

note = False
i = 0
chat_id = 0

#generates and saves the QR code for the entry id with timestamp
def generate_qr_code(id):
    qr = pyqrcode.create(id)
    qr.png(id+".png", scale=6)

#extracts data from the read QR code image  
def read_qr_code(qr_recvd):
    qr = qrtools.QR()
    qr.decode(qr_recvd)
    id_recvd =  qr.data
    if(search(id_recvd)):
        #grant access if the timestamp is not too old
    else:
        #display an error and inform the master user
        
#extract the QR code from a big image 
def extract_QR(input_image):
    #TODO
    print "Extracting QR from input"   

def on_chat_message(msg):
    global note, chat_id
    content_type, chat_type, chat_id = telepot.glance(msg)

    keyboard_on = ReplyKeyboardMarkup(keyboard=[    
                    [KeyboardButton(text='Open Sherlock')], [KeyboardButton(text='Close Sherlock')], [KeyboardButton(text='Leave Note')] ])

    keyboard_off = ReplyKeyboardHide(hide_keyboard=True)

    keyboard_in = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='Yes!', callback_data='press')],
               ])

    print msg['text']
    bot.sendMessage(chat_id, msg['text'], reply_markup=keyboard_on)
    if note == False:

      if (msg['text'] == "Open Sherlock"):
        GPIO.output(20, True)
      elif (msg['text'] == "Close Sherlock"):
        GPIO.output(20, False)
      elif (msg['text'] == "Leave Note"): 
        bot.sendMessage(chat_id,'Note to be written:', reply_markup=keyboard_off)
        note = True

    else:
      lcd.clear()
      lcd.message(msg['text'])
      bot.sendMessage(chat_id, 'Done?', reply_markup=keyboard_in)



def Send_pic(chat_id):
    lcd.clear()
    lcd.message('Look at the camera!')
    camera.start_preview()
    time.sleep(2)
    global i
    imagename = "image" + str(i) + ".jpg"
    camera.capture(imagename)
    i = i+1
    camera.stop_preview()
    bot.sendPhoto(chat_id=chat_id, photo=open(imagename, 'rb'))
    lcd.clear()
    lcd.message('Waiting for reply')


def on_callback_query(msg):
    global note
    note = False
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print('Callback Query:', query_id, from_id, query_data)

    bot.answerCallbackQuery(query_id, text='Got it')


# Raspberry Pi pin configuration:
lcd_rs        = 25  # Note this might need to be changed to 21 for older revision Pi's.
lcd_en        = 24
lcd_d4        = 23
lcd_d5        = 17
lcd_d6        = 27
lcd_d7        = 22
lcd_backlight = 4
# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2
# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)

lcd.message('Welcome to Prakhar\'s place')

camera = picamera.PiCamera()

GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(20, GPIO.OUT, initial=GPIO.LOW)
bot = telepot.Bot('299154848:AAEzu68oyqou90f2q4T1ON8mCSQ8sWkegVQ')

bot.message_loop({'chat': on_chat_message,
                  'callback_query': on_callback_query})
print('Listening ...')


try:
    while 1:
        time.sleep(1)
        while GPIO.input(12):
            pass
        Send_pic(chat_id)

except KeyboardInterrupt:
  lcd.clear()
  GPIO.cleanup()

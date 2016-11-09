import qrtools
import sys
import signal
import zbar 

def print_msg(msg):
	print(msg)

def callback(msg):
	print (msg)

def data_recognise(data=None):
        """Returns an unicode string indicating the data type of the data paramater"""
        data = data
        data_lower = data.lower()
        if data_lower.startswith(u"http://") or data_lower.startswith(u"https://"):
            return u'url'
        elif data_lower.startswith(u"mailto:"):
            return u'email'
        elif data_lower.startswith(u"matmsg:to:"):
            return u'emailmessage'
        elif data_lower.startswith(u"tel:"):
            return u'telephone'
        elif data_lower.startswith(u"smsto:"):
            return u'sms'
        elif data_lower.startswith(u"mmsto:"):
            return u'mms'
        elif data_lower.startswith(u"geo:"):
            return u'geo'
        elif data_lower.startswith(u"mebkm:title:"):
            return u'bookmark'
        elif data_lower.startswith(u"mecard:"):
            return u'phonebook'
        else:
            return u'text'

def decode_webcam(device='/dev/video0'):
        # create a Processor
        proc = zbar.Processor()

        # configure the Processor
        proc.parse_config('enable')

        # initialize the Processor
        proc.init(device)

        # setup a callback
        def my_handler(proc, image, closure):
            # extract results
            for symbol in image:
                if not symbol.count:
                    data = symbol.data
                    data_type = data_recognise(data)
		    callback(symbol.data)
        proc.set_data_handler(my_handler)

        # enable the preview window
        proc.visible = False

        # initiate scanning
        proc.active = True
       	try:
       		proc.user_wait(20)
	except zbar.WindowClosed:
       		pass

decode_webcam()

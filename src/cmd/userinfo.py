# userinfo command
import tempfile
import os

def userinfo_handler(update, context):
	with tempfile.NamedTemporaryFile() as tmp
		with open(tmp.name, 'w') as f:
	    	f.write(user_get_info(update))
	    update.message.reply_document(open(tmp, 'rb'), filename="userinfo.json")

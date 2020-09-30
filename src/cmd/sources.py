# sources command

import common

def sources_handler(update, context):

	sources = db_sources()
    info = get_user_info(update)

	# parse optional command
	tail = cmd_tail(update)
	if tail:
		new_sources = []
		for tok in tail.split(' '):
			if tok.isdigit():
				i = int(tok)
				i = ((i - 1) % len(sources) + 1) if i > 0 else 0
				new_sources .append(i )

		# set back in info
		if 0 in new_sources:
			new_sources = []
		elif not len(new_sources):
			new_sources = None
		if new_sources:
			info["sources"] = new_sources
			set_user_info(update, info)			

	# output (user) sources
    msg = ""
    index = 0
    for source in sources:
        index = index + 1;
        marker = "*" if index in info["sources"] else ""
        msg += (str(index) + marker + " " + source["name"] + " - " + source["rss"] + "\n")
    update.message.reply_text(msg)
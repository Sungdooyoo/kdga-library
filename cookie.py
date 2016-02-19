def trim_cookie(cookie):
	if cookie.find("|") == -1:
		print "There's no | "
		return None
	else:
		return cookie.split("|")
import cgi

def escape_html(s):
    return cgi.escape(s,quote = True) 

html = "<br>quote"
print("original : %s") %html
html = escape_html(html)
print(html)


from xmlrpc.client import ServerProxy

url = "https://showbiz.com/xmlrpc.php"

try:
    server = ServerProxy(url)
    print("XML-RPC connection successful")
except Exception as e:
    print("Error:", e)

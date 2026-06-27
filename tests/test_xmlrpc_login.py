from xmlrpc.client import ServerProxy
import ssl

url = "https://showbiz.com/xmlrpc.php"

username = input("WordPress Username: ")
password = input("WordPress Password: ")

context = ssl._create_unverified_context()

server = ServerProxy(
    url,
    context=context
)

try:
    blogs = server.wp.getUsersBlogs(username, password)

    print("\nSUCCESS")
    print("Connected to WordPress")
    print(blogs)

except Exception as e:
    print("\nFAILED")
    print(type(e).__name__)
    print(str(e))
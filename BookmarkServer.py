from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, unquote
import os
import requests

form = '''<!DOCTYPE html>
  <title>Message Board</title>
  <form method="POST">
    <label>Long Url:</label>
    <input type="text" name="LongURI"></input>
    <br>
    <br>
    <label>Short Url:</label>
    <input type="text" name="ShortName"></input>
    <br>
    <button type="submit">Post it!</button>
  </form>
  <pre>
  {}
  </pre>
'''
url_mapping = {}


def CheckURI(uri, timeout=5):

    try:
        req = requests.get(uri)

        if req.status_code == 200:
            return True
        else:
            return False
    except:
        return False


class BookmarkServer(BaseHTTPRequestHandler):

    def do_GET(self):
        page = unquote(self.path[1:])
        if page in url_mapping:
            self.send_response(303)
            self.send_header("Location",url_mapping[page])
            self.end_headers()
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(form.encode())

    def do_POST(self):

        length = int(self.headers.get("Content-Length", 0))
        data = self.rfile.read(length).decode()

       
        
        if 'LongURI' in parse_qs(data) and 'ShortName' in parse_qs(data):
            url1 = parse_qs(data)['LongURI'][0]
            url2 = parse_qs(data)['ShortName'][0]
            result = CheckURI(url1)
            if result:
                url_mapping[url2] = url1
                self.send_response(303)
                self.send_header("Location","/")
                self.end_headers()
            
            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write("Couldn't fetch URI '{}'. Sorry!".format(url1).encode())
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("Missing form fields!".encode())


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    server_address = ('', port)
    httpd = HTTPServer(server_address, BookmarkServer)
    httpd.serve_forever()
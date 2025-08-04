import http.server
import socketserver
import webbrowser
import os

# Configuration
PORT = 8000
HANDLER = http.server.SimpleHTTPRequestHandler

def main():
    # Change to the directory containing the HTML file
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Create the server
    with socketserver.TCPServer(("", PORT), HANDLER) as httpd:
        print(f"Serving frontend at http://localhost:{PORT}/frontend_demo.html")
        
        # Open the browser automatically
        webbrowser.open(f"http://localhost:{PORT}/frontend_demo.html")
        
        # Serve until interrupted
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == "__main__":
    main()
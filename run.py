from app import create_app
import threading
import tcp_server.server as tcp_server

def run_flask():
    app = create_app()
    app.run(debug=True, use_reloader=False)

def run_tcp_server():
    tcp_server.server_program()

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    tcp_thread = threading.Thread(target=run_tcp_server)
    
    flask_thread.start()
    tcp_thread.start()
    
    flask_thread.join()
    tcp_thread.join()

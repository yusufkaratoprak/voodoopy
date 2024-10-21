import os
from flask import Flask, render_template_string
import threading  # Threading kullanarak diğer Flask uygulamasını başlatacağız
from . import backendserver  # backend dosyasını aynı dizindeki __init__.py'den içe aktarıyoruz

class Gui:
    def __init__(self, page):
        self.page = page

    def start_backend(self):
        # Backend'i ayrı bir thread'de başlatıyoruz, ancak debug ve reloader kapalı
        backendserver.app.run(host="0.0.0.0", port=3001, debug=False, use_reloader=False)

    def run(self, debug=False):
        # Backend'i ayrı bir thread'de başlatıyoruz
        backend_thread = threading.Thread(target=self.start_backend)
        backend_thread.daemon = True  # Ana uygulama kapanınca backend de kapansın
        backend_thread.start()

        # Create the Flask app and specify the static folder location
        app = Flask(__name__)

        @app.route('/')
        def index():
            return render_template_string(self.page.render())

        # GUI uygulamasını 3000 portunda çalıştır
        app.run(host="0.0.0.0", port=3000, debug=debug, use_reloader=False)
        

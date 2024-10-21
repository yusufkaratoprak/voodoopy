import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
import importlib.util

app = Flask(__name__)
CORS(app)

# Project root directory, 2 levels up from voodoo/gui
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, PROJECT_ROOT)

# Ana dizindeki tüm .py dosyalarını bulur ve dinamik olarak tarar
def find_function_in_py_files(function_name):
    for filename in os.listdir(PROJECT_ROOT):
        if filename.endswith(".py") and filename != "backendserver.py":
            try:
                module_name = filename[:-3]  # ".py" uzantısını kaldır
                print(f'Module Name : {module_name}')
                module_path = os.path.join(PROJECT_ROOT, filename)
                print(f'Module Path : {module_path}')
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, function_name):
                    print(f'Found : {function_name}')
                    return getattr(module, function_name)  # Fonksiyonu döndür
            except Exception as e:
                # Hata yakalandı, hata mesajı ekrana yazdırılıyor
                print(f"Error while executing {function_name}: {e}")
    return None  # Fonksiyon hiçbir dosyada bulunmadı

@app.route('/run_function', methods=['POST'])
def run_function():
    data = request.get_json()
    function_name = data.get("function")
    state = data.get("state")
    print("started")
    
    function_to_call = find_function_in_py_files(function_name)
    
    if function_to_call:
        try:
            # Fonksiyon bulundu, çalıştırılıyor
            print("found")
            function_to_call(state)
            return jsonify({"status": "success", "message": f"{function_name} executed"}), 200
        except Exception as e:
            # Hata yakalandı, hata mesajı ekrana yazdırılıyor
            print(f"Error while executing {function_name}: {e}")
            return jsonify({"status": "error", "message": f"Error while executing {function_name}: {str(e)}"}), 500
    else:
        # Fonksiyon bulunamadı
        print("NOT found")
        return jsonify({"status": "error", "message": f"Function {function_name} not found in any .py file"}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3001, debug=True)
import uuid
from voodoo.gui.state import State

class Page:
    def __enter__(self):
        self.content = ""
        self.event_list = []
        self.current_button = None
        self.state = State()  # State nesnesi ekleniyor
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def text(self, text, mode="normal"):
        if mode == "md":
            self.content += f'<h1 class="text-3xl font-bold text-gray-900">{text}</h1>'
        else:
            self.content += f'<p class="text-base text-gray-700">{text}</p>'
        return self  # Method chaining için self döndürülüyor

    def input(self, id=None, text=None):
        if text is None:
            text_value = ""
        else:
            text_value = str(text)

        if id is None:
            id = str(uuid.uuid4())

        # HTML input elementi oluşturuluyor
        self.content += f'<input id="{id}" class="border border-gray-300 p-2 rounded-md w-full" type="text" value="{text_value}">'
        self.state.set(id, text_value)
        return self  # Method chaining'e olanak sağlamak için self döndürülüyor

    def button(self, text, function_ref=None):
        button_id = f"button-{len(self.event_list)}"
        self.current_button = button_id
        self.content += f'<button id="{button_id}" class="mx-2 text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">{text}</button>'

        # Butonla ilişkili fonksiyonu event_list'e ekliyoruz
        if function_ref is not None:
            self.event_list.append([function_ref])
        else:
            print(f"Geçilen fonksiyon referansı None: {function_ref}")
        return self  # Method chaining için self döndürülüyor

    def consolewrite(self, message):
        if self.current_button is not None:
            self.event_list[int(self.current_button.split('-')[-1])].append(f'console.log("{message}");')
        return self  # Method chaining için self döndürülüyor
    
    def callendpoint(self, endpoint, data):
            # API çağrısını ilgili butonun event listesine ekle
        if self.current_button is not None:
            self.event_list[int(self.current_button.split('-')[-1])].append(f"""
                var inputValue = {data};
                fetch('{endpoint}', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json'
                    }},
                    body: JSON.stringify(inputValue)
                }})
                .then(response => response.json())
                .then(data => {{
                    console.log('Success:', data);
                }})
                .catch((error) => {{
                    console.error('Error:', error);
                }});
            """)
        return self  # Method chaining için self döndürülüyor

    def render(self):
        event_scripts = ""
        for idx, events in enumerate(self.event_list):
            function_ref = events[0]
            event_scripts += f"""
            var button_{idx} = document.getElementById('button-{idx}');
            button_{idx}.addEventListener('click', function() {{
                var state = {{}};  // HTML input'lardan state'i topluyoruz
                document.querySelectorAll('input, label').forEach(function(element) {{
                    state[element.id] = element.value;
                }});
                window.state = state;
                console.log("Güncel State:", window.state);

                // Backend'e POST isteği yapılıyor
                fetch('http://localhost:3001/run_function', {{
                    method: 'POST',
                  
                    headers: {{
                         'Content-Type': 'application/json',
                         'Accept': 'application/json'
                    }},
                    body: JSON.stringify({{
                        "function": "{function_ref}",
                        "state": window.state  // State'i JSON'a çeviriyoruz
                    }})
                }})
                .then(data => {{
                    console.log("Response received");
                    console.log("data:", data);
                }})
                .catch((error) => {{
                    console.error('Error:', error);
                }});

                {''.join(events[1:])}  // Diğer event'leri çalıştır
            }});  // Button click event listener
            """
        return f"""
        <html>
        <head>
            <title>Voodoo GUI</title>
            <link href="/static/css/tailwind.min.css" rel="stylesheet" />
            <link href="/static/css/flowbite.min.css" rel="stylesheet" />
            <script src="/static/js/flowbite.min.js"></script>
        </head>
        <body class="bg-gray-50 p-10">
            <div class="max-w-lg mx-auto">
                <div class="bg-white shadow-lg rounded-lg p-6 space-y-4">
                    <h5 class="text-2xl font-semibold leading-tight text-gray-900 mb-4">Getting started with voodoo GUI</h5>
                    {self.content}
                </div>
            </div>
            <script>
                {event_scripts}  // JavaScript event scripts
            </script>
        </body>
        </html>
        """

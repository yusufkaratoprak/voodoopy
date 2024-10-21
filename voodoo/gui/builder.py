import uuid
from voodoo.gui.state import State

class Page:
    def __enter__(self):
        self.content = ""
        self.event_list = {}  # Event list dictionary olarak tanımlandı
        self.state = State()  # State nesnesi eklendi
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def add_panel(self, panel):
        """Panele ait içerikleri sayfaya ekler."""
        self.event_list.update(panel.event_list)
        self.content += panel.render()
        return self

    def Setup(self, title: str, width: str = "max-w-lg", shadow: bool = True, rounded: bool = True):
        shadow_class = "shadow-lg" if shadow else ""
        rounded_class = "rounded-lg" if rounded else ""

        # Sayfanın genel HTML yapısı
        self.content = f'''
        <html>
        <head>
            <title>{title}</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link href="/static/css/tailwind.min.css" rel="stylesheet" />
            <link href="/static/css/flowbite.min.css" rel="stylesheet" />
            <script src="/static/js/flowbite.min.js"></script>
        </head>
        <body class="bg-gray-50 p-10">
            <div class="{width} mx-auto">
                <div class="bg-white {shadow_class} {rounded_class} p-6 space-y-4">
                    <h5 class="text-2xl font-semibold leading-tight text-gray-900 mb-4">{title}</h5>
                    {self.content}
                </div>
            </div>
        '''
        return self

    def render(self):
        event_scripts = ""
       
        for button_id, function_ref in self.event_list.items():
            event_scripts += f"""
            var button = document.getElementById('{button_id}');
            if (button) {{
                console.log("Button with id {button_id} found");
                button.addEventListener('click', function() {{
                    //alert("Button with id {button_id} clicked!");
                    var state = {{}};
                    // Tüm input'lardan state topluyoruz
                    document.querySelectorAll('input').forEach(function(element) {{
                        state[element.id] = element.value;
                    }});
                    console.log("Collected State:", state);

                    // Backend'e POST isteği yapılıyor
                    fetch('http://localhost:3001/run_function', {{
                        method: 'POST',
                        headers: {{
                            'Content-Type': 'application/json',
                            'Accept': 'application/json'
                        }},
                        body: JSON.stringify({{
                            "function": "{function_ref}",
                            "state": state
                        }})
                    }})
                    .then(response => response.json())
                    .then(data => {{
                        console.log("Response received:", data);
                    }})
                    .catch((error) => {{
                        console.error("Error in fetch:", error);
                    }});
                }});  // Button click event listener
            }} else {{
                console.error("Button with id {button_id} not found");
            }}
            """
        
        # Tüm event scriptlerini sayfa içeriğine ekleyip HTML'yi döndürüyoruz
        full_html = self.content + f"""
            <script>
                {event_scripts}
            </script>
        </body>
        </html>
        """
        
        # HTML çıktısını kontrol edelim
        #print(full_html)
        return full_html


class Panel:
    def __enter__(self):
        self.content = ""
        self.event_list = {}
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def text(self, text, mode="normal"):
        if mode == "md":
            self.content += f'<h1 class="text-3xl font-bold text-gray-900">{text}</h1>'
        else:
            self.content += f'<p class="text-base text-gray-700">{text}</p>'
        return self

    def input(self, id=None, text=None):
        text_value = "" if text is None else str(text)
        id = str(uuid.uuid4()) if id is None else id
        self.content += f'<input id="{id}" class="border border-gray-300 p-2 rounded-md w-full" type="text" value="{text_value}">'
        return self

    def button(self, text, function_ref=None):
        # Benzersiz bir ID veriyoruz, eğer yoksa yeni bir GUID üretiyoruz
        button_id = str(uuid.uuid4())
        
        # Buton oluşturuyoruz
        self.content += f'<button id="{button_id}" class="mx-2 text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">{text}</button>'

        # Butonun event'ini kaydediyoruz
        if function_ref is not None:
            self.event_list[button_id] = function_ref
        else:
            print(f"Geçilen fonksiyon referansı None: {function_ref}")
        return self

    def render(self):
        return f'''
        <div class="w-full h-auto mx-auto">
            <div class="bg-pastel-blue shadow-lg rounded-lg p-6 space-y-4">
                {self.content}
            </div>
        </div>
        '''

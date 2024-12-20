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
    
    def initial(self, initial_function=None):
        if initial_function:
            initial_function()
        return self
    
    def end(self, end_function=None):
        if end_function:
            end_function()
        return self

    def setup(self, title: str, width: str = "max-w-lg", shadow: bool = True, rounded: bool = True):
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
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
            <script src="/static/js/flowbite.min.js"></script>
            <script>
                function toggleDarkMode() {{
                    document.documentElement.classList.toggle('dark');
                    localStorage.setItem('theme', document.documentElement.classList.contains('dark') ? 'dark' : 'light');
                }}
                document.addEventListener('DOMContentLoaded', () => {{
                    if (localStorage.getItem('theme') === 'dark') {{
                        document.documentElement.classList.add('dark');
                    }}
                }});
            </script>
        </head>
        <body class="bg-gray-100 dark:bg-gray-800 dark:text-gray-200 transition-colors duration-300 p-10">
            
            <!-- Sağ üst köşede dark mode geçiş butonu -->
            <div class="absolute top-4 right-4 flex flex-col items-center space-y-2">
                <span class="text-gray-800 dark:text-gray-200 font-medium">Mode</span>
                <div class="flex items-center p-1 bg-gray-200 dark:bg-gray-700 rounded-lg">
                    <!-- Gündüz modu ikonu -->
                    <button onclick="toggleDarkMode()" class="w-10 h-10 flex items-center justify-center rounded-l-lg bg-white dark:bg-transparent text-yellow-500 dark:text-gray-400">
                        <i class="fas fa-sun"></i>
                    </button>
                    
                    <!-- Gece modu ikonu -->
                    <button onclick="toggleDarkMode()" class="w-10 h-10 flex items-center justify-center rounded-r-lg bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-400">
                        <i class="fas fa-moon"></i>
                    </button>
                </div>
            </div>

            <div class="{width} mx-auto">
                <div class="bg-white dark:bg-gray-900 {shadow_class} {rounded_class} p-6 space-y-4">
                    <h5 class="text-2xl font-semibold leading-tight text-gray-900 dark:text-gray-100 mb-4">{title}</h5>
                    {self.content}
                </div>
            </div>
        '''
        return self


    def render(self):
        event_scripts = ""
        event_scripts = """
    function toggleDarkMode() {
        document.documentElement.classList.toggle('dark');
        localStorage.setItem('theme', document.documentElement.classList.contains('dark') ? 'dark' : 'light');
    }

    document.addEventListener('DOMContentLoaded', () => {
        if (localStorage.getItem('theme') === 'dark') {
            document.documentElement.classList.add('dark');
        }
    });
"""

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
        if mode == "big":
            self.content += f'<h1 class="text-3xl font-bold text-gray-900">{text}</h1>'
        else:
            self.content += f'<p class="text-base text-gray-700">{text}</p>'
        return self

    def input(self, id=None, text=None, label=None):
        # ID ve placeholder metinleri ayarlanıyor
        input_id = str(uuid.uuid4()) if id is None else id
        placeholder_text = "" if text is None else str(text)
        
        # Label kontrol ediliyor; varsa label ile input ekleniyor, yoksa sadece placeholder ile input ekleniyor
        if label:
            self.content += f'''
                <div class="mb-4">
                    <label for="{input_id}" class="block text-sm font-medium text-gray-700 dark:text-gray-300">{label}</label>
                    <input id="{input_id}" class="border border-gray-300 p-2 rounded-md w-full text-black" type="text" value="{placeholder_text}">
                </div>
            '''
        else:
            self.content += f'''
                <input id="{input_id}" class="border border-gray-300 p-2 rounded-md w-full mb-4 text-black" type="text" placeholder="{placeholder_text}">
            '''
        
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
    
    def newline(self):
        self.content += "<br>"
        return self

    def render(self):
        return f'''
        <div class="w-full h-auto mx-auto">
            <div class="bg-pastel-blue shadow-lg rounded-lg p-6 space-y-4">
                {self.content}
            </div>
        </div>
        '''

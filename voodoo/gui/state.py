class State:
    def __init__(self):
        self.components = {}

    def update_state(self, state_data):
        """Frontend'den gelen state'i günceller."""
        for key, value in state_data.items():
            self.components[key] = value

    def __getattr__(self, name):
        """Dinamik olarak state.input1 gibi çağrılara izin verir."""
        if name in self.components:
            return self.components[name]
        else:
            raise AttributeError(f"'State' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        """Dinamik olarak state.input1 = 'değer' şeklinde atama yapmayı sağlar."""
        if name == 'components':
            super().__setattr__(name, value)
        else:
            self.components[name] = value

    def set(self, key, value):
        """Yeni bir state bileşeni ekler veya var olanı günceller."""
        self.components[key] = value
        print(f"State'deki {key} güncellendi: {value}")

    def get(self, key, default=None):
        """State içinden bir bileşeni alır, yoksa varsayılan değeri döner."""
        return self.components.get(key, default)

    def get_state(self):
        """Tüm component değerlerini döner."""
        return self.components
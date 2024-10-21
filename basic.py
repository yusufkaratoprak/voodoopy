from voodoo.gui import Gui
import voodoo.gui.builder as vo

def process_data(state):
    print(f"Process Data State: {state['input1']} , {state['input2']}")

def another_function(state):
    print(f"Another : Process Data State: {state['input1']} , {state['input2']}")

# Bu blok GUI'yi yalnızca dosya doğrudan çalıştırıldığında başlatacak
if __name__ == "__main__":
    with vo.Page() as page:
        # Panel başlatıyoruz
        with vo.Panel() as panel:
            panel.text("Let's Make Some Voodoo!", mode="md") \
                  .input(id="input1", text="Değer 1") \
                  .input(id="input2", text="Değer 2") \
                  .button("Submit", "process_data") \
                  .button("Another Button", "another_function")

        page.add_panel(panel)

        page.Setup(title="Getting started with voodoo GUI")
    
    Gui(page).run(debug=True)

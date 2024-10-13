from voodoo.gui import Gui
import voodoo.gui.builder as vo



def process_data(state):
    print(f"Process Data State: {state.input1} , {state.input2}")

def another_function(state):
    print(f"Another : Process Data State: {state.input1} , {state.input2}")

with vo.Page() as page:
    page.text("Let's Make Some Voodoo!", mode="md")
    page.input(id="input1", text="Değer 1")
    page.input(id="input2", text="Değer 2")
    
    # Her buton farklı fonksiyon referansı alıyor
    page.button("Submit", function_ref=process_data).consolewrite(f'submit:{page.state}')
    page.button("Another Button", function_ref=another_function).consolewrite(f'Another button: {page.state}')
    
    gui = Gui(page)
    gui.run(debug=True)
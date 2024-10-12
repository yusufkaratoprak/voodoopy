from voodoo.gui import Gui
import voodoo.gui.builder as vo
import voodoo.gui.state as st

# State nesnesi oluşturuluyor
state = st.State()
state.update_state({
    'input1': 'Değer 1',
    'input2': 'Değer 2'
})

# Backend'de verileri işleyen fonksiyon
def process_data(state):
    print(f"Submit Data Called with: {state.get_state()}")
    print(f"Input 1: {state.get('input1')}, Input 2: {state.get('input2')}")
    
    # Stateleri güncelliyoruz
    state.update_state({
        'input1': 'Değer 3',
        'input2': 'Değer 4'
    })
    
    state.set('input1','Deger 5')
    
    # Frontend'e yeni statelerin yansıtılması için
    return state.get_state()

# GUI oluşturma
with vo.Page() as page:
    page.text("Let's Make Some Voodoo!", mode="md")
    page.input(id="input1", text=state.get('input1'))
    page.input(id="input2", text=state.get('input2'))
    
    # Butona tıklandığında process_data çalıştırılıyor
    page.button("Submit").method(process_data, state).consolewrite("Done").consolewrite(f"Input 1: {state.get('input1')}, Input 2: {state.get('input2')}")

    # GUI'yi başlatıyoruz ve sayfa ile birlikte çalıştırıyoruz
    gui = Gui(page)  # Page nesnesini Gui nesnesine veriyoruz
    gui.run(debug=True)

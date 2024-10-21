from voodoo.gui import Gui
import voodoo.gui.builder as vo

def submit(state):
    print(f"Doctor Info: {state['input1']} , {state['input2']}")

def cancel(state):
    print(f"Doctor Assignment Cancelled Info: {state['input1']} , {state['input2']}")
    
def submitpatient(state):
    print(f"Patient Info: {state['input3']} , {state['input4']}")

def cancelpatient(state):
    print(f"Patient Assignment Cancelled Info: {state['input3']} , {state['input4']}")

# Bu blok GUI'yi yalnızca dosya doğrudan çalıştırıldığında başlatacak
if __name__ == "__main__":
    with vo.Page() as page:
        # Panel başlatıyoruz
        with vo.Panel() as panel1:
            panel1.text("Doctor Appointment", mode="md") \
                  .input(id="input1", text="Doctor Name") \
                  .input(id="input2", text="Doctor SurName") \
                  .button("Submit", "submit") \
                  .button("Cancel", "cancel")

        page.add_panel(panel1)
        
        with vo.Panel() as panel2:
            panel2.text("Patient Info", mode="md") \
                  .input(id="input3", text="Patient Name") \
                  .input(id="input4", text="Patient SurName") \
                  .button("Submit for Patient", "submitpatient") \
                  .button("Cancel Appointment", "cancelpatient")

        page.add_panel(panel2)

        page.Setup(title="System Voodoo Hospital")
    
    Gui(page).run(debug=True)

from tkinter_extension.tk_context import TkContext

from gui.car_assembly_advisor_app import CarAssemblyAdvisorApp

with TkContext() as ctx:
    app = CarAssemblyAdvisorApp(ctx)
    app.mainloop()

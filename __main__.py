import sys

from src.logica.logica_service import LogicaService
from src.vista.InterfazEnForma import App_EnForma
#from src.logica.LogicaMock import LogicaMock

if __name__ == '__main__':
    # Punto inicial de la aplicación

    # logica = LogicaMock()
    logica = LogicaService()

    app = App_EnForma(sys.argv, logica)
    sys.exit(app.exec_())
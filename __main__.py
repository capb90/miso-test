import sys

from src.logica.logica_service import LogicaService
from src.vista.InterfazEnForma import App_EnForma
import src.modelo.declarative_base

#from src.logica.LogicaMock import LogicaMock

if __name__ == '__main__':
    # Punto inicial de la aplicación
    src.modelo.declarative_base.IS_TEST = False

    logica = LogicaService()

    app = App_EnForma(sys.argv, logica)
    sys.exit(app.exec_())
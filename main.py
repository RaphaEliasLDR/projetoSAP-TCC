# main.py

from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivy.core.window import Window
from kivy.core.text import LabelBase

from screens.telaDeInicializacao import TelaDeInicializacao
from screens.telaPedidos import TelaPedidos
from screens.telaMenu import TelaMenu  # Importe a TelaMenu

Window.size = (360, 800)

LabelBase.register(
    name="MontserratBold",
    fn_regular="assets/fonts/Montserrat-Bold.ttf"
)

class SistemaPedidosApp(MDApp):
    def build(self):
        self.title = "Cardápio - SAP"
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"

        sm = MDScreenManager()
        sm.add_widget(TelaDeInicializacao(name="tela_inicial"))
        sm.add_widget(TelaPedidos(name="tela_pedido"))
        sm.add_widget(TelaMenu(name="tela_menu"))  # Adicione a TelaMenu

        sm.current = "tela_inicial"
        return sm

if __name__ == "__main__":
    SistemaPedidosApp().run()
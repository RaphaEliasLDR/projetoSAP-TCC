import subprocess
import threading
import webbrowser
import time
import sys
import socket
import os

from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivy.core.window import Window
from kivy.core.text import LabelBase
from database import DatabaseManager

# Importações das telas
from screens.telaDeInicializacao import TelaDeInicializacao
from screens.telaLogin import TelaLogin
from screens.telaBoasVindas import BoasVindasScreen
from screens.telaPedidos import TelaPedidos
from screens.telaMenu import TelaMenu
from screens.telaCozinha import TelaCozinha
from screens.telaGestao import TelaGestao
from screens.telaMenuGestao import TelaMenuGestao
from screens.telaCadastroFuncionario import TelaCadastroFuncionario
from screens.telaCadastroPrato import TelaCadastroPrato

Window.size = (360, 800)

os.chdir(os.path.dirname(os.path.abspath(__file__)))

LabelBase.register(
    name="MontserratBold",
    fn_regular="assets/fonts/Montserrat-Bold.ttf"
)

def porta_esta_livre(porta=8501):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("127.0.0.1", porta))
        s.close()
        return True  # Porta livre
    except OSError:
        return False  # Porta ocupada

def iniciar_streamlit():
    if not porta_esta_livre(8501):
        print("Streamlit já está rodando na porta 8501. Não iniciando outra instância.")
        return

    caminho_dashboard = os.path.join(os.path.dirname(__file__), "screens", "dashboard.py")


    def run():
        cmd = [
        sys.executable, "-m", "streamlit", "run", caminho_dashboard,
        "--server.headless", "true"
]

        processo = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for linha in processo.stdout:
            print(linha.decode(), end='')

    thread = threading.Thread(target=run, daemon=True)
    thread.start()

    time.sleep(5)

class SistemaPedidosApp(MDApp):
    db = None
    logged_in_user = None
    user_type_ids = {}

    # ALTERE para True se quiser usar o banco de dados
    usar_banco = False

    def build(self):
        # Inicia o Streamlit em background quando o app iniciar
        iniciar_streamlit()

        self.title = "Sistema de Pedidos - SAP"
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"

        if self.usar_banco:
            self.db = DatabaseManager()
            if not self.db.connect():
                print("Erro crítico: Não foi possível conectar ao banco de dados.")
                exit()

            # Carrega os tipos de usuário do banco
            user_types = self.db.get_all_user_types()
            if user_types:
                for tid, tname in user_types:
                    self.user_type_ids[tname] = tid
        else:
            # Dados mock para rodar sem banco
            print("Rodando sem banco de dados: usando dados mock.")
            self.db = None
            self.user_type_ids = {
                "admin": 1,
                "usuario": 2,
            }

        sm = MDScreenManager()
        sm.add_widget(TelaDeInicializacao(name="tela_inicial"))
        sm.add_widget(TelaLogin(name="tela_login"))
        sm.add_widget(BoasVindasScreen(name="tela_boas_vindas"))  
        sm.add_widget(TelaPedidos(name="tela_pedido"))
        sm.add_widget(TelaMenu(name="tela_menu"))
        sm.add_widget(TelaCozinha(name="tela_cozinha"))
        sm.add_widget(TelaGestao(name="tela_gestao"))
        sm.add_widget(TelaMenuGestao(name="tela_menu_gestao")) 
        sm.add_widget(TelaCadastroFuncionario(name='cadastro_funcionario'))
        sm.add_widget(TelaCadastroPrato(name='cadastro_prato'))
        sm.current = "tela_inicial"
        return sm
    
    def mudar_tela(self, screen_name):
        self.root.current = screen_name

    def on_stop(self):
        if self.db:
            self.db.disconnect()

if __name__ == "__main__":
    SistemaPedidosApp().run()

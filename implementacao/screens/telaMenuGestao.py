# screens/telaMenuGestao.py

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.button import Button
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.image import Image
import webbrowser
import subprocess
import sys
import os

class CustomStyledButton(Button):
    button_bg_color = ListProperty([0, 0, 0, 1])
    button_radius = NumericProperty(dp(12))

KV_CONTENT = '''
#:import dp kivy.metrics.dp

<CustomStyledButton>:
    background_normal: ''
    background_down: ''
    background_color: 0,0,0,0
    color: 1, 1, 1, 1
    font_name: "MontserratBold"
    font_size: "18sp"
    size_hint: None, None
    size: dp(250), dp(50)
    pos_hint: {"center_x": 0.5}

    canvas.before:
        Color:
            rgba: self.button_bg_color
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [self.button_radius]

<TelaMenuGestao>:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.066, 0.071, 0.075, 1
        padding: dp(20)
        spacing: dp(30)

        MDBoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.5
            spacing: dp(10)
            MDBoxLayout:
                size_hint: None, None
                size: dp(600), dp(400)
                pos_hint: {'center_x': 0.5}
                Image:
                    source: 'assets/logoSAP.png'
                    fit_mode: 'contain'

        MDBoxLayout:
            orientation: 'vertical'
            size_hint_y: 1
            spacing: dp(20)
            padding: dp(20)

            CustomStyledButton:
                text: 'LISTAR FUNCIONÁRIOS'
                button_bg_color: 0.047, 0.533, 0.066, 1
                button_radius: dp(12)
                on_release: root.go_to_listar_funcionarios()

            CustomStyledButton:
                text: 'LISTAR PRATOS'
                button_bg_color: 0.101, 0.513, 0.917, 1
                button_radius: dp(12)
                on_release: root.go_to_listar_pratos()

            CustomStyledButton:
                text: 'VERSÃO WEB'
                button_bg_color: 0.721, 0.525, 0.043, 1
                button_radius: dp(12)
                on_release: root.abrir_dashboard()

            CustomStyledButton:
                text: 'VOLTAR'
                button_bg_color: 0.309, 0.309, 0.309, 1
                button_radius: dp(12)
                on_release: root.go_to_back_gestao()
'''

Builder.load_string(KV_CONTENT)

class TelaMenuGestao(MDScreen):
    _streamlit_process = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def go_to_listar_funcionarios(self):
        self.manager.current = 'listar_funcionarios'

    def go_to_listar_pratos(self):
        self.manager.current = 'listar_pratos'

    def go_to_back_gestao(self):
        self.manager.current = 'tela_gestao'

    def iniciar_dashboard(self):
        if TelaMenuGestao._streamlit_process and TelaMenuGestao._streamlit_process.poll() is None:
            print("Streamlit já está rodando.")
            return

        url_dashboard = "http://localhost:8501"
        dashboard_script_path = os.path.join(os.path.dirname(__file__), 'dashboard.py')

        print(f"Tentando iniciar Streamlit para {dashboard_script_path}...")
        try:
            TelaMenuGestao._streamlit_process = subprocess.Popen(
                [sys.executable, "-m", "streamlit", "run", dashboard_script_path],
                creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0
            )
            print(f"Processo Streamlit iniciado (PID: {TelaMenuGestao._streamlit_process.pid})")
        except Exception as e:
            print(f"Erro ao iniciar o Streamlit: {e}")
            TelaMenuGestao._streamlit_process = None

    def encerrar_dashboard(self):
        if TelaMenuGestao._streamlit_process and TelaMenuGestao._streamlit_process.poll() is None:
            print("Encerrando processo Streamlit...")
            try:
                TelaMenuGestao._streamlit_process.terminate()
                TelaMenuGestao._streamlit_process.wait(timeout=5)
                if TelaMenuGestao._streamlit_process.poll() is None:
                    TelaMenuGestao._streamlit_process.kill()
                print("Processo Streamlit encerrado.")
            except Exception as e:
                print(f"Erro ao encerrar Streamlit: {e}")
            TelaMenuGestao._streamlit_process = None
        else:
            print("Streamlit não está rodando ou já foi encerrado.")

    def abrir_dashboard(self):
        self.iniciar_dashboard()
        url_dashboard = "http://localhost:8501"
        try:
            webbrowser.open(url_dashboard)
            print(f"Abrindo dashboard no navegador: {url_dashboard}")
        except Exception as e:
            print(f"Erro ao abrir o dashboard no navegador: {e}")

from kivymd.app import MDApp
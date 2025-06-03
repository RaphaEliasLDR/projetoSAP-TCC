# screens/telaCozinha.py

from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout # Usado para centralizar o texto
from kivy.metrics import dp # Para padding e espaçamento
from kivy.utils import get_color_from_hex # Para cores de texto
from kivymd.app import MDApp # Para acessar o usuário logado

KV_CONTENT = '''
#:import dp kivy.metrics.dp
#:import get_color_from_hex kivy.utils.get_color_from_hex

<TelaCozinha>: # O nome da classe DEVE SER TelaCozinha
    name: 'tela_cozinha' # O nome da tela no ScreenManager
    md_bg_color: 0.1, 0.1, 0.1, 1 # Fundo escuro simples

    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(30)
        spacing: dp(25)
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        size_hint_y: None
        height: self.minimum_height

        MDLabel:
            text: "LOGIN REALIZADO COM SUCESSO!"
            font_name: "MontserratBold"
            font_size: "28sp"
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1]
            color: get_color_from_hex("#4CAF50") # Verde

        MDLabel:
            id: logged_in_user_label
            text: "Bem-vindo, Cozinheiro!" # Será atualizado dinamicamente
            font_name: "MontserratBold"
            font_size: "18sp"
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1]
            color: 1, 1, 1, 1
'''

Builder.load_string(KV_CONTENT)

class TelaCozinha(MDScreen):
    def on_enter(self, *args):
        # Atualiza a mensagem de boas-vindas com o nome do usuário logado
        app = MDApp.get_running_app()
        if app.logged_in_user:
            self.ids.logged_in_user_label.text = f"Bem-vindo, {app.logged_in_user['nome']}!"
        else:
            self.ids.logged_in_user_label.text = "Usuário não logado."
# screens/telaMenu.py

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.button import Button
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout

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

<TelaMenu>:
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
            size_hint_y: 0.5
            spacing: dp(20)
            padding: dp(20)

            CustomStyledButton:
                text: 'STATUS'
                button_bg_color: 0.047, 0.533, 0.066, 1
                button_radius: dp(12)
                on_release: root.go_to_status()

            CustomStyledButton:
                text: 'HISTÓRICO'
                button_bg_color: 0.101, 0.513, 0.917, 1
                button_radius: dp(12)
                on_release: root.go_to_historico()

            CustomStyledButton:
                text: 'AVALIAÇÃO'
                button_bg_color: 0.309, 0.309, 0.309, 1
                button_radius: dp(12)
                on_release: root.go_to_avaliacao()

            CustomStyledButton:
                text: 'VOLTAR'
                button_bg_color: 0.721, 0.525, 0.043, 1
                button_radius: dp(12)
                on_release: root.go_back()
'''

Builder.load_string(KV_CONTENT)

class TelaMenu(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def go_back(self):
        self.manager.current = 'tela_pedido'  # Volta para a tela inicial

    def go_to_status(self):
        self.manager.current = 'tela_gestao' 

    def go_to_status(self):
        print("Indo para a tela de STATUS")
        # Implemente a lógica para ir para a tela de STATUS
        # Exemplo: self.manager.current = 'tela_status'
        pass

    def go_to_historico(self):
        print("Indo para a tela de HISTÓRICO")
        # Implemente a lógica para ir para a tela de HISTÓRICO
        # Exemplo: self.manager.current = 'tela_historico'
        pass

    def go_to_avaliacao(self):
        print("Indo para a tela de AVALIAÇÃO")
        # Implemente a lógica para ir para a tela de AVALIAÇÃO
        # Exemplo: self.manager.current = 'tela_avaliacao'
        pass

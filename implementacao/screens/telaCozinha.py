# screens/telaCozinha.py

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import ObjectProperty

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.card import MDCard

Window.size = (360, 800)

KV = '''
#:import dp kivy.metrics.dp
#:import get_color_from_hex kivy.utils.get_color_from_hex

<TelaCozinha>:
    name: 'tela_cozinha'
    md_bg_color: 0.1, 0.1, 0.1, 1

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
            color: get_color_from_hex("#4CAF50")

        MDLabel:
            id: logged_in_user_label
            text: "Bem-vindo, Cozinheiro!"
            font_name: "MontserratBold"
            font_size: "18sp"
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1]
            color: 1, 1, 1, 1

        MDBoxLayout:
            id: pedidos_layout
            orientation: 'vertical'
            spacing: dp(10)
            size_hint_y: None
            height: self.minimum_height
'''

Builder.load_string(KV)

class TelaCozinha(MDScreen):
    pedidos_layout = ObjectProperty(None)

    def on_kv_post(self, base_widget):
        self.pedidos_layout = self.ids.pedidos_layout

    def on_enter(self, *args):
        app = MDApp.get_running_app()
        if app.logged_in_user:
            self.ids.logged_in_user_label.text = f"Bem-vindo, {app.logged_in_user['nome']}!"
        else:
            self.ids.logged_in_user_label.text = "Usuário não logado."

        pedidos_teste = [
            {'mesa': '1', 'status': 'Preparando', 'itens': {'Pizza': 2, 'Refrigerante': 1}, 'observacao': 'Sem cebola'},
            {'mesa': '2', 'status': 'Pendente', 'itens': {'Hambúrguer': 1}, 'observacao': ''},
        ]
        self.atualizar_pedidos(pedidos_teste)

    def go_back(self):
        self.manager.current = 'tela_inicial'

    def atualizar_pedidos(self, pedidos):
        self.pedidos_layout.clear_widgets()
        for pedido in pedidos:
            lbl_status = MDLabel(
                text=f"Status: [b]{pedido['status']}[/b]",
                markup=True,
                text_color=get_color_from_hex("#FFEB3B"),
                halign="center"
            )
            self.pedidos_layout.add_widget(lbl_status)

            botoes_layout = MDBoxLayout(spacing=dp(10))
            btn_preparando = MDRaisedButton(
                text="Preparando",
                md_bg_color=get_color_from_hex("#FFA000"),
                on_release=lambda x, p=pedido, l=lbl_status, b=botoes_layout: self.marcar_preparando(p, l, x, b)
            )
            btn_pronto = MDRaisedButton(
                text="Pronto",
                md_bg_color=get_color_from_hex("#4CAF50"),
                on_release=lambda x, p=pedido, l=lbl_status, b=botoes_layout: self.marcar_pronto(p, l, b)
            )
            botoes_layout.add_widget(btn_preparando)
            botoes_layout.add_widget(btn_pronto)
            self.pedidos_layout.add_widget(botoes_layout)

    def marcar_preparando(self, pedido, lbl_status, btn_preparando, botoes_layout):
        pedido['status'] = 'Preparando'
        lbl_status.text = f"Status: [b]{pedido['status']}[/b]"
        lbl_status.text_color = get_color_from_hex("#FFEB3B")
        self.piscar_status(lbl_status, get_color_from_hex("#FFEB3B"))

    def marcar_pronto(self, pedido, lbl_status, botoes_layout):
        pedido['status'] = 'Pronto'
        lbl_status.text = f"Status: [b]{pedido['status']}[/b]"
        lbl_status.text_color = get_color_from_hex("#4CAF50")
        botoes_layout.clear_widgets()

        btn_detalhes = MDRaisedButton(
            text="Ver Detalhes",
            md_bg_color=get_color_from_hex("#1565C0")
        )
        botoes_layout.add_widget(btn_detalhes)

        self.piscar_status(lbl_status, get_color_from_hex("#4CAF50"))

        tela_status = self.manager.get_screen('tela_status')
        pedidos_prontos = [pedido]
        tela_status.atualizar_pedidos(pedidos_prontos)

    def piscar_status(self, lbl_status, cor_destino):
        original_color = lbl_status.text_color

        def alternar_cor(dt):
            lbl_status.text_color = original_color if lbl_status.text_color == cor_destino else cor_destino

        Clock.schedule_interval(alternar_cor, 0.5)
        Clock.schedule_once(lambda dt: Clock.unschedule(alternar_cor), 3)

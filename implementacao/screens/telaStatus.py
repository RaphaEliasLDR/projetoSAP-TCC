from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivy.properties import ObjectProperty

KV = '''
<TelaStatus>:
    name: 'tela_status'
    md_bg_color: 0.1, 0.1, 0.1, 1

    BoxLayout:
        orientation: 'vertical'
        padding: dp(10)
        spacing: dp(10)

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(40)
            spacing: dp(10)

            MDIconButton:
                icon: "arrow-left"
                user_font_size: "24sp"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                size_hint: None, None
                size: dp(35), dp(35)
                on_release: root.go_back()

            MDLabel:
                text: "Pedidos Confirmados"
                font_name: "MontserratBold"
                font_size: "18sp"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                halign: "center"
                valign: "middle"

        ScrollView:
            do_scroll_x: False

            BoxLayout:
                id: pedidos_layout
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(10)

'''

Builder.load_string(KV)

class TelaStatus(MDScreen):
    pedidos_layout = ObjectProperty(None)
    dialog = None  # Referência para o dialog

    def on_kv_post(self, base_widget):
        self.pedidos_layout = self.ids.pedidos_layout

    def go_back(self):
        self.manager.current = 'tela_pedido'

    def atualizar_pedidos(self, pedidos):
        self.pedidos_layout.clear_widgets()

        for pedido in pedidos:
            card = self.criar_card_pedido(pedido)
            self.pedidos_layout.add_widget(card)

    def criar_card_pedido(self, pedido):
        card = MDCard(
            orientation='vertical',
            padding=dp(10),
            spacing=dp(10),
            size_hint_y=None,
            height=dp(150),
            md_bg_color=get_color_from_hex("#DDDDDD"),
            radius=[10, 10, 10, 10],
            elevation=4
        )

        lbl_mesa = MDLabel(
            text=f"Mesa: [b]{pedido['mesa']}[/b]",
            markup=True,
            font_name="MontserratBold",
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=dp(25),
            halign="center",
            valign="middle"
        )

        itens_texto = "\n".join([f"{item} x{quant}" for item, quant in pedido['itens'].items()])
        lbl_itens = MDLabel(
            text=f"Itens:\n{itens_texto}",
            font_name="MontserratBold",
            color = (0, 0, 0, 1),
            size_hint_y=None,
            height=dp(60),
            halign="center",
            valign="middle"
        )

        botoes_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40),
            spacing=dp(10)
        )

        # Botão "Ver Detalhes"
        btn_detalhes = MDRaisedButton(
            text="Ver Detalhes",
            md_bg_color=get_color_from_hex("#1565C0"),
            on_release=lambda x: self.ver_detalhes(pedido)
        )

        # Botão "Entregar"
        btn_entregar = MDRaisedButton(
            text_color = (0, 0, 0, 1),
            text="Entregar",
            md_bg_color=get_color_from_hex("#4CAF50"),
        )
        # Se pedido já estiver entregue, atualizar botão e desabilitar
        if pedido.get('entregue', False):
            btn_entregar.text = "Entregue"
            btn_entregar.md_bg_color = get_color_from_hex("#D32F2F")
            btn_entregar.disabled = True

        def marcar_como_entregue(button):
            button.text = "Entregue"
            button.text_color = (0, 0, 0, 1) 
            button.disabled = True
            pedido['entregue'] = True

        btn_entregar.bind(on_release=lambda x: marcar_como_entregue(btn_entregar))

        botoes_layout.add_widget(btn_detalhes)
        botoes_layout.add_widget(btn_entregar)

        card.add_widget(lbl_mesa)
        card.add_widget(lbl_itens)
        card.add_widget(botoes_layout)

        return card

    def ver_detalhes(self, pedido):
        itens_texto = "\n".join([f"{item} x{quant}" for item, quant in pedido['itens'].items()])
        observacao = pedido['observacao'] or "Nenhuma"

    # Criar layout com scroll
        content_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=dp(10),
            spacing=dp(10)
        )

        content_layout.bind(minimum_height=content_layout.setter('height'))

        lbl_obs = MDLabel(
            text=f"[b]Observação:[/b] {observacao}",
            markup=True,
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            size_hint_y=None,
            height=dp(40)
        )

        lbl_itens = MDLabel(
            text=f"[b]Itens:[/b]\n{itens_texto}",
            markup=True,
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            size_hint_y=None,
            height=max(dp(100), dp(20) * len(pedido['itens']))
        )

        content_layout.add_widget(lbl_obs)
        content_layout.add_widget(lbl_itens)

        scroll = ScrollView(size_hint=(1, None), size=(dp(300), dp(250)))
        scroll.add_widget(content_layout)

        if self.dialog:
            self.dialog.dismiss()

        self.dialog = MDDialog(
            title=f"Detalhes da Mesa {pedido['mesa']}",
            type="custom",
            content_cls=scroll,
            buttons=[
                MDFlatButton(
                    text="FECHAR",
                    text_color=(0, 0, 0, 1),
                    on_release=lambda x: self.dialog.dismiss()
                ),
            ]
        )
        self.dialog.open()

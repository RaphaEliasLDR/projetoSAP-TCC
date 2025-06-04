from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView

KV_STATUS = '''
<TelaStatus>:
    name: 'tela_status'
    md_bg_color: 0.1, 0.1, 0.1, 1  # Cor de fundo

    BoxLayout:
        orientation: 'vertical'
        padding: dp(10)
        spacing: dp(10)
        
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(50)
            spacing: dp(10)

            MDIconButton:  
                text: ""
                icon: "arrow-left"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                size_hint: None, None
                size: dp(40), dp(40)
                on_release: root.go_back()

            Widget:

            BoxLayout:
                orientation: 'horizontal'
                size_hint_x: None
                width: dp(135)
                pos_hint: {"center_x": 0.5}
                Image:
                    source: 'assets/logoSAP3.png'
                    size_hint_x: None
                    width: dp(135)
                    fit_mode: 'contain'

            Widget:

        ScrollView:
            do_scroll_x: False

            BoxLayout:
                id: pedidos_prontos_layout
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(10)
'''


Builder.load_string(KV_STATUS)

class TelaStatus(MDScreen):
    def on_kv_post(self, base_widget):
        self.pedidos_prontos_layout = self.ids.pedidos_prontos_layout
        self.carregar_status()

    def go_back(self):
        # Código para voltar à tela anterior
        self.manager.current = 'tela_pedido'

    def carregar_status(self):
        pedidos = [
            {"mesa": 5, "status": "Pendente", "itens": {"Pizza": 2, "Refrigerante": 1}},
            {"mesa": 3, "status": "Preparando", "itens": {"Hamburguer": 1, "Batata Frita": 1}},
            {"mesa": 2, "status": "Pronto", "itens": {"Espaguete": 1}},
        ]
        self.atualizar_pedidos(pedidos)

    def atualizar_pedidos(self, pedidos):
        self.pedidos_prontos_layout.clear_widgets()

        if not pedidos:
            lbl_vazio = MDLabel(
                text="Nenhum pedido no momento.",
                halign="center",
                theme_text_color="Hint",
                size_hint_y=None,
                height=dp(40)
            )
            self.pedidos_prontos_layout.add_widget(lbl_vazio)
            return

        for pedido in pedidos:
            card = self.criar_card_pedido_pronto(pedido)
            self.pedidos_prontos_layout.add_widget(card)

    def criar_card_pedido_pronto(self, pedido):
        # Card com fundo branco
        card = MDCard(
            orientation='vertical',
            padding=dp(10),
            spacing=dp(8),
            size_hint_y=None,
            height=dp(200),  # Card maior
            md_bg_color=get_color_from_hex("#FFFFFF"),  # Cor de fundo branca
            radius=[8, 8, 8, 8],  # Bordas suaves
            elevation=8  # Elevation para destacar
        )

        content_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(180),  # Altura ajustada
            spacing=dp(10),
            padding=dp(10),
            pos_hint={'center_x': 0.5}
        )

        # Label "Mesa" (sem mudança de cor)
        lbl_mesa = MDLabel(
            text=f"Mesa: [b]{pedido.get('mesa', '?')}[/b]",
            markup=True,
            font_style="Body1",  # Fonte menor
            theme_text_color="Primary",  # Mantém a cor primária para o título
            size_hint_y=None,
            height=dp(30),  # Altura do label
            halign="center"
        )

        # Status do pedido
        status = pedido.get('status', 'Pendente')
        color_map = {
            'Pendente': "#F44336",  # Vermelho
            'Preparando': "#FF9800",  # Laranja
            'Pronto': "#4CAF50",  # Verde
            'Entregue': "#D32F2F"  # Vermelho para entregue
        }
        lbl_status = MDLabel(
            text=f"Status: [b]{status}[/b]",
            markup=True,
            theme_text_color="Custom",
            text_color=get_color_from_hex(color_map.get(status, "#388E3C")),
            font_style="Body2",  # Fonte menor
            size_hint_y=None,
            height=dp(20),
            halign="center"
        )

        # Itens do pedido
        itens = pedido.get('itens', {})
        texto_itens = "\n".join([f"{item} x{quant}" for item, quant in itens.items()])

        lbl_itens = MDLabel(
            text=f"Itens:\n{texto_itens}",
            size_hint_y=None,
            height=max(dp(50), dp(18) * len(itens)),
            halign="center",
            theme_text_color="Secondary",
            font_style="Body2"
        )

        # Layout para os botões
        botoes_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(30),
            spacing=dp(6),
            pos_hint={'center_x': 0.5}
        )

        # Botões
        btn_detalhes = MDRaisedButton(
            text="Ver Detalhes",
            md_bg_color=get_color_from_hex("#1565C0"),
            on_release=lambda x: self.ver_detalhes(pedido)
        )
        botoes_layout.add_widget(btn_detalhes)

        btn_entregar = MDRaisedButton(
            text="Entregar",
            md_bg_color=get_color_from_hex("#4CAF50"),
            on_release=lambda x: self.marcar_entregue(pedido, card, btn_entregar)
        )
        # Exibir botão "Entregar" apenas para pedidos com status "Pronto"
        if pedido['status'] != "Pronto":
            btn_entregar.disabled = True
            btn_entregar.md_bg_color = get_color_from_hex("#BDBDBD")  # Cor do botão desabilitado
        botoes_layout.add_widget(btn_entregar)

        content_layout.add_widget(lbl_mesa)
        content_layout.add_widget(lbl_status)
        content_layout.add_widget(lbl_itens)
        content_layout.add_widget(botoes_layout)

        card.add_widget(content_layout)

        return card

    def ver_detalhes(self, pedido):
        itens_texto = "\n".join([f"{item} x{quant}" for item, quant in pedido['itens'].items()])
        observacao = pedido.get('observacao', "Nenhuma")

        content_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=dp(8),
            spacing=dp(8)
        )
        content_layout.bind(minimum_height=content_layout.setter('height'))

        lbl_obs = MDLabel(
            text=f"[b]Observação:[/b] {observacao}",
            markup=True,
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            size_hint_y=None,
            height=dp(30),
            font_style="Body1"
        )

        lbl_itens = MDLabel(
            text=f"[b]Itens:[/b]\n{itens_texto}",
            markup=True,
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            size_hint_y=None,
            height=max(dp(90), dp(18) * len(pedido['itens'])),
            font_style="Body2"
        )

        content_layout.add_widget(lbl_obs)
        content_layout.add_widget(lbl_itens)

        scroll = ScrollView(size_hint=(1, None), size=(dp(300), dp(250)))
        scroll.add_widget(content_layout)

        dialog = MDDialog(
            title=f"Detalhes da Mesa {pedido['mesa']}",
            type="custom",
            content_cls=scroll,
            buttons=[MDFlatButton(
                    text="FECHAR",
                    text_color=(0, 0, 0, 1),
                    on_release=lambda x: dialog.dismiss()
                ),
            ]
        )
        dialog.open()

    def marcar_entregue(self, pedido, card, btn_entregar):
        # Atualiza status e UI
        pedido['status'] = 'Entregue'

        for widget in card.children:
            if isinstance(widget, BoxLayout):
                for label in widget.children:
                    if isinstance(label, MDLabel) and label.text.startswith("Status:"):
                        label.text = f"Status: [b]{pedido['status']}[/b]"
                        label.text_color = get_color_from_hex("#D32F2F")  # Cor de "Entregue"

        btn_entregar.text = "Entregue"
        btn_entregar.disabled = True
        btn_entregar.md_bg_color = get_color_from_hex("#BDBDBD")  # Cor do botão desabilitado

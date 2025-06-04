# screens/telaStatus.py
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
    md_bg_color: 0.95, 0.95, 0.95, 1

    BoxLayout:
        orientation: 'vertical'
        padding: dp(10)
        spacing: dp(10)

        MDLabel:
            text: "Pedidos"
            font_style: "H5"
            size_hint_y: None
            height: dp(40)
            halign: "center"
            theme_text_color: "Primary"

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
        self.simular_pedidos()

    def simular_pedidos(self):
        # Simulando alguns pedidos para teste
        pedidos_prontos = [
            {'mesa': 1, 'status': 'Pronto', 'itens': {'Hambúrguer': 2, 'Batata Frita': 1}},
            {'mesa': 2, 'status': 'Pronto', 'itens': {'Pizza': 1, 'Refrigerante': 2}},
            {'mesa': 3, 'status': 'Pronto', 'itens': {'Espaguete': 1, 'Salada': 1}},
        ]
        self.atualizar_pedidos(pedidos_prontos)

    def atualizar_pedidos(self, pedidos_prontos):
        # Limpa a lista de pedidos
        self.pedidos_prontos_layout.clear_widgets()

        if not pedidos_prontos:
            lbl_vazio = MDLabel(
                text="Nenhum pedido pronto no momento.",
                halign="center",
                theme_text_color="Hint",
                size_hint_y=None,
                height=dp(40)
            )
            self.pedidos_prontos_layout.add_widget(lbl_vazio)
            return

        for pedido in pedidos_prontos:
            card = self.criar_card_pedido_pronto(pedido)
            self.pedidos_prontos_layout.add_widget(card)

    def criar_card_pedido_pronto(self, pedido):
        # Ajustando o card para um tamanho maior e uma cor bege puxando para o branco
        card = MDCard(
            orientation='vertical',
            padding=dp(10),
            spacing=dp(8),
            size_hint_y=None,
            height=dp(200),  # Card maior
            md_bg_color=get_color_from_hex("#FAF3E0"),  # Cor de fundo bege claro
            radius=[8, 8, 8, 8],  # Bordas suaves
            elevation=8  # Elevation para manter um destaque sutil
        )

        # Centralizando e ajustando o conteúdo dentro do card
        content_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(180),  # Ajustando a altura do conteúdo dentro do card
            spacing=dp(10),
            padding=dp(10),
            pos_hint={'center_x': 0.5}
        )

        # Ajuste para o label "Mesa" com fonte menor
        lbl_mesa = MDLabel(
            text=f"Mesa: [b]{pedido.get('mesa', '?')}[/b]",
            markup=True,
            font_style="Body1",  # Fonte menor
            theme_text_color="Primary",
            size_hint_y=None,
            height=dp(30),  # Altura do label menor
            halign="center"
        )

        # Status do pedido com fonte menor
        lbl_status = MDLabel(
            text=f"Status: [b]{pedido.get('status', 'Pronto')}[/b]",
            markup=True,
            theme_text_color="Custom",
            text_color=get_color_from_hex("#388E3C"),  # Cor do status (verde escuro)
            font_style="Body2",  # Fonte menor
            size_hint_y=None,
            height=dp(20),  # Altura do label do status menor
            halign="center"
        )

        # Itens do pedido
        itens = pedido.get('itens', {})
        texto_itens = "\n".join([f"{item} x{quant}" for item, quant in itens.items()])

        lbl_itens = MDLabel(
            text=f"Itens:\n{texto_itens}",
            size_hint_y=None,
            height=max(dp(50), dp(18) * len(itens)),  # Altura ajustada para os itens
            halign="center",
            theme_text_color="Secondary",
            font_style="Body2"  # Fonte menor
        )

        # Layout para os botões
        botoes_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(30),
            spacing=dp(6),
            pos_hint={'center_x': 0.5}
        )

        # Botão "Ver Detalhes"
        btn_detalhes = MDRaisedButton(
            text="Ver Detalhes",
            md_bg_color=get_color_from_hex("#1565C0"),  # Cor de destaque azul
            on_release=lambda x: self.ver_detalhes(pedido)
        )
        botoes_layout.add_widget(btn_detalhes)

        # Botão "Entregar"
        btn_entregar = MDRaisedButton(
            text="Entregar",
            md_bg_color=get_color_from_hex("#4CAF50"),  # Cor do botão verde
            on_release=lambda x: self.marcar_entregue(pedido, card, btn_entregar)
        )
        botoes_layout.add_widget(btn_entregar)

        # Adicionando widgets ao layout do card
        content_layout.add_widget(lbl_mesa)
        content_layout.add_widget(lbl_status)
        content_layout.add_widget(lbl_itens)
        content_layout.add_widget(botoes_layout)

        # Adiciona o layout de conteúdo no card
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
            font_style="Body1"  # Fonte ajustada
        )

        lbl_itens = MDLabel(
            text=f"[b]Itens:[/b]\n{itens_texto}",
            markup=True,
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            size_hint_y=None,
            height=max(dp(90), dp(18) * len(pedido['itens'])),
            font_style="Body2"  # Fonte ajustada
        )

        content_layout.add_widget(lbl_obs)
        content_layout.add_widget(lbl_itens)

        scroll = ScrollView(size_hint=(1, None), size=(dp(300), dp(250)))
        scroll.add_widget(content_layout)

        dialog = MDDialog(
            title=f"Detalhes da Mesa {pedido['mesa']}",
            type="custom",
            content_cls=scroll,
            buttons=[
                MDFlatButton(
                    text="FECHAR",
                    text_color=(0, 0, 0, 1),
                    on_release=lambda x: dialog.dismiss()
                ),
            ]
        )
        dialog.open()

    def marcar_entregue(self, pedido, card, btn_entregar):
        # Atualiza o status do pedido para "Entregue" e muda o texto no card
        pedido['status'] = 'Entregue'

        # Altera o status no card (não alterando a cor)
        for widget in card.children:
            if isinstance(widget, BoxLayout):
                for label in widget.children:
                    if isinstance(label, MDLabel) and label.text.startswith("Status:"):
                        label.text = f"Status: [b]{pedido['status']}[/b]"
                        label.text_color = get_color_from_hex("#D32F2F")  # Cor de "Entregue" (vermelho)

        # Desabilita o botão "Entregar", muda o texto e a cor
        btn_entregar.text = "Entregue"
        btn_entregar.disabled = True
        btn_entregar.md_bg_color = get_color_from_hex("#BDBDBD")  # Cor do botão desabilitado

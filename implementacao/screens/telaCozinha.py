from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.properties import ObjectProperty
from kivy.clock import Clock
Window.size = (360, 800)
KV = '''
<TelaCozinha>:
    name: 'tela_cozinha'
    md_bg_color: 0.1, 0.1, 0.1, 1

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
                icon: "arrow-left"
                user_font_size: "24sp"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1
                size_hint: None, None
                size: dp(40), dp(40)
                on_release: root.go_back()

            BoxLayout:
                Widget:
                Image:
                    source: 'assets/logoSAP3.png'
                    size_hint_x: None
                    width: dp(135)
                    fit_mode: 'contain'
                Widget:

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

class TelaCozinha(MDScreen):
    pedidos_layout = ObjectProperty(None)
    dialog = None

    def on_kv_post(self, base_widget):
        self.pedidos_layout = self.ids.pedidos_layout

    def go_back(self):
        self.manager.current = 'tela_inicial'

    def atualizar_pedidos(self, pedidos):
        ordem_status = {'Pendente': 0, 'Preparando': 1, 'Pronto': 2}
        pedidos_ordenados = sorted(pedidos, key=lambda p: ordem_status.get(p.get('status', 'Pendente'), 0))

        self.pedidos_layout.clear_widgets()

        for pedido in pedidos_ordenados:
            pedido.setdefault('status', 'Pendente')
            card = self.criar_card_pedido(pedido)
            self.pedidos_layout.add_widget(card)

    def criar_card_pedido(self, pedido):
        card = MDCard(
            orientation='vertical',
            padding=dp(10),
            spacing=dp(8),
            size_hint_y=None,
            height=dp(200),
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
            height=dp(30),
            halign="center",
            valign="middle"
        )

        status = pedido.get('status', 'Pendente')
        color_map = {
            'Pendente': (1, 0, 0, 1),
            'Preparando': (1, 0.8, 0, 1),
            'Pronto': (0, 0.7, 0, 1)
        }
        status_color = color_map.get(status, (0, 0, 0, 1))

        lbl_status = MDLabel(
            text=f"Status: [b]{status}[/b]",
            markup=True,
            theme_text_color="Custom",
            text_color=status_color,
            size_hint_y=None,
            height=dp(30),
            halign="center",
            valign="middle"
        )

        itens = pedido.get('itens', {})
        itens_lista = list(itens.items())
        itens_exibidos = itens_lista[:2]
        texto_itens = "\n".join([f"{item} x{quant}" for item, quant in itens_exibidos])
        if len(itens_lista) > 2:
            texto_itens += f"\n... e mais {len(itens_lista) - 2} itens"

        lbl_itens = MDLabel(
            text=f"Itens:\n{texto_itens}",
            font_name="MontserratBold",
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=dp(50),
            halign="center",
            valign="top"
        )

        botoes_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(40),
            spacing=dp(10)
        )

        btn_detalhes = MDRaisedButton(
            text="Ver Detalhes",
            md_bg_color=get_color_from_hex("#1565C0"),
            on_release=lambda x: self.ver_detalhes(pedido, lbl_status)
        )
        botoes_layout.add_widget(btn_detalhes)

        if status == 'Pendente':
            btn_preparando = MDRaisedButton(
                text="Preparando",
                md_bg_color=get_color_from_hex("#FFEB3B"),
                on_release=lambda x: self.marcar_preparando(pedido, lbl_status, btn_preparando, botoes_layout)
            )
            botoes_layout.add_widget(btn_preparando)

        if status == 'Preparando':
            btn_pronto = MDRaisedButton(
                text="Pronto",
                md_bg_color=get_color_from_hex("#4CAF50"),
                on_release=lambda x: self.marcar_pronto(pedido, lbl_status, botoes_layout)
            )
            botoes_layout.add_widget(btn_pronto)

        card.add_widget(lbl_mesa)
        card.add_widget(lbl_status)
        card.add_widget(lbl_itens)
        card.add_widget(botoes_layout)

        return card

    def ver_detalhes(self, pedido, lbl_status):
        itens_texto = "\n".join([f"{item} x{quant}" for item, quant in pedido['itens'].items()])
        observacao = pedido.get('observacao', "Nenhuma")

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

    def marcar_preparando(self, pedido, lbl_status, btn_preparando, botoes_layout):
        pedido['status'] = 'Preparando'
        lbl_status.text = f"Status: [b]{pedido['status']}[/b]"
        lbl_status.text_color = get_color_from_hex("#FFEB3B")
        btn_preparando.disabled = True
        botoes_layout.clear_widgets()

        btn_detalhes = MDRaisedButton(
            text="Ver Detalhes",
            md_bg_color=get_color_from_hex("#1565C0"),
            on_release=lambda x: self.ver_detalhes(pedido, lbl_status)
        )
        botoes_layout.add_widget(btn_detalhes)

        btn_pronto = MDRaisedButton(
            text="Pronto",
            md_bg_color=get_color_from_hex("#4CAF50"),
            on_release=lambda x: self.marcar_pronto(pedido, lbl_status, botoes_layout)
        )
        botoes_layout.add_widget(btn_pronto)

        self.piscar_status(lbl_status, get_color_from_hex("#FFEB3B"))

    def marcar_pronto(self, pedido, lbl_status, botoes_layout):
        pedido['status'] = 'Pronto'
        lbl_status.text = f"Status: [b]{pedido['status']}[/b]"
        lbl_status.text_color = get_color_from_hex("#4CAF50")
        botoes_layout.clear_widgets()

        app = MDApp.get_running_app()
        pedidos_prontos = [p for p in app.pedidos if p.get("status") == "Pronto"]
        status_screen = self.manager.get_screen('tela_status')
        status_screen.atualizar_pedidos(pedidos_prontos)

        btn_detalhes = MDRaisedButton(
            text="Ver Detalhes",
            md_bg_color=get_color_from_hex("#1565C0"),
            on_release=lambda x: self.ver_detalhes(pedido, lbl_status)
        )
        botoes_layout.add_widget(btn_detalhes)

        self.piscar_status(lbl_status, get_color_from_hex("#4CAF50"))

    def piscar_status(self, lbl_status, cor_destino):
        original_color = lbl_status.text_color
        lbl_status.text_color = cor_destino
        def reset_color(dt):
            lbl_status.text_color = original_color
        Clock.schedule_once(reset_color, 0.7)

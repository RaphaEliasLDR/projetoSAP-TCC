# screens/telaPedidos.py

from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty
from kivy.utils import get_color_from_hex
from functools import partial
import json
import os

def carregar_pratos():
    caminho_arquivo = 'pratos.json'
    if not os.path.exists(caminho_arquivo):
        return []  # Se o arquivo não existe, retorna lista vazia
    
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        try:
            pratos = json.load(f)
            return pratos
        except json.JSONDecodeError:
            # Se o JSON estiver com erro, retorna vazio
            return []



class PedidoStyledButton(Button):
    button_bg_color = ListProperty([0, 0.5, 0, 1])
    button_radius = NumericProperty(dp(12))
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = [0, 0, 0, 0]
        self.color = [1, 1, 1, 1]
        self.font_name = "MontserratBold"

KV = '''
#:import dp kivy.metrics.dp
#:import get_color_from_hex kivy.utils.get_color_from_hex

<PedidoStyledButton>:
    canvas.before:
        Color:
            rgba: self.button_bg_color
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [self.button_radius]

<TelaPedidos>:
    name: 'tela_pedido'
    md_bg_color: 0.1, 0.1, 0.1, 1

    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(56)
            padding: dp(10)
            spacing: dp(10)
            canvas.before:
                Color:
                    rgba: 0.05, 0.05, 0.05, 1
                Rectangle:
                    pos: self.pos
                    size: self.size

            PedidoStyledButton:
                text: "SAIR"
                on_release: root.go_back_to_initial_screen()
                size_hint: None, None
                size: dp(50), dp(35)
                font_size: "14sp"
                button_bg_color: get_color_from_hex("#CF1919")
                button_radius: dp(5)

            BoxLayout:
                Widget:
                Image:
                    source: 'assets/logoSAP3.png'
                    size_hint_x: None
                    width: dp(135)
                    fit_mode: 'contain'
                Widget:

            PedidoStyledButton:
                text: "MENU"
                on_release: root.go_to_menu_screen()
                size_hint: None, None
                size: dp(50), dp(35)
                font_size: "14sp"
                button_bg_color: get_color_from_hex("#0C8811")
                button_radius: dp(5)

        BoxLayout:
            orientation: 'vertical'
            padding: dp(10)
            spacing: dp(10)

            Label:
                text: "Número da Mesa:"
                size_hint_y: None
                height: dp(30)
                font_name: "MontserratBold"
                color: 1,1,1,1

            TextInput:
                id: mesa_input
                hint_text: "Digite o número da mesa"
                size_hint_y: None
                height: dp(40)
                foreground_color: 1,1,1,1
                background_color: 0.2,0.2,0.2,1
                hint_text_color: 0.6,0.6,0.6,1

            Label:
                text: "Observação:"
                size_hint_y: None
                height: dp(30)
                font_name: "MontserratBold"
                color: 1,1,1,1

            TextInput:
                id: observacao_input
                hint_text: "Ex: Sem cebola"
                size_hint_y: None
                height: dp(40)
                foreground_color: 1,1,1,1
                background_color: 0.2,0.2,0.2,1
                hint_text_color: 0.6,0.6,0.6,1

            ScrollView:
                BoxLayout:
                    id: categorias_layout
                    orientation: 'vertical'
                    size_hint_y: None
                    height: self.minimum_height
                    spacing: dp(10)

            Label:
                text: "Itens Selecionados:"
                size_hint_y: None
                height: dp(30)
                font_name: "MontserratBold"
                color: 1,1,1,1

            ScrollView:
                BoxLayout:
                    id: lista_pedidos
                    orientation: 'vertical'
                    size_hint_y: None
                    height: self.minimum_height
                    spacing: dp(5)

            BoxLayout:
                size_hint_y: None
                height: dp(50)
                spacing: dp(10)

                PedidoStyledButton:
                    text: "CANCELAR"
                    button_bg_color: get_color_from_hex("#CF1919")
                    on_release: root.cancelar_pedido()
                    size_hint: None, None
                    size: dp(105), dp(40)
                    font_size: "14sp"
                    button_radius: dp(5)

                PedidoStyledButton:
                    text: "EDITAR"
                    button_bg_color: get_color_from_hex("#4F4F4F")
                    on_release: root.editar_pedido()
                    size_hint: None, None
                    size: dp(105), dp(40)
                    font_size: "14sp"
                    button_radius: dp(5)

                PedidoStyledButton:
                    text: "CONFIRMAR"
                    button_bg_color: get_color_from_hex("#2AB630")
                    on_release: root.confirmar_pedido()
                    size_hint: None, None
                    size: dp(105), dp(40)
                    font_size: "14sp"
                    button_radius: dp(5)
'''

Builder.load_string(KV)

class TelaPedidos(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.itens_selecionados = {}
        self.popup_edicao_ref = None
        self._items_list_layout_popup = None

    def on_kv_post(self, base_widget):
        self.mostrar_todas_categorias()

    def go_back_to_initial_screen(self):
        self.manager.current = 'tela_inicial'

    def go_to_menu_screen(self):
        self.manager.current = 'tela_menu'

    def mostrar_todas_categorias(self, *args):
        layout = self.ids.categorias_layout
        layout.clear_widgets()
        layout.bind(minimum_height=layout.setter('height'))

        pratos = carregar_pratos()  # Aqui você carrega seus pratos cadastrados
        categorias = {}

    # Agrupar pratos por categoria
        for prato in pratos:
            cat = prato.get('categoria', 'Outros')
            if cat not in categorias:
                categorias[cat] = []
            categorias[cat].append(prato)   

        for categoria, itens in categorias.items():
            layout.add_widget(Label(text=f"[b]{categoria}[/b]", markup=True, font_name="MontserratBold", color=(1,1,1,1), size_hint_y=None, height=dp(30)))
            for item in itens:
                box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(80), spacing=dp(10))
                box.add_widget(Image(source=item['imagem'], size_hint_x=None, width=dp(100), fit_mode='contain'))
                preco_formatado = f"R$ {float(item['preco']):.2f}".replace('.', ',')
                box.add_widget(Label(text=f"{item['nome']}\n{preco_formatado}",color=(1,1,1,1), font_name="MontserratBold", size_hint_x=0.7))

                btn = PedidoStyledButton(
                    text="ADICIONAR",
                    button_bg_color=get_color_from_hex("#2AB630"),
                    size_hint=(None, None),
                    size=(dp(85), dp(40)),
                    button_radius=dp(5),
                    font_size="12sp"
                )
                btn.bind(on_release=partial(self.adicionar_item, item['nome']))
                box.add_widget(btn)
                layout.add_widget(box)

    def adicionar_item(self, nome, *args):
        self.itens_selecionados[nome] = self.itens_selecionados.get(nome, 0) + 1
        self.atualizar_lista_pedidos()

    def atualizar_lista_pedidos(self):
        lista = self.ids.lista_pedidos
        lista.clear_widgets()
        lista.bind(minimum_height=lista.setter('height'))
        for nome, quantidade in self.itens_selecionados.items():
            lista.add_widget(Label(text=f"{nome} ({quantidade})",
                               font_name="MontserratBold",
                               color=(1,1,1,1),
                               size_hint_y=None,
                               height=dp(30)))
    def editar_pedido(self):
        self.mostrar_popup_edicao_pedido()

    def mostrar_popup_edicao_pedido(self):
        if self.popup_edicao_ref and self.popup_edicao_ref._is_open:
            self.popup_edicao_ref.dismiss()

        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        self._items_list_layout_popup = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(5))
        self._items_list_layout_popup.bind(minimum_height=self._items_list_layout_popup.setter('height'))

        scroll = ScrollView()
        scroll.add_widget(self._items_list_layout_popup)
        layout.add_widget(scroll)

        self._atualizar_conteudo_popup_edicao(self._items_list_layout_popup)

        btn_fechar = PedidoStyledButton(
            text="FECHAR",
            button_bg_color=get_color_from_hex("#CF1919"),
            size_hint=(None, None),
            size=(dp(100), dp(40)),
            font_size="14sp",
            button_radius=dp(5),
            pos_hint={"center_x": 0.5}
        )
        btn_fechar.bind(on_release=lambda x: self.popup_edicao_ref.dismiss())
        layout.add_widget(btn_fechar)

        self.popup_edicao_ref = Popup(
            title="Editar Pedido",
            content=layout,
            size_hint=(0.9, 0.8),
            title_color=get_color_from_hex("#FFFFFF"),
            separator_color=get_color_from_hex("#FFFFFF"),
            background_color=get_color_from_hex("#111213")
        )
        self.popup_edicao_ref.open()

    def _atualizar_conteudo_popup_edicao(self, layout):
        layout.clear_widgets()
        if not self.itens_selecionados:
            layout.add_widget(Label(text="Nenhum item para editar.", color=(1,1,1,1), font_name="MontserratBold", size_hint_y=None, height=dp(40)))
            return

        for nome, qtd in sorted(self.itens_selecionados.items()):
            linha = BoxLayout(orientation='horizontal', 
                            size_hint_y=None, 
                            height=dp(45),
                            spacing=dp(5),
                            padding=[dp(5), 0, dp(5), 0])
            
            lbl = Label(text=f"{nome} ({qtd})", 
                      font_name="MontserratBold", 
                      color=(1,1,1,1),
                      size_hint_x=0.7,
                      text_size=(None, None),
                      halign='left',
                      valign='middle',
                      shorten=True,
                      shorten_from='right')
            linha.add_widget(lbl)
            
            btn_menos = PedidoStyledButton(
                text="-", 
                button_bg_color=get_color_from_hex("#CF1919"), 
                size_hint=(None, None),
                size=(dp(30), dp(30)),
                font_size="20sp",
                button_radius=dp(5),
                padding=[dp(-1), dp(-1)]
            )
            btn_menos.bind(on_release=partial(self.decrementar_quantidade_item, nome))
            linha.add_widget(btn_menos)
            
            btn_mais = PedidoStyledButton(
                text="+", 
                button_bg_color=get_color_from_hex("#2AB630"), 
                size_hint=(None, None),
                size=(dp(30), dp(30)),
                font_size="20sp",
                button_radius=dp(5),
                padding=[dp(-2), dp(-2)]
            )
            btn_mais.bind(on_release=partial(self.incrementar_quantidade_item, nome))
            linha.add_widget(btn_mais)
            
            layout.add_widget(linha)

    def decrementar_quantidade_item(self, nome, *args):
        if nome in self.itens_selecionados:
            self.itens_selecionados[nome] -= 1
            if self.itens_selecionados[nome] <= 0:
                del self.itens_selecionados[nome]
        self.atualizar_lista_pedidos()
        self._atualizar_conteudo_popup_edicao(self._items_list_layout_popup)

    def incrementar_quantidade_item(self, nome, *args):
        self.itens_selecionados[nome] = self.itens_selecionados.get(nome, 0) + 1
        self.atualizar_lista_pedidos()
        self._atualizar_conteudo_popup_edicao(self._items_list_layout_popup)

    def cancelar_pedido(self):
        self.itens_selecionados.clear()
        self.ids.mesa_input.text = ""
        self.ids.observacao_input.text = ""
        self.atualizar_lista_pedidos()

    def confirmar_pedido(self):
        mesa = self.ids.mesa_input.text.strip()
        if not mesa or not self.itens_selecionados:
            self.mostrar_popup("Erro", "Mesa e itens são obrigatórios!")
            return
        self.mostrar_popup("Sucesso", "Pedido adicionado!")
        self.cancelar_pedido()

    def mostrar_popup(self, titulo, mensagem):
        # Layout principal
        main_layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(15))
        
        # Layout para a mensagem (centralizada)
        message_layout = BoxLayout(size_hint_y=0.7)
        lbl = Label(text=mensagem, 
                  font_name="MontserratBold", 
                  color=(1,1,1,1),
                  halign='center',
                  valign='middle')
        message_layout.add_widget(lbl)
        main_layout.add_widget(message_layout)
        
        # Layout para o botão (centralizado)
        button_layout = BoxLayout(size_hint_y=0.3, padding=(dp(20), 0, dp(20), 0))
        btn = PedidoStyledButton(
            text="FECHAR", 
            button_bg_color=get_color_from_hex("#CF1919"), 
            size_hint=(None, None),
            size=(dp(120), dp(40)), 
            font_size="14sp",
            button_radius=dp(5),
            pos_hint={'center_x': 0.5})
        btn.bind(on_release=lambda x: popup.dismiss())
        button_layout.add_widget(btn)
        main_layout.add_widget(button_layout)

        popup = Popup(
            title=titulo, 
            content=main_layout, 
            size_hint=(0.8, None), 
            height=dp(200),
            title_color=get_color_from_hex("#FFFFFF"),
            separator_color=get_color_from_hex("#FFFFFF"),
            background_color=get_color_from_hex("#111213"))
        popup.open()

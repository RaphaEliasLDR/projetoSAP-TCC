# Exemplo mínimo em screens/telaStatus.py
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from database import DatabaseManager

class TelaStatus(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = DatabaseManager()
        self.db.connect()
        self.carregar_pedidos()

    def carregar_pedidos(self):
        query = """
            SELECT p.id_pedido, m.numero_mesa, s.descricao 
            FROM pedido p
            JOIN mesa m ON p.mesa_id_mesa = m.id_mesa
            JOIN status_pedido s ON p.status_pedido_id_status_pedido = s.id_status_pedido
        """
        pedidos = self.db.execute_query(query)
        
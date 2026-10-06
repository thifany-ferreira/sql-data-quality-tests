-- Os mesmos dados com defeitos plantados. Cada defeito está marcado com o teste que precisa pegá-lo.

INSERT INTO clientes (id, nome, email, cidade, ativo) VALUES
(1, 'Ana Souza',   'ana@email.com',   'São Paulo', 1),
(2, 'Bruno Lima',  'bruno@email.com', 'Recife',    1),
(3, 'Carla Dias',  NULL,              'São Paulo', 1),  -- email_vazio
(4, 'Diego Alves', 'diego@email.com', 'Curitiba',  0),
(5, 'Elisa Rocha', 'ana@email.com',   'Salvador',  1),  -- email_duplicado
(6, 'Fábio Nunes', 'fabio.email.com', 'Natal',     1);  -- email_invalido

INSERT INTO produtos (id, nome, preco, estoque) VALUES
(1, 'Teclado',   150.00, 20),
(2, 'Mouse',      80.00,  0),
(3, 'Monitor',   900.00,  5),
(4, 'Cabo HDMI', -25.00, 50),  -- preco_negativo
(5, 'Headset',   300.00, -3);  -- estoque_negativo

INSERT INTO pedidos (id, cliente_id, produto_id, quantidade, data_pedido, status) VALUES
(1, 1, 1, 1, '2026-09-01', 'entregue'),
(2, 1, 3, 1, '2026-09-10', 'entregue'),
(3, 2, 2, 2, '2026-09-12', 'pendente'),
(4, 3, 5, 1, '2026-09-15', 'cancelado'),
(5, 9, 1, 1, '2026-09-20', 'pendente'),   -- pedido_sem_cliente
(6, 2, 4, 3, '2026-09-22', 'entregue'),
(7, 4, 3, 0, '2026-09-25', 'pendente'),   -- quantidade_invalida e pedido_de_cliente_inativo
(8, 1, 7, 1, '2026-09-26', 'entregue'),   -- pedido_sem_produto
(9, 2, 1, 1, '2026-09-27', 'enviadoo');   -- status_invalido

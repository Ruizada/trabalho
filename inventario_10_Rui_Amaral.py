# ==============================================================================
# TRABALHO PRÁTICO: Gestor de Inventário do Laboratório de Informática
# Formando: Rui Amaral | Número: 10
# Data: Outubro 2026
# ==============================================================================

# 1. ESTRUTURAS DE DADOS OBRIGATÓRIAS
SALAS = ('LAB1', 'LAB2', 'LAB3')
ESTADOS = ('operacional', 'avariado', 'em reparação')

tipos = ['computador', 'monitor', 'impressora', 'router', 'switch']

inventario = {
    'PC01': {
        'nome': 'desktop hp elitedesk',
        'tipo': 'computador',
        'sala': 'LAB1',
        'quantidade': 12,
        'estado': 'operacional',
    },
    'PC02': {
        'nome': 'desktop hp elitedeskHome',
        'tipo': 'computador',
        'sala': 'LAB2',
        'quantidade': 12,
        'estado': 'avariado',
    },
    'PC03': {
        'nome': 'desktop hp elitedeskPro',
        'tipo': 'computador',
        'sala': 'LAB3',
        'quantidade': 12,
        'estado': 'em reparação',
    },
    'MN01': {
        'nome': 'monitor dell 24',
        'tipo': 'monitor',
        'sala': 'LAB1',
        'quantidade': 10,
        'estado': 'operacional',
    },
    'IMP01': {
        'nome': 'impressora laser brother',
        'tipo': 'impressora',
        'sala': 'LAB3',
        'quantidade': 1,
        'estado': 'avariado',
    },
    'SW01': {
        'nome': 'switch cisco 24 portas',
        'tipo': 'switch',
        'sala': 'LAB2',
        'quantidade': 2,
        'estado': 'operacional',
    },
}

# Construção automática da lista de reparação no arranque
lista_reparacao = []
for codigo, info in inventario.items():
    if info['estado'] == 'avariado':
        lista_reparacao.append(codigo)

reparados = []
historico = []

# 2. CONSTRUÇÃO DO MENU PRINCIPAL (R0)
menu = "\nGESTOR DE INVENTÁRIO DO LABORATÓRIO\n"
menu += "1 - Listar equipamentos\n"
menu += "2 - Adicionar equipamento\n"
menu += "3 - Pesquisar equipamento\n"
menu += "4 - Alterar estado de um equipamento\n"
menu += "5 - Remover equipamento\n"
menu += "6 - Lista de reparação\n"
menu += "7 - Estatísticas\n"
menu += "8 - Histórico de operações\n"
menu += "0 - Sair\n"

# 3. CICLO PRINCIPAL DO PROGRAMA
ativo = True

while ativo:
    print(menu)
    opcao = input("Escolha uma opção: ").strip()

    # R1 - LISTAR EQUIPAMENTOS
    if opcao == '1':
        print("\n=== LISTA DE EQUIPAMENTOS ===")
        if not inventario:
            print("O inventário está vazio.")
        else:
            print("CÓDIGO | NOME | SALA | QUANTIDADE | ESTADO")
            for codigo in sorted(inventario.keys()):
                item = inventario[codigo]
                nome_formatado = item['nome'].title()
                print(f"{codigo} | {nome_formatado} | {item['sala']} | {item['quantidade']} un. | {item['estado']}")
            print(f"Total de registos: {len(inventario)}")

    # R2 - ADICIONAR EQUIPAMENTO
    elif opcao == '2':
        print("\n=== ADICIONAR EQUIPAMENTO ===")
        codigo = input("Código do equipamento: ").strip().upper()
        
        if codigo == "" or codigo in inventario:
            print("Erro: Código inválido ou já existente no inventário.")
        else:
            nome = ""
            while nome == "":
                nome = input("Nome/Descrição: ").strip()
                if nome == "":
                    print("O nome não pode ficar vazio!")

            print(f"Tipos aceites: {tipos}")
            tipo = input("Tipo: ").strip().lower()
            while tipo not in tipos:
                print(f"Tipo inválido! Escolha entre: {tipos}")
                tipo = input("Tipo: ").strip().lower()

            sala = input("Sala (LAB1, LAB2, LAB3): ").strip().upper()
            while sala not in SALAS:
                print(f"Sala inválida! Escolha entre: {SALAS}")
                sala = input("Sala: ").strip().upper()

            quantidade = 0
            valido = False
            while not valido:
                qtd_str = input("Quantidade: ").strip()
                if qtd_str.isdigit():
                    quantidade = int(qtd_str)
                    if quantidade > 0:
                        valido = True
                    else:
                        print("A quantidade deve ser maior que zero!")
                else:
                    print("Introduza um número inteiro válido!")

            inventario[codigo] = {
                'nome': nome.lower(),
                'tipo': tipo,
                'sala': sala,
                'quantidade': quantidade,
                'estado': 'operacional'
            }
            
            msg = f"Adicionado equipamento {codigo} ({nome.title()})"
            historico.append(msg)
            print("Equipamento adicionado com sucesso!")

    # R3 - PESQUISAR EQUIPAMENTO
    elif opcao == '3':
        print("\n=== PESQUISAR EQUIPAMENTO ===")
        codigo = input("Introduza o código: ").strip().upper()
        equipamento = inventario.get(codigo)
        
        if equipamento is None:
            print("Equipamento não encontrado.")
        else:
            print(f"\nFICHA DO EQUIPAMENTO [{codigo}]")
            for chave, valor in equipamento.items():
                if chave == 'nome':
                    print(f"{chave.title()}: {valor.title()}")
                else:
                    print(f"{chave.title()}: {valor}")

    # R4 - ALTERAR ESTADO DE UM EQUIPAMENTO
    elif opcao == '4':
        print("\n=== ALTERAR ESTADO ===")
        codigo = input("Introduza o código do equipamento: ").strip().upper()
        
        if codigo not in inventario:
            print("Equipamento não encontrado.")
        else:
            estado_atual = inventario[codigo]['estado']
            print(f"Estado atual: {estado_atual}")
            print(f"Estados possíveis: {ESTADOS}")
            
            novo_estado = input("Novo estado: ").strip().lower()
            while novo_estado not in ESTADOS:
                print("Estado inválido!")
                novo_estado = input("Novo estado: ").strip().lower()

            if novo_estado == estado_atual:
                print("O novo estado é igual ao atual. Nenhuma alteração efetuada.")
            else:
                inventario[codigo]['estado'] = novo_estado
                
                # Gestão da lista de reparação
                if novo_estado == 'avariado':
                    if codigo not in lista_reparacao:
                        lista_reparacao.append(codigo)
                else:
                    while codigo in lista_reparacao:
                        lista_reparacao.remove(codigo)

                msg = f"Estado de {codigo}: {estado_atual} -> {novo_estado}"
                historico.append(msg)
                print("Estado atualizado com sucesso!")

    # R5 - REMOVER EQUIPAMENTO
    elif opcao == '5':
        print("\n=== REMOVER EQUIPAMENTO ===")
        codigo = input("Introduza o código do equipamento: ").strip().upper()
        
        if codigo not in inventario:
            print("Equipamento não encontrado.")
        else:
            nome_eq = inventario[codigo]['nome'].title()
            confirma = input(f"Tem a certeza que deseja remover '{nome_eq}'? (s/n): ").strip().lower()
            
            if confirma == 's':
                del inventario[codigo]
                
                # Remover todas as ocorrências da lista de reparação
                while codigo in lista_reparacao:
                    lista_reparacao.remove(codigo)

                msg = f"Removido equipamento {codigo}"
                historico.append(msg)
                print("Equipamento removido com sucesso!")
            else:
                print("Operação cancelada.")

    # R6 - LISTA DE REPARAÇÃO
    elif opcao == '6':
        print("\n=== EQUIPAMENTOS A AGUARDAR REPARAÇÃO ===")
        if not lista_reparacao:
            print("Não existem equipamentos aguardando reparação.")
        else:
            num = 1
            for cod in lista_reparacao:
                nome_fmt = inventario[cod]['nome'].title()
                print(f"{num}. {cod} - {nome_fmt}")
                num += 1

            proc = input("Deseja processar todas as reparações? (s/n): ").strip().lower()
            if proc == 's':
                reparados_sessao = []
                while len(lista_reparacao) > 0:
                    cod_proc = lista_reparacao.pop(0)
                    inventario[cod_proc]['estado'] = 'operacional'
                    reparados.append(cod_proc)
                    reparados_sessao.append(cod_proc)
                    
                    msg = f"Reparado equipamento {cod_proc}"
                    historico.append(msg)
                    print(f"A reparar {cod_proc}...")

                print("Todas as reparações foram concluídas.")
                print(f"Equipamentos reparados nesta sessão: {reparados_sessao}")

    # R7 - ESTATÍSTICAS
    elif opcao == '7':
        print("\n=== ESTATÍSTICAS DO INVENTÁRIO ===")
        if not inventario:
            print("O inventário está vazio.")
        else:
            # List Comprehension para quantidades
            quantidades = [item['quantidade'] for item in inventario.values()]
            total_unidades = sum(quantidades)
            max_qtd = max(quantidades)
            min_qtd = min(quantidades)

            print(f"Total de registos no inventário: {len(inventario)}")
            print(f"Total de unidades em stock: {total_unidades}")
            print(f"Maior quantidade num equipamento: {max_qtd}")
            print(f"Menor quantidade num equipamento: {min_qtd}")

            # Tipos distintos com set() e sorted()
            tipos_existentes = sorted(set(item['tipo'] for item in inventario.values()))
            print(f"Tipos distintos existentes: {tipos_existentes}")

            # Contagem por estado com dicionário dinâmico
            contagem_estados = {}
            for item in inventario.values():
                est = item['estado']
                contagem_estados[est] = contagem_estados.get(est, 0) + 1
            
            print("\nRegistos por estado:")
            for est_nome, qtd_est in contagem_estados.items():
                print(f" - {est_nome}: {qtd_est}")

            # Unidades por sala percorrendo a tupla SALAS
            print("\nTotal de unidades por sala:")
            for s in SALAS:
                total_sala = sum(item['quantidade'] for item in inventario.values() if item['sala'] == s)
                print(f" - {s}: {total_sala} unidades")

    # R8 - HISTÓRICO DE OPERAÇÕES
    elif opcao == '8':
        print("\n=== HISTÓRICO DE OPERAÇÕES ===")
        if not historico:
            print("Ainda não foram realizadas operações nesta sessão.")
        else:
            print("Últimas 5 operações:")
            ultimas = historico[-5:]
            for op in ultimas:
                print(f" • {op}")
            print(f"\nTotal de operações realizadas na sessão: {len(historico)}")

    # 0 - SAIR
    elif opcao == '0':
        confirma = input("Tem a certeza que deseja sair? (s/n): ").strip().lower()
        if confirma == 's':
            ativo = False
            print("Programa encerrado. Bom trabalho!")

    # OPÇÃO INVÁLIDA
    else:
        print("Opção inválida! Escolha um número entre 0 e 8.")
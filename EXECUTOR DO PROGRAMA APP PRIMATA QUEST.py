import psycopg2
import psycopg2.extras
import json
import time
import os
import matplotlib.pyplot as plt

# === 1. CONFIGURAÇÃO DO BANCO (DBeaver/Postgres) ===
DB_CONFIG = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": os.getenv('DB_PASSWORD') or "1997"
}

if os.name == 'nt': os.system('') # Ativa cores no Terminal Windows

def conectar():
    return psycopg2.connect(**DB_CONFIG)

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

# === 2. FUNÇÕES ADMINISTRATIVAS (OPÇÃO 9) ===

def painel_admin():
    while True:
        limpar_tela()
        print("\033[91m" + "="*45)
        print("       🛡️ PAINEL DE CONTROLE ADMIN 🛡️")
        print("="*45 + "\033[0m")
        print("1. 👥 Listar Todos os Usuários")
        print("2. ➕ Adicionar Novo Usuário")
        print("3. 💀 Deletar Usuário por ID")
        print("4. 🔙 Voltar ao Menu Principal")
        
        escolha = input("\nSelecione uma ação: ")
        
        try:
            with conectar() as conn:
                with conn.cursor() as cur:
                    if escolha == "1":
                        cur.execute("SELECT id, nome, permissao, pontuacao_total FROM usuarios ORDER BY id")
                        usuarios = cur.fetchall()
                        print(f"\n{'ID':<5} | {'NOME':<20} | {'NÍVEL':<10} | {'PONTOS'}")
                        print("-" * 55)
                        for u in usuarios:
                            print(f"{u[0]:<5} | {u[1]:<20} | {u[2]:<10} | {u[3]}")
                        input("\nENTER para continuar...")
                    elif escolha == "2":
                        nome = input("Nome do Usuário: ").strip()
                        perm = input("Nível (admin/aluno): ").strip().lower()
                        cur.execute("INSERT INTO usuarios (nome, permissao, pontuacao_total) VALUES (%s, %s, 0)", (nome, perm))
                        conn.commit()
                        print(f"✅ {nome} cadastrado!")
                        time.sleep(1.5)
                    elif escolha == "3":
                        id_alvo = input("ID para remover: ")
                        cur.execute("DELETE FROM usuarios WHERE id = %s AND permissao != 'admin'", (id_alvo,))
                        conn.commit()
                        print("✅ Operação realizada.")
                        time.sleep(1.5)
                    elif escolha == "4": break
        except Exception as e:
            print(f"Erro: {e}"); time.sleep(2)

# === 3. FUNÇÕES DE ESTUDO E SIMULADO (OPÇÃO 1) ===

def executar_simulado_10(id_user):
    limpar_tela()
    print("🚀 INICIANDO SIMULADO: 10 QUESTÕES ALEATÓRIAS")
    time.sleep(1.5)
    acertos = 0
    try:
        with conectar() as conn:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("SELECT * FROM questoes ORDER BY RANDOM() LIMIT 10")
                questoes = cur.fetchall()
                
                for i, q in enumerate(questoes, 1):
                    limpar_tela()
                    print(f"📝 QUESTÃO {i}/10 | BANCA: {q['banca'].upper()}")
                    print("="*55)
                    print(f"{q['enunciado']}\n")
                    opts = json.loads(q['alternativas']) if isinstance(q['alternativas'], str) else q['alternativas']
                    for k, v in (opts.items() if isinstance(opts, dict) else enumerate(opts)):
                        print(f" {k}) {v}")
                    
                    res = input("\nSua resposta: ").strip().upper()
                    if res == str(q['gabarito']).upper():
                        print("\033[92m✅ CORRETO!\033[0m")
                        acertos += 1
                        cur.execute("UPDATE usuarios SET pontuacao_total = pontuacao_total + 1 WHERE id = %s", (id_user,))
                    else:
                        print(f"\033[91m❌ ERRADO! Gabarito: {q['gabarito']}\033[0m")
                        cur.execute("INSERT INTO historico_erros (usuario_id, materia, questao_enunciado) VALUES (%s, %s, %s)", 
                                    (id_user, q['materia'], q['enunciado']))
                    conn.commit()
                    time.sleep(1)
        
        limpar_tela()
        print("="*45)
        print(f"🏁 SIMULADO CONCLUÍDO! ACERTOS: {acertos}/10")
        print("="*45)
        input("\nENTER para voltar ao menu...")
    except Exception as e:
        print(f"Erro no simulado: {e}"); time.sleep(2)

def painel_estudos(id_user):
    limpar_tela()
    print("=== 🔍 FILTRAR POR BANCA ===")
    print("1. FGV | 2. SELECON | 3. FCC | 4. VOLTAR") # FCC Adicionada
    print("\033[93m5. 🔥 SIMULADO (10 QUESTÕES ALEATÓRIAS)\033[0m")
    
    b_op = input("\nEscolha: ")
    if b_op == "4": return
    if b_op == "5":
        executar_simulado_10(id_user)
        return
        
    # Mapeamento para as 3 bancas
    if b_op == "1":
        banca = "FGV"
    elif b_op == "2":
        banca = "SELECON"
    elif b_op == "3":
        banca = "FCC"
    else:
        return

    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT DISTINCT materia FROM questoes WHERE banca ILIKE %s", (f'%{banca}%',))
                materias = [row[0] for row in cur.fetchall()]
        
        if not materias:
            print(f"⚠️ Nenhuma questão da {banca} encontrada."); time.sleep(2); return

        limpar_tela()
        print(f"=== 📚 DISCIPLINAS ({banca}) ===")
        for i, m in enumerate(materias, 1): print(f"{i}. {m.upper()}")
        
        m_sel = int(input("\nEscolha a matéria: ")) - 1
        executar_questao(materias[m_sel], banca, id_user)
    except: pass

# === 3. FUNÇÕES DE ESTUDO E SIMULADO (OPÇÃO 1) ===

# === 3. FUNÇÕES DE ESTUDO E SIMULADO (OPÇÃO 1) ===

def painel_estudos(id_user):
    limpar_tela()
    print("=== 🔍 FILTRAR POR BANCA ===")
    print("1. FGV | 2. SELECON | 3. FCC | 4. VOLTAR")
    print("\033[93m5. 🔥 SIMULADO (10 QUESTÕES ALEATÓRIAS)\033[0m")
    
    op = input("\nEscolha: ")
    if op == "4": return
    if op == "5":
        executar_simulado_10(id_user)
        return
        
    mapa = {"1": "FGV", "2": "SELECON", "3": "FCC"}
    banca = mapa.get(op)
    if not banca: return

    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                # Busca as matérias agora no banco limpo
                cur.execute("SELECT DISTINCT materia FROM questoes WHERE banca ILIKE %s", (f'%{banca}%',))
                materias = [row[0] for row in cur.fetchall()]
        
        if not materias:
            print(f"⚠️ Nenhuma questão encontrada."); time.sleep(2); return

        limpar_tela()
        print(f"=== 📚 DISCIPLINAS ({banca}) ===")
        for i, m in enumerate(materias, 1): 
            print(f"{i}. {m.upper()}")
        
        m_sel = int(input("\nEscolha a matéria: ")) - 1
        # Inicia o estudo sequencial profissional
        executar_estudo_sequencial(materias[m_sel], banca, id_user)
        
    except Exception as e:
        print(f"Erro no painel: {e}"); time.sleep(2)

def executar_estudo_sequencial(materia, banca, id_user):
    try:
        with conectar() as conn:
            # RealDictCursor permite ler as colunas pelo nome: q['ano'], q['cargo']...
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                cur.execute("""
                    SELECT id, banca, enunciado, alternativas, gabarito,
                           orgao, ano, cargo
                    FROM questoes 
                    WHERE materia = %s AND banca ILIKE %s 
                    ORDER BY id ASC
                """, (materia, f'%{banca}%'))
                todas = cur.fetchall()
        
        if not todas:
            print("⚠️ Nenhuma questão disponível."); time.sleep(2); return

        total = len(todas)
        for num, q in enumerate(todas, 1):
            limpar_tela()
            
            # --- CABEÇALHO COM METADADOS ---
            print(f"\033[1;33m{'='*80}")
            print(f" QUESTÃO {num} de {total} | BANCA: {q['banca'].upper()}")
            # Mostra Órgão, Ano e Cargo se existirem
            meta = [f"ÓRGÃO: {q['orgao']}" if q['orgao'] else "", 
                    f"ANO: {q['ano']}" if q['ano'] else "", 
                    f"CARGO: {q['cargo']}" if q['cargo'] else ""]
            meta_filtrada = [m for m in meta if m]
            if meta_filtrada:
                print(f" {' | '.join(meta_filtrada)}")
            print(f"{'='*80}\033[0m")
            
            # ENUNCIADO
            print(f"\n{q['enunciado']}\n")
            
            # ALTERNATIVAS
            opts = q['alternativas'] if isinstance(q['alternativas'], dict) else json.loads(q['alternativas'])
            for letra, texto in sorted(opts.items()):
                print(f" \033[1;34m{letra})\033[0m {texto}")
            
            res = input("\n\033[1;32mSua resposta (ou 'SAIR'): \033[0m").strip().upper()
            
            if res == "SAIR": break
            
            # VALIDAÇÃO E PONTUAÇÃO
            if res == str(q['gabarito']).upper():
                print("\033[92m✅ ACERTOU!\033[0m")
                with conectar() as conn:
                    with conn.cursor() as cur_up:
                        cur_up.execute("UPDATE usuarios SET pontuacao_total = pontuacao_total + 1 WHERE id = %s", (id_user,))
                    conn.commit()
            else:
                print(f"\033[91m❌ ERRADO! Gabarito: {q['gabarito']}\033[0m")
                with conectar() as conn:
                    with conn.cursor() as cur_err:
                        cur_err.execute("""
                            INSERT INTO historico_erros (usuario_id, materia, questao_enunciado) 
                            VALUES (%s, %s, %s)
                        """, (id_user, materia, q['enunciado']))
                    conn.commit()
            
            # Pula para a próxima sem voltar ao menu
            input("\nENTER para a PRÓXIMA questão...")

    except Exception as e:
        print(f"Erro na execução: {e}"); time.sleep(2)


def executar_estudo_sequencial(materia, banca, id_user):
    try:
        with conectar() as conn:
            # RealDictCursor permite acessar os dados pelo nome da coluna: q['cargo']
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
                # SELECT trazendo os campos individuais. Se for nulo, traz vazio ''
                cur.execute("""
                    SELECT id, 
                           UPPER(banca) as banca_nome,
                           COALESCE(orgao, '') as orgao, 
                           COALESCE(ano::text, '') as ano, 
                           COALESCE(cargo, '') as cargo,
                           enunciado, alternativas, gabarito 
                    FROM questoes 
                    WHERE materia = %s AND banca ILIKE %s 
                    ORDER BY id ASC
                """, (materia, f'%{banca}%'))
                todas = cur.fetchall()
        
        if not todas:
            print("⚠️ Nenhuma questão encontrada nesta matéria."); time.sleep(2); return

        total = len(todas)
        for num, q in enumerate(todas, 1):
            limpar_tela()
            
            # === CABEÇALHO LIMPO (SÓ PREENCHE SE TIVER DADO) ===
            print(f"\033[1;33m{'='*85}")
            print(f" QUESTÃO {num} de {total} | BANCA: {q['banca_nome']}")
            
            # Monta a linha de metadados dinamicamente
            meta_info = []
            if q['orgao']: meta_info.append(f"ÓRGÃO: {q['orgao']}")
            if q['ano']: meta_info.append(f"ANO: {q['ano']}")
            if q['cargo']: meta_info.append(f"CARGO: {q['cargo']}")
            
            # Só imprime a linha se houver pelo menos um metadado
            if meta_info:
                print(f" {' | '.join(meta_info)}")
            
            print(f"{'='*85}\033[0m")
            
            # EXIBIÇÃO DO ENUNCIADO
            print(f"\n{q['enunciado']}\n")
            
            # TRATAMENTO DAS ALTERNATIVAS
            opts = q['alternativas']
            if isinstance(opts, str):
                opts = json.loads(opts)
            
            # Exibe ordenado por letra (A, B, C...)
            for letra, texto in sorted(opts.items()):
                print(f" \033[1;34m{letra})\033[0m {texto}")
            
            # INPUT DE RESPOSTA
            res = input("\n\033[1;32mSua resposta (ou 'SAIR'): \033[0m").strip().upper()
            
            if res == "SAIR": 
                break
            
            # VALIDAÇÃO E ATUALIZAÇÃO DO BANCO
            if res == str(q['gabarito']).upper():
                print("\033[92m✅ ACERTOU!\033[0m")
                with conectar() as conn:
                    with conn.cursor() as cur_up:
                        cur_up.execute("UPDATE usuarios SET pontuacao_total = pontuacao_total + 1 WHERE id = %s", (id_user,))
                    conn.commit()
            else:
                print(f"\033[91m❌ ERRADO! Gabarito: {q['gabarito']}\033[0m")
                with conectar() as conn:
                    with conn.cursor() as cur_err:
                        cur_err.execute("""
                            INSERT INTO historico_erros (usuario_id, materia, questao_enunciado) 
                            VALUES (%s, %s, %s)
                        """, (id_user, materia, q['enunciado']))
                    conn.commit()
            
            # PRÓXIMA QUESTÃO
            input("\nPressione ENTER para a PRÓXIMA questão...")

    except Exception as e:
        print(f"Erro na execução: {e}"); time.sleep(3)




# === 4. FUNÇÕES DE DESEMPENHO ===

def ver_ranking():
    limpar_tela()
    print("\n🏆 RANKING DE ELITE")
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT nome, pontuacao_total FROM usuarios ORDER BY pontuacao_total DESC LIMIT 3")
                for i, r in enumerate(cur.fetchall(), 1):
                    print(f"{i}º {r[0]} - {r[1]} Pontos")
        input("\nENTER para voltar...")
    except: pass

def ver_caderno_erros(id_user):
    limpar_tela()
    print("\n📚 MEU CADERNO DE ERROS (Últimos 5)")
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT materia, questao_enunciado FROM historico_erros WHERE usuario_id = %s ORDER BY id DESC LIMIT 5", (id_user,))
                erros = cur.fetchall()
                if not erros: print("✨ Tudo limpo por aqui!")
                for e in erros: print(f"- [{e[0]}] {e[1][:70]}...")
        input("\nENTER para voltar...")
    except: pass

def mostrar_grafico(id_user, nome):
    try:
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT materia, COUNT(*) FROM historico_erros WHERE usuario_id = %s GROUP BY materia", (id_user,))
                dados = cur.fetchall()
        if not dados: 
            print("\033[93m⚠️ Sem dados de erros para gerar o gráfico.\033[0m")
            time.sleep(1.5); return
        
        mats = [d[0] for d in dados]
        qtds = [d[1] for d in dados]
        plt.figure(figsize=(10, 6))
        plt.bar(mats, qtds, color='#e63946', edgecolor='black')
        plt.xticks(rotation=45, ha='right') 
        plt.title(f"DESEMPENHO POR MATÉRIA: {nome.upper()}")
        plt.ylabel("Quantidade de Erros")
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout() 
        plt.show()
    except Exception as e:
        print(f"Erro no gráfico: {e}"); time.sleep(2)

# === 5. LOGIN E MENU PRINCIPAL ===

def login():
    while True:
        limpar_tela()
        print("=== PRIMATA QUEST - SEU APP DA EVOLUÇÃO ===")
        nome = input("Usuário: ").strip()
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, nome, permissao FROM usuarios WHERE nome = %s", (nome,))
                u = cur.fetchone()
                if u: return u
        print("❌ Usuário inválido."); time.sleep(1)

def main():
    id_user, nome_user, nivel = login()
    while True:
        limpar_tela()
        with conectar() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT pontuacao_total FROM usuarios WHERE id = %s", (id_user,))
                p_fetch = cur.fetchone()
                pontos = p_fetch[0] if p_fetch else 0

        print("\n" + "="*50)
        status_label = "ADMIN" if nivel == 'admin' else "ALUNO"
        print(f"📝 CONCURSEIRO: {nome_user.upper()} | 🛡️ STATUS: {status_label}")
        print(f"🏆 PONTOS TOTAIS: {pontos}")
        print("="*50)
        
        print("1. 📝 ESTUDAR (PAINEL DE QUESTÕES)")
        print("2. 🏆 Ranking de Elite")
        print("3. 📚 Meu Caderno de Erros")
        print("4. 📊 Gráfico de Desempenho")
        print("5. 🚪 Sair do Aplicativo")
        
        if nivel == 'admin':
            print("\033[91m9. 🛡️ PAINEL ADMINISTRATIVO\033[0m")
        
        op = input("\nSelecione uma opção: ")
        
        if op == "1": painel_estudos(id_user)
        elif op == "2": ver_ranking()
        elif op == "3": ver_caderno_erros(id_user)
        elif op == "4": mostrar_grafico(id_user, nome_user)
        elif op == "5": 
            print(f"\n✨ Bons estudos, {nome_user}! Até a próxima."); break
        elif op == "9" and nivel == 'admin': painel_admin()
        else:
            print("\033[91m⚠️ Opção Inválida!\033[0m"); time.sleep(1)

if __name__ == "__main__":
    main()

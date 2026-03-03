import psycopg2
import psycopg2.extras
import json
import time
import os
import textwrap
import re
import matplotlib.pyplot as plt

# === CONFIGURAÇÕES GERAIS ===
DB_CONFIG = {"host": "localhost", "database": "postgres", "user": "postgres", "password": "1997"}

def limpar_tela(): 
    os.system('cls' if os.name == 'nt' else 'clear')

def conectar():
    return psycopg2.connect(**DB_CONFIG)

def organizar_texto(texto):
    if not texto: return ""
    texto = re.sub(r'(\w+)-\s+(\w+)', r'\1\2', texto)
    texto = " ".join(texto.split())
    texto = re.sub(r'^\d+[\.\-\s]+', '', texto)
    return texto.replace("Assinale a opção", "\n\nAssinale a opção")

# --- BUSCA DINÂMICA DE MATÉRIAS (VERSÃO BLINDADA) ---
def obter_materias_por_banca(banca):
    try:
        conn = conectar()
        cur = conn.cursor()
        # Buscamos as matérias removendo espaços e garantindo que não venham nulas
        sql = "SELECT DISTINCT TRIM(materia) FROM questoes WHERE banca ILIKE %s AND materia IS NOT NULL ORDER BY 1"
        cur.execute(sql, (f'%{banca}%',))
        
        # O fetchall retorna tuplas, extraímos o primeiro elemento [0] de cada uma
        rows = cur.fetchall()
        materias = [row[0] for row in rows if row[0]]
        
        conn.close()
        return materias
    except Exception as e:
        print(f"Erro ao acessar banco: {e}")
        return []

# --- MOTOR DE BUSCA DE QUESTÕES ---
def buscar_questao(materia_nome, id_usuario, banca_escolhida):
    try:
        conn = conectar()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        # ILIKE garante que encontre mesmo com diferenças de maiúsculas/minúsculas
        sql = """SELECT * FROM questoes 
                 WHERE banca ILIKE %s AND materia ILIKE %s 
                 AND LENGTH(enunciado) > 50 
                 ORDER BY RANDOM() LIMIT 1"""
        cur.execute(sql, (f'%{banca_escolhida}%', f'%{materia_nome}%'))
        q = cur.fetchone()
        conn.close()

        if not q:
            print(f"\n\033[1;31m⚠️ QUESTÃO NÃO ENCONTRADA.\033[0m")
            time.sleep(2); return

        limpar_tela()
        print(f"\033[1;33m[ BANCO: {q['banca']} ]\033[0m")
        print(f"\033[0;36mMATÉRIA: {q['materia'].upper()}\033[0m")
        print("="*75)
        
        enun = organizar_texto(q['enunciado'])
        print(textwrap.fill(enun, width=75))
        print("\n" + "="*75)

        opts = q['alternativas']
        if isinstance(opts, str): opts = json.loads(opts)
        for letra in sorted(opts.keys()): 
            print(f"  \033[1m{letra})\033[0m {organizar_texto(opts[letra])}")
        
        print("="*75)
        res_user = input("👉 SUA RESPOSTA: ").strip().upper()

        if res_user == q['gabarito'].upper():
            print("\n\033[1;32m✔ ACERTOU!\033[0m")
            salvar_progresso(id_usuario, True)
        else:
            print(f"\n\033[1;31m✘ ERROU. Gabarito: {q['gabarito']}\033[0m")
            salvar_progresso(id_usuario, False, enun, q['materia'])
        
        input("\n[Pressione ENTER]")
    except Exception as e: print(f"❌ Erro: {e}"); time.sleep(2)

# --- FUNÇÕES DE APOIO ---
def salvar_progresso(id_u, acertou, enun=None, mat=None):
    try:
        conn = conectar(); cur = conn.cursor()
        if acertou:
            cur.execute("UPDATE usuarios SET pontuacao_total = pontuacao_total + 1 WHERE id = %s", (id_u,))
        elif enun and mat:
            cur.execute("INSERT INTO historico_erros (usuario_id, questao_enunciado, materia) VALUES (%s, %s, %s)", (id_u, enun[:500], mat))
        conn.commit(); conn.close()
    except: pass

# --- MENU PRINCIPAL ---
def menu():
    # Login rápido
    limpar_tela()
    print("\033[1;34m=== PRIMATA QUEST - LOGIN ===\033[0m")
    nome_input = input("USUÁRIO: ").strip()
    
    conn = conectar()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT id, nome FROM usuarios WHERE nome ILIKE %s", (nome_input,))
    user = cur.fetchone()
    conn.close()

    if not user:
        print("❌ Usuário não encontrado."); return
    
    bancas = ["FGV", "SELECON", "CESPE", "FCC"]
    idx_banca = 0

    while True:
        banca_atual = bancas[idx_banca]
        # Carregamos as matérias reais do banco para esta banca
        materias_reais = obter_materias_por_banca(banca_atual)
        
        limpar_tela()
        print(f"\033[1;37mUSUÁRIO: {user['nome'].upper()} | BANCA: \033[1;32m{banca_atual}\033[0m")
        print("="*75)
        print(" [B] ALTERAR BANCA")
        print("-" * 75)
        
        if not materias_reais:
            print(f"  ⚠️ Nenhuma matéria cadastrada para {banca_atual}.")
            print("  Verifique se o nome da banca no banco de dados está correto.")
        else:
            for i, mat in enumerate(materias_reais, 1):
                # Exibe matérias em duas colunas
                print(f" [{i}] {mat.upper()[:25]:<28}", end="\n" if i % 2 == 0 else "")
            print()

        print("-" * 75)
        print(" [0] SAIR")
        print("="*75)
        
        esc = input("ESCOLHA UMA OPÇÃO: ").upper().strip()
        
        if esc == '0': break
        elif esc == 'B': idx_banca = (idx_banca + 1) % len(bancas)
        elif esc.isdigit():
            idx = int(esc) - 1
            if 0 <= idx < len(materias_reais):
                buscar_questao(materias_reais[idx], user['id'], banca_atual)
            else:
                print("Opção inválida!"); time.sleep(1)

if __name__ == "__main__":
    menu()

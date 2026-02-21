import psycopg2
import time

def conectar():
    return psycopg2.connect(host="localhost", database="postgres", user="postgres", password="1997")

def salvar_ponto(nome_usuario):
    """Adiciona +1 ponto no banco de dados para o Lucas"""
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("UPDATE usuarios SET pontuacao_total = pontuacao_total + 1 WHERE nome = %s", (nome_usuario,))
        conexao.commit()
        cursor.close()
        conexao.close()
    except Exception as e:
        print(f"Erro ao salvar: {e}")

def ver_placar(nome_usuario):
    """Busca o placar atual que está gravado no banco"""
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT pontuacao_total FROM usuarios WHERE nome = %s", (nome_usuario,))
    total = cursor.fetchone()[0]
    cursor.close()
    conexao.close()
    return total

def buscar_questao(materia_escolhida):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        sql = "SELECT enunciado, alternativas, gabarito FROM questoes WHERE materia = %s ORDER BY RANDOM() LIMIT 1"
        cursor.execute(sql, (materia_escolhida,))
        questao = cursor.fetchone()
        
        if questao:
            print(f"\n--- {materia_escolhida.upper()} ---")
            print(f"PERGUNTA: {questao[0]}")
            print(f"OPÇÕES: {questao[1]}")
            
            # --- CRONÔMETRO ---
            inicio = time.time()
            resposta = input("\nSua resposta (A/B/C/D/E): ").strip().upper()
            fim = time.time()
            tempo_gasto = fim - inicio
            # ------------------

            if tempo_gasto > 15: # LIMITE DE 15 SEGUNDOS
                print(f"⏰ TEMPO ESGOTADO! Você levou {tempo_gasto:.2f}s. (Limite: 15s)")
            elif resposta == questao[2].upper():
                print(f"✨ ACERTOU! Tempo: {tempo_gasto:.2f}s")
                salvar_ponto('Lucas') # Salva no banco!
            else:
                print(f"❌ ERROU! Gabarito: {questao[2]}")
        
        cursor.close()
        conexao.close()
    except Exception as e:
        print(f"Erro: {e}")

# --- MENU PRINCIPAL ---
while True:
    placar = ver_placar('Lucas') # Busca do banco toda vez que volta ao menu
    print(f"\n{'='*30}\n🏆 PLACAR PERMANENTE: {placar} PONTOS\n{'='*30}")
    print("1. PORTUGUÊS | 2. MATEMÁTICA | 3. SAIR")
    
    op = input("Escolha: ")
    if op == "1": buscar_questao("Português")
    elif op == "2": buscar_questao("Matemática")
    elif op == "3": 
        print(f"\n -✨ Você terminou com {placar} acertos... SEUS ESTUDOS DEPENDE DE VOCE CARO HEREMÍTA!!!")
        break
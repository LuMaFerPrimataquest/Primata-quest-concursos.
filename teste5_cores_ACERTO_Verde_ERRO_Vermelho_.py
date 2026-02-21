import psycopg2
import time
import os
# --- ADICIONE ISSO AQUI PARA AS CORES FUNCIONAREM ---
if os.name == 'nt':
    os.system('') 
# ----------------------------------------------------

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
    """Busca o placar atual. Se não achar, devolve 0 em vez de quebrar."""
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT pontuacao_total FROM usuarios WHERE nome = %s", (nome_usuario,))
        resultado = cursor.fetchone() # Pegamos o que veio do banco
        cursor.close()
        conexao.close()

        # O SEGREDO: Se o banco achou algo, pega o número [0]. Se não, devolve 0.
        if resultado:
            return resultado[0]
        else:
            return 0
    except:
        return 0 # Caso dê qualquer erro de conexão, o app não trava e mostra 0


def buscar_questao(materia_escolhida):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        sql = "SELECT enunciado, alternativas, gabarito FROM questoes WHERE materia = %s ORDER BY RANDOM() LIMIT 1"
        cursor.execute(sql, (materia_escolhida,))
        questao = cursor.fetchone()
        
        # ---limpar o terminal
        if questao:
            print(f"\n--- {materia_escolhida.upper()} ---")
            print(f"PERGUNTA: {questao[0]}")
            print("\nOPÇÕES:")
            for opções_texto in questao[1]:
                print(f"{opções_texto}")
            
            # --- CRONÔMETRO ---
            inicio = time.time()
            resposta = input("\nSua resposta (A/B/C/D/E): ").strip().upper()
            fim = time.time()
            tempo_gasto = fim - inicio
            # ------------------

            # LIMITE DE 15 SEGUNDOS - CORES: VERDE ACERTO - VERMELHO ERRO.
            if tempo_gasto > 15: 
                print(f"⏰ TEMPO ESGOTADO! Você levou {tempo_gasto:.2f}s. (Limite: 15s)")
            elif resposta == questao[2].upper():
                print(f"\033[92m ✨ ACERTOU! Tempo: {tempo_gasto:.2f}s \033[0m")
                salvar_ponto('Lucas') # Salva no banco!
            else:
                print(f"\033[91m ❌ ERROU! O gabarito era: {questao[2]} (Tempo: {tempo_gasto:.2f}s) \033[0m")

            print("\n" + "-"*30)
            input("\033[93mPressione ENTER para voltar ao menu...\033[0m") 
        
        cursor.close()
        conexao.close()
    except Exception as e:
        print(f"Erro: {e}")

# --- MENU PRINCIPAL ---
while True:
    # 1. Limpa a tela 
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # 2. BUSCA O PLACAR (É aqui que ela deve ficar!)
    placar_atual = ver_placar('Lucas') 
    
    # 3. MOSTRA O MENU
    print(f"\n{'='*35}\n🏆 PLACAR PERMANENTE: {placar_atual} PONTOS\n{'='*35}")
    print("1. PORTUGUÊS | 2. MATEMÁTICA | 3. SAIR")
    
    op = input("\nEscolha: ")
    
    if op == "1": buscar_questao("Português")
    elif op == "2": buscar_questao("Matemática")
    elif op == "3": 
        print(f"\n -✨ Você terminou com {placar_atual} acertos... SEUS ESTUDOS DEPENDE DE VOCE CARO MAGO HEREMÍTA !")
        break
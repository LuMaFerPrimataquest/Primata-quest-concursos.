import psycopg2
import json
import time
import os
if os.name == 'nt':
    os.system('') 

def conectar():
    return psycopg2.connect(host="localhost", database="postgres", user="postgres", password="1997")

# login

def fazer_login():
    while True: # O segredo: ele fica em loop até o nome ser válido
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== 🧙 PORTAL DO MAGO CONCURSEIRO ===")
        nome = input("Digite seu nome de usuário: ").strip()
        
        # --- A TRAVA DE SEGURANÇA (A CORREÇÃO) ---
        if not nome: # Se apertar ENTER sem digitar nada
            print("\033[91m⚠️ Erro: O nome não pode ser vazio!\033[0m")
            time.sleep(2)
            continue 
            
        if nome.isdigit(): # Se digitar apenas números (tipo o "1" que apareceu)
            print("\033[91m⚠️ Erro: O nome deve conter letras, não apenas números!\033[0m")
            time.sleep(2)
            continue
        # ------------------------------------------

        try:
            conexao = conectar()
            cursor = conexao.cursor()
            # Só chega aqui se o nome passou no teste acima!
            cursor.execute("INSERT INTO usuarios (nome, pontuacao_total) VALUES (%s, 0) ON CONFLICT (nome) DO NOTHING;", (nome,))
            conexao.commit()
            cursor.close()
            conexao.close()
            return nome # Retorna o nome limpo e correto
        except Exception as e:
            print(f"Erro no Portal: {e}")
            return "Convidado"
        

def salvar_ponto(nome_usuario):
    """Adiciona +1 ponto no banco de dados para o usuario_logado"""
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("UPDATE usuarios SET pontuacao_total = pontuacao_total + 1 WHERE nome = %s", (nome_usuario,))
        conexao.commit()
        cursor.close()
        conexao.close()
    except Exception as e:
        print(f"Erro ao salvar: {e}")

# --- ONDE SALVA O ERRO ---
def salvar_erro(nome_usuario, enunciado, materia):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        sql = "INSERT INTO historico_erros (nome_usuario, questao_enunciado, materia) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nome_usuario, enunciado, materia))
        conexao.commit() 
        cursor.close()
        conexao.close()
        # --- O AVISO PARA O ALUNO ---
        print("\033[93m📖 Questão salva no seu CADERNO DE ERROS!\033[0m")
    except Exception as e:
        print(f"Erro ao salvar histórico: {e}")


def ver_placar(nome_usuario):
    """Busca o placar atual. Se não achar, devolve 0 em vez de quebrar."""
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT pontuacao_total FROM usuarios WHERE nome = %s", (nome_usuario,))
        resultado = cursor.fetchone() 
        cursor.close()
        conexao.close()

        
        if resultado:
            return resultado[0]
        else:
            return 0
    except:
        return 0 
    # ---- INSERIMOS AQUI A NOVA FUNÇAO E ADICIONAMOS A OPÇAO 4 NO WHILE.
def ver_ranking():
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        # SQL de Elite: Ordena por pontos (DESC = decrescente) e limita a 3
        cursor.execute("SELECT nome, pontuacao_total FROM usuarios ORDER BY pontuacao_total DESC LIMIT 3;")
        top_alunos = cursor.fetchall()
        cursor.close()
        conexao.close()
        
        print("\n" + "🏆" + "="*30 + "🏆")
        print("      RANKING DE ELITE      ")
        print("="*32)
        
        for i, aluno in enumerate(top_alunos, 1):
            nome, pontos = aluno
            # Cores: O primeiro lugar fica em Amarelo (Ouro)
            cor = "\033[93m" if i == 1 else "\033[0m"
            print(f"{cor}{i}º Lugar: {nome} - {pontos} Pontos\033[0m")
        
        print("="*32)
        input("\n\033[93mPressione ENTER para voltar... \033[0m")
    except Exception as e:
        print(f"Erro no ranking: {e}")


def buscar_questao(materia_escolhida, nome_usuario):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        sql = "SELECT enunciado, alternativas, gabarito FROM questoes WHERE materia = %s ORDER BY RANDOM() LIMIT 1"
        cursor.execute(sql, (materia_escolhida,))
        questao = cursor.fetchone()
        
        
        if questao:
            print(f"\n--- {materia_escolhida.upper()} ---")
            print(f"PERGUNTA: {questao[0]}")
            print("\nOPÇÕES:")
            for opções_texto in questao[1]:
                print(f"{opções_texto}")
            
            
            inicio = time.time()
            resposta = input("\nSua resposta (A/B/C/D/E): ").strip().upper()
            fim = time.time()
            tempo_gasto = fim - inicio
            

            
            if tempo_gasto > 15: 
                print(f"⏰ TEMPO ESGOTADO! Você levou {tempo_gasto:.2f}s. (Limite: 15s)")
            elif resposta == questao[2].upper():
                print(f"\033[92m ✨ ACERTOU! Tempo: {tempo_gasto:.2f}s \033[0m")
                salvar_ponto(nome_usuario) 
            else:
                print(f"\033[91m ❌ ERROU! O gabarito era: {questao[2]} (Tempo: {tempo_gasto:.2f}s) \033[0m")
                salvar_erro(nome_usuario, questao[0], materia_escolhida)  # ADICIONAMOS ESTA LINHA SALVAR ERRO
            print("\n" + "-"*30)
            input("\033[93mPressione ENTER para voltar ao menu...\033[0m") 
        
        cursor.close()
        conexao.close()
    except Exception as e:
        print(f"Erro: {e}")

# CHAMANDO LOGIN ---

usuario_logado = fazer_login()  
# --- MENU PRINCIPAL ---

def ver_caderno_erros(nome_usuario):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        # Busca apenas os erros de QUEM ESTÁ LOGADO
        cursor.execute("SELECT materia, questao_enunciado, data_erro FROM historico_erros WHERE nome_usuario = %s ORDER BY data_erro DESC LIMIT 5", (nome_usuario,))
        erros = cursor.fetchall()
        cursor.close()
        conexao.close()

        print("\n" + "📚" + "="*35 + "📚")
        print(f"   CADERNO DE ERROS: {nome_usuario.upper()}   ")
        print("="*39)

        if not erros:
            print("✨ Você ainda não tem erros registrados! Parabéns.")
        else:
            for i, erro in enumerate(erros, 1):
                # erro[0] é materia, erro[1] é enunciado
                print(f"{i}. [\033[93m{erro[0]}\033[0m] - {erro[1][:60]}...") 
        
        print("="*39)
        input("\n\033[93mPressione ENTER para voltar ao menu... \033[0m")
    except Exception as e:
        print(f"Erro ao ler caderno: {e}")


# --- MENU PRINCIPAL ATUALIZADO ---
while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    placar_atual = ver_placar(usuario_logado)
    
    print("\n" + "="*40)
    print(f"🧙 MAGO: {usuario_logado.upper()} | 🏆 PLACAR: {placar_atual} PONTOS")
    print("="*40)
    print("1. PORTUGUÊS")
    print("2. MATEMÁTICA")
    print("3. RANKING DE ELITE (TOP 3)")
    print("4. MEU CADERNO DE ERROS 📚") # <--- NOVIDADE!
    print("5. SAIR DO APP")              # <--- MUDOU PARA 5
    print("="*40)

    op = input("\nEscolha (1 a 5): ")

    if op == "1":
        buscar_questao("Português", usuario_logado)
    elif op == "2":
        buscar_questao("Matemática", usuario_logado)
    elif op == "3":
        ver_ranking()
    elif op == "4":
        ver_caderno_erros(usuario_logado) # <--- CHAMA A FUNÇÃO NOVA
    elif op == "5":
        print(f"\n✨ {usuario_logado}, SEUS ESTUDOS DEPENDEM DE VOCÊ!")
        break
    else:
        print("\n⚠️ Opção inválida!")
        time.sleep(1)

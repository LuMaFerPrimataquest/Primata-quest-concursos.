import psycopg2
import json
import time
import os
import matplotlib.pyplot as plt 

# Pega a senha que você salvou no Windows (aquela do comando anterior)
senha_do_banco = os.getenv('DB_PASSWORD')

# Na hora de conectar, use a variável sem aspas
conexao = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password=senha_do_banco  # <-- SEM ASPAS AQUI
)

if os.name == 'nt':
    os.system('') 

def conectar():
    return psycopg2.connect(host="localhost", database="postgres", user="postgres", password="1997")

# --- FUNÇÕES DO SISTEMA ---

def fazer_login():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== 🧙 PORTAL DE ACESSO DO MAGO CONCURSEIRO ===")
        nome = input("Digite seu nome de usuário: ").strip()
        
        if not nome:
            print("\033[91m⚠️ Erro: tente novamente!\033[0m")
            time.sleep(2)
            continue

        try:
            conexao = conectar()
            cursor = conexao.cursor()
            cursor.execute("SELECT id, nome, permissao FROM usuarios WHERE nome = %s", (nome,))
            usuario = cursor.fetchone()
            cursor.close()
            conexao.close()

            if usuario:
                id_user, nome_real, permissao_raw = usuario
                # Blindagem total da permissão
                permissao = str(permissao_raw).strip().lower() if permissao_raw else "aluno"
                
                print(f"\033[92m✨ Bem-vindo de volta, {nome_real}!\033[0m")
                time.sleep(1)
                return id_user, nome_real, permissao 
            else:
                print("\033[91m❌ Erro: Usuário não encontrado!\033[0m")
                time.sleep(2)
        except Exception as e:
            print(f"Erro na conexão: {e}")
            time.sleep(3)

def salvar_ponto(id_usuario):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("UPDATE usuarios SET pontuacao_total = pontuacao_total + 1 WHERE id = %s", (id_usuario,))
        conexao.commit()
        cursor.close()
        conexao.close()
    except Exception as e:
        print(f"Erro ao salvar ponto: {e}")

def salvar_erro(id_usuario, enunciado, materia):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        
        # Note que passamos o id_usuario duas vezes: 
        # 1. Para buscar o nome do usuário
        # 2. Para preencher a coluna usuario_id que você criou
        sql = """INSERT INTO historico_erros (nome_usuario, questao_enunciado, materia, usuario_id) 
                 VALUES ((SELECT nome FROM usuarios WHERE id=%s), %s, %s, %s)"""
        
        cursor.execute(sql, (id_usuario, enunciado, materia, id_usuario))
        
        conexao.commit() 
        cursor.close()
        conexao.close()
        print("\033[93m📖 Questão salva no seu CADERNO DE ERROS!\033[0m")
    except Exception as e:
        print(f"❌ Erro ao salvar no banco: {e}")


def ver_placar(id_usuario):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT pontuacao_total FROM usuarios WHERE id = %s", (id_usuario,))
        resultado = cursor.fetchone() 
        cursor.close()
        conexao.close()
        return resultado[0] if resultado else 0
    except:
        return 0

def ver_ranking():
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT nome, pontuacao_total FROM usuarios ORDER BY pontuacao_total DESC LIMIT 3;")
        top_alunos = cursor.fetchall()
        cursor.close()
        conexao.close()
        print("\n🏆" + "="*30 + "🏆\n      RANKING DE ELITE      \n" + "="*32)
        for i, aluno in enumerate(top_alunos, 1):
            print(f"{i}º Lugar: {aluno[0]} - {aluno[1]} Pontos")
        input("\nPressione ENTER para voltar...")
    except Exception as e:
        print(f"Erro no ranking: {e}")

def buscar_questao(materia_escolhida, id_usuario):
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
            for op_txt in questao[1]: print(op_txt)
            
            inicio = time.time()
            res = input("\nSua resposta (A/B/C/D/E): ").strip().upper()
            tempo = time.time() - inicio
            
            if tempo > 15: 
                print(f"⏰ TEMPO ESGOTADO! ({tempo:.2f}s)")
            elif res == questao[2].upper():
                print(f"\033[92m ✨ ACERTOU! ({tempo:.2f}s) \033[0m")
                salvar_ponto(id_usuario)
            else:
                print(f"\033[91m ❌ ERROU! Gabarito: {questao[2]} \033[0m")
                salvar_erro(id_usuario, questao[0], materia_escolhida)
            input("\nENTER para voltar...")
        cursor.close()
        conexao.close()
    except Exception as e:
        print(f"Erro: {e}")

def ver_caderno_erros(id_usuario, nome_usuario):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT materia, questao_enunciado FROM historico_erros WHERE usuario_id = %s ORDER BY data_erro DESC LIMIT 5", (id_usuario,))
        erros = cursor.fetchall()
        cursor.close()
        conexao.close()

        print("\n📚" + "="*35 + "📚")
        print(f"   CADERNO DE ERROS: {nome_usuario.upper()}   ")
        print("="*39)
        if not erros:
            print("✨ Sem erros registrados!")
        else:
            for i, erro in enumerate(erros, 1):
                print(f"{i}. [{erro[0]}] - {erro[1][:60]}...") 
        input("\nENTER para voltar...")
    except Exception as e:
        print(f"Erro ao ler caderno: {e}")

def deletar_usuario_teste(nome_alvo):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM usuarios WHERE nome = %s AND permissao != 'admin'", (nome_alvo,))
        conexao.commit()
        if cursor.rowcount > 0:
            print(f"\n\033[92m✅ Usuário '{nome_alvo}' deletado!\033[0m")
        else:
            print(f"\n\033[91m❌ Falha ao deletar.\033[0m")
        cursor.close()
        conexao.close()
        time.sleep(2)
    except Exception as e:
        print(f"Erro: {e}")


def mostrar_mapa_de_erros(id_user, nome_user):
    try:
        # --- PARTE 1: BUSCA OS DADOS NO BANCO ---
        conexao = conectar()
        cursor = conexao.cursor()
        query = "SELECT materia, COUNT(*) FROM historico_erros WHERE usuario_id = %s GROUP BY materia"
        cursor.execute(query, (id_user,))
        dados = cursor.fetchall()
        cursor.close()
        conexao.close()

        # --- PARTE 2: PREPARA O GRÁFICO ---
        plt.figure(figsize=(10, 6))
        
        if not dados:
            # Lógica de Gênero que você pediu (Cara Concurseira)
            fem = nome_user.lower().endswith('a') or "wendy" in nome_user.lower()
            titulo = "Cara Concurseira" if fem else "Caro Concurseiro"
            
            plt.text(0.5, 0.5, f"✨ {titulo}, {nome_user}!\nVocê ainda não possui erros registrados.", 
                     fontsize=12, ha='center', va='center', fontweight='bold')
            plt.title(f"MAPA DE DESEMPENHO: {nome_user.upper()}")
            plt.axis('off') 
        else:
            # --- PARTE 2 (AJUSTADA PARA VERMELHO) ---
            materias = [item[0] for item in dados]
            quantidades = [item[1] for item in dados]
            
            # Mudamos de uma lista de cores para uma cor única: VERMELHO
            plt.bar(materias, quantidades, color='#e63946', edgecolor='black', linewidth=1.2)
            
            # Dica de Professor: Adiciona o número de erros no topo da barra
            for i, valor in enumerate(quantidades):
                plt.text(i, valor + 0.1, str(valor), ha='center', fontweight='bold', color='red')

            plt.ylabel("Quantidade de Erros")
            plt.title(f"🚨 MAPA DE ERROS: {nome_user.upper()}", color='#9d0208', fontsize=14)

            plt.title(f"GRAFICO DE ERROS - DESEMPENHO: {nome_user.upper()}")

        # --- PARTE 3: MOSTRA E LIMPA ---
        print(f"\033[94m🎨 Abrindo mapa de desempenho de {nome_user}...\033[0m")
        plt.show()
        plt.close() # Importante para não travar o próximo gráfico!

    except Exception as e:
        print(f"Erro visual: {e}")





# --- EXECUÇÃO DO APP (Onde a mágica começa) ---

# Passo único: logar e pegar permissão
id_logado, usuario_logado, nivel_permissao = fazer_login() 

while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    placar_atual = ver_placar(id_logado) 
    
    print("\n" + "="*40)
    print(f"🧙 MAGO: {usuario_logado.upper()} | 🏆 PLACAR: {placar_atual}")
    print("="*40)
    print("1. PORTUGUÊS")
    print("2. MATEMÁTICA")
    print("3. RANKING DE ELITE (TOP 3)")
    print("4. MEU CADERNO DE ERROS 📚")
    print("5. SAIR DO APP")
    print("7. VER MEU DESEMPENHO (GRÁFICO) 📊") # <--- NOVA OPÇÃO
    

    
    
    if nivel_permissao == 'admin':
        print("\033[91m9. [PAINEL DELETAR USUARIO] - SOMENTE ADMINISTRADOR 💀\033[0m")

    print("="*40)
    op = input("\nEscolha: ")

    if op == "1":
        buscar_questao("Português", id_logado)
    elif op == "2":
        buscar_questao("Matemática", id_logado)
    elif op == "3":
        ver_ranking()
    elif op == "4":
        ver_caderno_erros(id_logado, usuario_logado)
    elif op == "7":
        # Passamos o ID e o Nome para a função ser completa
        mostrar_mapa_de_erros(id_logado, usuario_logado)  # <--- CHAMA A FUNÇÃO
    elif op == "5":
        print(f"\n✨ Até logo, {usuario_logado}!")
        break
    elif op == "9" and nivel_permissao == 'admin':
        nome_lixo = input("Nome do usuário para DELETAR: ").strip()
        confirmar = input(f"Confirmar exclusão de {nome_lixo}? (S/N): ").upper()
        if confirmar == 'S':
            deletar_usuario_teste(nome_lixo)
    else:
        print("\n⚠️ Opção inválida!")
        time.sleep(1)

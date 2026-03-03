import psycopg2
import json
import time
import os
import matplotlib.pyplot as plt 
import unicodedata

# 1. Configuração de Ambiente e Segurança
senha_do_banco = os.getenv('DB_PASSWORD') or "1997" # Fallback para 1997 se a variável falhar

if os.name == 'nt':
    os.system('') # Ativa cores ANSI no terminal Windows

def conectar():
    """Conecta ao banco usando a senha do ambiente ou o padrão de segurança."""
    return psycopg2.connect(
        host="localhost", 
        database="postgres", 
        user="postgres", 
        password=senha_do_banco
    )

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
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome, permissao FROM usuarios WHERE nome = %s", (nome,))
            usuario = cursor.fetchone()
            cursor.close()
            conn.close()

            if usuario:
                id_user, nome_real, permissao_raw = usuario
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
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE usuarios SET pontuacao_total = pontuacao_total + 1 WHERE id = %s", (id_usuario,))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao salvar ponto: {e}")

def salvar_erro(id_usuario, enunciado, materia):
    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = """INSERT INTO historico_erros (nome_usuario, questao_enunciado, materia, usuario_id) 
                 VALUES ((SELECT nome FROM usuarios WHERE id=%s), %s, %s, %s)"""
        cursor.execute(sql, (id_usuario, enunciado, materia, id_usuario))
        conn.commit() 
        cursor.close()
        conn.close()
        print("\033[93m📖 Questão salva no seu CADERNO DE ERROS!\033[0m")
    except Exception as e:
        print(f"❌ Erro ao salvar erro no banco: {e}")

def ver_placar(id_usuario):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT pontuacao_total FROM usuarios WHERE id = %s", (id_usuario,))
        resultado = cursor.fetchone() 
        cursor.close()
        conn.close()
        return resultado[0] if resultado else 0
    except:
        return 0

def buscar_questao(materia_escolhida, id_usuario):
    try:
        conn = conectar()
        cursor = conn.cursor()
        # Busca uma questão aleatória da matéria selecionada
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
            
            if tempo > 20: # Aumentei um pouco o tempo para leitura
                print(f"⏰ TEMPO ESGOTADO! ({tempo:.2f}s)")
            elif res == str(questao[2]).upper():
                print(f"\033[92m ✨ ACERTOU! ({tempo:.2f}s) \033[0m")
                salvar_ponto(id_usuario)
            else:
                print(f"\033[91m ❌ ERROU! Gabarito: {questao[2]} \033[0m")
                salvar_erro(id_usuario, questao[0], materia_escolhida)
            input("\nENTER para continuar...")
        else:
            print(f"\033[93m⚠️ Nenhuma questão de {materia_escolhida} encontrada no banco.\033[0m")
            time.sleep(2)
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao buscar questão: {e}")
        time.sleep(2)

def mostrar_mapa_de_erros(id_user, nome_user):
    try:
        conn = conectar()
        cursor = conn.cursor()
        query = "SELECT materia, COUNT(*) FROM historico_erros WHERE usuario_id = %s GROUP BY materia"
        cursor.execute(query, (id_user,))
        dados = cursor.fetchall()
        cursor.close()
        conn.close()

        plt.figure(figsize=(10, 6))
        
        if not dados:
            fem = nome_user.lower().endswith('a') or "wendy" in nome_user.lower()
            titulo = "Cara Concurseira" if fem else "Caro Concurseiro"
            plt.text(0.5, 0.5, f"✨ {titulo}, {nome_user}!\nVocê ainda não possui erros registrados.", 
                     fontsize=12, ha='center', va='center', fontweight='bold')
            plt.title(f"MAPA DE DESEMPENHO: {nome_user.upper()}")
            plt.axis('off') 
        else:
            materias = [item[0] for item in dados]
            quantidades = [item[1] for item in dados]
            
            plt.bar(materias, quantidades, color='#e63946', edgecolor='black', linewidth=1.2)
            
            for i, valor in enumerate(quantidades):
                plt.text(i, valor + 0.1, str(valor), ha='center', fontweight='bold', color='red')

            plt.ylabel("Quantidade de Erros")
            plt.title(f"🚨 MAPA DE ERROS: {nome_user.upper()}", color='#9d0208', fontsize=14, fontweight='bold')
            plt.xticks(rotation=45)
            plt.tight_layout()

        print(f"\033[94m🎨 Abrindo mapa de desempenho de {nome_user}...\033[0m")
        plt.show()
        plt.close() 

    except Exception as e:
        print(f"Erro visual: {e}")

def ver_ranking():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT nome, pontuacao_total FROM usuarios ORDER BY pontuacao_total DESC LIMIT 3;")
        top_alunos = cursor.fetchall()
        cursor.close()
        conn.close()
        print("\n🏆" + "="*30 + "🏆\n      RANKING DE ELITE      \n" + "="*32)
        for i, aluno in enumerate(top_alunos, 1):
            print(f"{i}º Lugar: {aluno[0]} - {aluno[1]} Pontos")
        input("\nPressione ENTER para voltar...")
    except Exception as e:
        print(f"Erro no ranking: {e}")

def ver_caderno_erros(id_usuario, nome_usuario):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT materia, questao_enunciado FROM historico_erros WHERE usuario_id = %s ORDER BY data_erro DESC LIMIT 5", (id_usuario,))
        erros = cursor.fetchall()
        cursor.close()
        conn.close()

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
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE nome = %s AND permissao != 'admin'", (nome_alvo,))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"\n\033[92m✅ Usuário '{nome_alvo}' deletado!\033[0m")
        else:
            print(f"\n\033[91m❌ Falha ao deletar.\033[0m")
        cursor.close()
        conn.close()
        time.sleep(2)
    except Exception as e:
        print(f"Erro: {e}")

# --- EXECUÇÃO DO APP ---

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
    print("7. VER MEU DESEMPENHO (GRÁFICO) 📊")
    
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
        mostrar_mapa_de_erros(id_logado, usuario_logado)
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

import psycopg2
import matplotlib.pyplot as plt

def conectar():
    return psycopg2.connect(host="localhost", database="postgres", user="postgres", password="1997")

def mostrar_mapa_de_erros(id_user, nome_user):
    try:
        conexao = conectar()
        cursor = conexao.cursor()

        # SQL de Inteligência: Conta erros por matéria
        query = """
            SELECT materia, COUNT(*) 
            FROM historico_erros 
            WHERE nome_usuario = %s 
            GROUP BY materia
        """
        cursor.execute(query, (nome_user,))
        dados = cursor.fetchall()
        cursor.close()
        conexao.close()

        if not dados:
            print(f"✨ O Mago {nome_user} ainda não tem erros registrados. Continue estudando!")
            return

        # Separando os dados (Mágica do Python)
        materias = [item[0] for item in dados]
        quantidades = [item[1] for item in dados]

        # --- CRIANDO O GRÁFICO ---
        plt.style.use('ggplot') # Estilo visual moderno
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Desenha as barras em vermelho (Alerta de Erro!)
        barras = ax.bar(materias, quantidades, color='#e63946', edgecolor='black')

        # Adiciona os números em cima das barras
        ax.bar_label(barras, padding=3, fontweight='bold')

        # Perfumaria de Elite (UX)
        ax.set_title(f"📊 RELATÓRIO ESTRATÉGICO: {nome_user.upper()}", fontsize=16, pad=20)
        ax.set_ylabel("Quantidade de Erros", fontsize=12)
        ax.set_xlabel("Disciplinas", fontsize=12)

        print(f"🎨 Desenhando mapa para {nome_user}... A janela vai abrir!")
        plt.show()

    except Exception as e:
        print(f"Erro ao gerar o gráfico: {e}")

# --- com o usuario do aluno rode esta linha para ver seus erros  ---

mostrar_mapa_de_erros(12, 'Wendy Tattoo')

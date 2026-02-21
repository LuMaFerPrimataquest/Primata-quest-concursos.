import psycopg2

# Criamos a variável de pontos FORA da função para ela não zerar
acertos = 0

def buscar_questao(materia_escolhida):
    global acertos # Avisamos que vamos usar a variável lá de fora
    try:
        conexao = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="1997")
        cursor = conexao.cursor()
        
        sql = "SELECT enunciado, alternativas, gabarito FROM questoes WHERE materia = %s ORDER BY RANDOM() LIMIT 1"
        cursor.execute(sql, (materia_escolhida,))
        questao = cursor.fetchone()
        
        if questao:
            print(f"\n--- QUESTÃO DE {materia_escolhida.upper()} ---")
            print(f"PERGUNTA: {questao[0]}")
            print(f"OPÇÕES: {questao[1]}")
            
            # MUDANÇA AQUI: Agora o usuário responde!
            resposta_usuario = input("\nQual sua resposta? (A/B/C/D/E): ").strip().upper()
            
            if resposta_usuario == questao[2].upper():
                print("✨ PARABÉNS! Você acertou!")
                acertos += 1 # Soma 1 ponto
            else:
                print(f"❌ ERROU! O gabarito correto era: {questao[2]}")
        else:
            print("\n❌ Nenhuma questão encontrada.")
            
        cursor.close()
        conexao.close()
    except Exception as e:
        print(f"Erro: {e}")

# --- MENU PRINCIPAL ---
while True: 
    print("\n" + "="*40)
    print(f"=== PLACAR ATUAL: {acertos} ACERTOS ===") # Mostra os pontos!
    print("1. Estudar PORTUGUÊS")
    print("2. Estudar MATEMÁTICA")
    print("3. SAIR DO APP")
    print("="*40)

    opcao = input("Escolha (1, 2 ou 3): ")

    if opcao == "1":
        buscar_questao("Português")
    elif opcao == "2":
        buscar_questao("Matemática")
    elif opcao == "3":
        print(f"\n -✨ Você terminou com {acertos} acertos... SEUS ESTUDOS DEPENDE DE VOCE CARA !!!")
        break
    else:
        print("\n⚠️ Opção inválida!")

import psycopg2

def buscar_questao(materia_escolhida):
    try:
        conexao = psycopg2.connect(host="localhost", database="postgres", user="postgres", password="1997")
        cursor = conexao.cursor()
        
        # O Python coloca o que o usuário digitou dentro do SQL!
        sql = "SELECT enunciado, alternativas, gabarito FROM questoes WHERE materia = %s ORDER BY RANDOM() LIMIT 1"
        cursor.execute(sql, (materia_escolhida,))
        
        questao = cursor.fetchone()
        
        if questao:
            print(f"\n--- QUESTÃO DE {materia_escolhida.upper()} ---")
            print(f"PERGUNTA: {questao[0]}")
            print(f"OPÇÕES: {questao[1]}")
            input("\nAperte ENTER para ver o gabarito...")
            print(f"✅ GABARITO CORRETO: {questao[2]}")
        else:
            print("\n❌ Nenhuma questão encontrada para essa matéria.")
            
        cursor.close()
        conexao.close()
    except Exception as e:
        print(f"Erro: {e}")

# --- O MENU COMEÇA AQUI ---
while True: 
    print("\n" + "="*40)
    print("=== APP DE QUESTÕES - MENU PRINCIPAL ! ===")
    print("1. Estudar PORTUGUÊS !")
    print("2. Estudar MATEMÁTICA !")
    print("3. Sair do Aplicativo !")
    print("="*40)

    opcao = input("Escolha uma opção (1, 2 ou 3): ")

    if opcao == "1":
        buscar_questao("Português")
    elif opcao == "2":
        buscar_questao("Matemática")
    elif opcao == "3":
        print("\n --- 😉 VOLTE SEMPRE ! ... SEUS ESTUDOS DEPENDE DE VOCÊ ...  😜✌️ ---")
        break
    else:
        print("\n Opção inválida! Tente novamente.")
        
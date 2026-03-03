**select \* from questoes;**

**select  \* from historico\_erros;**

**select \* from usuarios u**

**------------------------------------**





**3. Principais Componentes Visuais**

**Para o seu Primata Quest, a interface ganharia estes elementos:**



    \*\*Cards: Você pode colocar a pergunta dentro de um "Cartão" branco com sombra para destacar do fundo.\*\*

&nbsp;   \\\*\\\*Progress Bar: Para mostrar o tempo de resposta diminuindo visualmente.\\\*\\\*

    \\\*\\\*ListTiles: Para listar as alternativas de forma organizada.\\\*\\\*

    \\\*\\\*Modais/Dialogs: Aquelas janelas que saltam na tela dizendo "Parabéns! Você acertou 8/10 questões".\\\*\\\*





eae doido







**----------------------------------------------------------------------------**





**Opção A: O Ranking de Elite (Top 3): Criar um novo comando no menu que busca no banco quem são os melhores alunos (mesmo que por enquanto seja só você, é bom deixar pronto para quando o app tiver mais usuários).**

**Opção B: O Detector de Fraquezas (Histórico de Erros): Criar uma nova tabela no SQL para salvar quais questões você errou. Assim, o app pode te perguntar no futuro: "Lucas, quer refazer as questões que você errou ontem?".**

**Opção C: Cadastro via Python: Parar de usar o DBeaver para cadastrar e criar uma opção no menu para você mesmo digitar as questões novas direto no terminal.**



**------------------------------------------------------------------------------**

**Seu App já tem:**



* \*\*Coração: Banco de Dados (PostgreSQL).\*\*
* \*\*Cérebro: Lógica de questões, tempo e filtros (Python).\*\*
* \*\*Memória: Placar permanente que não zera (Update no SQL).\*\*
* \*\*Estética: Limpeza de tela e feedback visual (Cores Verde, Vermelho e Amarelo).\*\*
* 

**--------------------------------------------------------------------------------**



**PARAMOS NA PARTE DE APRENDER A LIMPAR A TELA DO JOGO: COMECE PERGUTNDANDO COMO FAZER COMQUE O JOGO LIMPE A TELA DO TERMINAL SEMPRE QUE ENCERRAR UMA QUESTAO SEJA ELA CERTA OU ERRADA.**

 



---

2\. Como a biblioteca funciona (A Lógica)

A Psycopg2 trabalha com três passos fundamentais que você deve decorar:



    Connection (Conexão): Abre o cano de comunicação com o banco.

    Cursor: É o seu "mensageiro". Ele leva o comando SQL e traz o resultado.

    Fetch (Busca): É o ato de pegar o resultado que o mensageiro trouxe e colocar numa variável.



---



SELECT \* FROM questoes

WHERE materia = 'Matemática';



---



SELECT \* FROM questoes

WHERE materia = 'Português';



---



-- QUESTÕES DE PORTUGUÊS

INSERT INTO questoes (banca, materia, assunto, enunciado, alternativas, gabarito) VALUES

('FGV', 'Português', 'Crase', 'Assinale a opção com crase correta.', '\["A) Vou a casa", "B) Vou à Bahia", "C) A prazo", "D) As vezes"]'::jsonb, 'B'),

('FGV', 'Português', 'Pontuação', 'Onde falta uma vírgula?', '\["A) Maria correu.", "B) João o médico saiu.", "C) Sim eu vou.", "D) Olá!"]'::jsonb, 'C'),

('CESPE', 'Português', 'Acentuação', 'Qual palavra é proparoxítona?', '\["A) Café", "B) Árvore", "C) Caju", "D) Item"]'::jsonb, 'B'),

('CESPE', 'Português', 'Verbos', 'Qual o tempo de "Eu cantarei"?', '\["A) Presente", "B) Pretérito", "C) Futuro", "D) Imperfeito"]'::jsonb, 'C'),

('VUNESP', 'Português', 'Sintaxe', 'O que é o sujeito em "O sol brilha"?', '\["A) O sol", "B) Brilha", "C) Inexistente", "D) O"]'::jsonb, 'A'),

('VUNESP', 'Português', 'Ortografia', 'Qual grafia está correta?', '\["A) Excessão", "B) Exceção", "C) Ezceção", "D) Exceção"]'::jsonb, 'B'),

('FCC', 'Português', 'Concordância', 'Qual frase está correta?', '\["A) Fazem dois anos", "B) Faz dois anos", "C) Houveram erros", "D) Menos pessoas"]'::jsonb, 'B'),

('FCC', 'Português', 'Pronomes', 'Qual pronome é de tratamento?', '\["A) Eu", "B) Você", "C) Vossa Excelência", "D) Meu"]'::jsonb, 'C'),

('FGV', 'Português', 'Significação', 'Sinônimo de efêmero?', '\["A) Eterno", "B) Rápido", "C) Passageiro", "D) Forte"]'::jsonb, 'C'),

('CESPE', 'Português', 'Morfologia', 'Qual o substantivo?', '\["A) Belo", "B) Correr", "C) Casa", "D) Rapidamente"]'::jsonb, 'C');



-- QUESTÕES DE MATEMÁTICA

INSERT INTO questoes (banca, materia, assunto, enunciado, alternativas, gabarito) VALUES

('FCC', 'Matemática', 'Porcentagem', 'Quanto é 20% de 500?', '\["A) 50", "B) 100", "C) 150", "D) 200"]'::jsonb, 'B'),

('FCC', 'Matemática', 'Frações', 'Quanto é 1/2 + 1/4?', '\["A) 1/8", "B) 3/4", "C) 1/4", "D) 2/4"]'::jsonb, 'B'),

('CESPE', 'Matemática', 'Equação', 'Valor de x em x + 5 = 10?', '\["A) 2", "B) 5", "C) 10", "D) 15"]'::jsonb, 'B'),

('CESPE', 'Matemática', 'Geometria', 'Lados de um triângulo?', '\["A) 2", "B) 3", "C) 4", "D) 5"]'::jsonb, 'B'),

('FGV', 'Matemática', 'Probabilidade', 'Chance de cara na moeda?', '\["A) 25%", "B) 50%", "C) 75%", "D) 100%"]'::jsonb, 'B'),

('FGV', 'Matemática', 'Média', 'Média de 4 e 6?', '\["A) 4", "B) 5", "C) 6", "D) 10"]'::jsonb, 'B'),

('VUNESP', 'Matemática', 'Tabuada', '7 vezes 8 é quanto?', '\["A) 49", "B) 54", "C) 56", "D) 64"]'::jsonb, 'C'),

('VUNESP', 'Matemática', 'Divisão', '100 dividido por 4?', '\["A) 20", "B) 25", "C) 40", "D) 50"]'::jsonb, 'B'),

('FCC', 'Matemática', 'Subtração', '1000 menos 450?', '\["A) 550", "B) 650", "C) 450", "D) 500"]'::jsonb, 'A'),

('CESPE', 'Matemática', 'Lógica', 'Qual o próximo número: 2, 4, 6...?', '\["A) 7", "B) 8", "C) 9", "D) 10"]'::jsonb, 'B');


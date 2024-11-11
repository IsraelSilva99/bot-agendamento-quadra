Bot de Agendamento de Quadra

Este repositório contém o código fonte para um bot do Telegram que permite agendar, desmarcar e editar reservas de uma quadra.


Funcionalidades:
Agendamento de reservas: Permite que os usuários agendem reservas de uma quadra especificando a data e o horário desejados.
Desmarcação de reservas: Permite que os usuários cancelem suas reservas existentes.
Edição de reservas: Permite que os usuários alterem a data e o horário de suas reservas.
Geração de Relatório (Somente para Administradores): Permite que o administrador gere um relatório PDF com todas as reservas.

Requisitos:
Python 3.7+
Biblioteca telebot
Biblioteca sqlite3
Biblioteca datetime
Biblioteca fpdf

Instalação:
Clone este repositório.
Crie um arquivo chamado config.py na mesma pasta do script principal.
Adicione o token do seu bot do Telegram no arquivo config.py da seguinte forma:
TOKEN = 'SEU_TOKEN_DO_TELEGRAM'
pip install -r requirements.txt

Execute o script principal.

Uso:
Adicione o bot ao seu grupo ou conversa privada do Telegram.
Envie o comando /start para iniciar o bot.
Use os botões do menu para agendar, desmarcar ou editar reservas.
Para gerar um relatório de agendamentos, use o comando /relatorio.

Observações:
O bot armazena os dados das reservas em um banco de dados SQLite.
O bot oferece opções de horários pré-definidos para agendamento, mas pode ser facilmente adaptado para outras necessidades.
O código inclui validações para garantir que os dados inseridos pelos usuários sejam válidos.
A funcionalidade de gerar relatório está disponível apenas para o administrador.

Contribuições:
Contribuições são bem-vindas! Se você encontrar algum erro ou tiver alguma sugestão de melhoria, sinta-se à vontade para abrir uma issue ou enviar um pull request.

![Imagem do WhatsApp de 2024-11-11 à(s) 15 23 59_b4082719](https://github.com/user-attachments/assets/48298275-e5e3-4bb2-bd7a-ac7c26c636b2)
![Imagem do WhatsApp de 2024-11-11 à(s) 15 23 59_1e7afe35](https://github.com/user-attachments/assets/0db88aa4-a7b7-47ee-9fb0-59e2a73b3a13)
![Imagem do WhatsApp de 2024-11-11 à(s) 15 24 00_c92af718](https://github.com/user-attachments/assets/b01a51c4-1a0f-4d05-a583-f0fbdb0ae0ce)
![Imagem do WhatsApp de 2024-11-11 à(s) 15 24 00_225a7f20](https://github.com/user-attachments/assets/dd82dd61-4c85-4d43-bb23-d0ed028d39ff)
![Imagem do WhatsApp de 2024-11-11 à(s) 15 24 01_4b3587f4](https://github.com/user-attachments/assets/92529d95-b19b-45a0-aba2-668d92a0e51c)

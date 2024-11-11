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
content_copy
Use code with caution.
Python

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

## Bot de Agendamento de Quadra 🏀

Este repositório contém o código fonte para um bot do Telegram que facilita o gerenciamento de reservas de uma quadra esportiva. Com ele, os usuários podem agendar, desmarcar e editar suas reservas de forma simples e intuitiva.

**Funcionalidades:**

* **Agendamento de Reservas:** Permite agendar reservas de quadra, especificando data e horário desejados.
* **Desmarcação de Reservas:** Cancela reservas existentes de forma rápida e fácil.
* **Edição de Reservas:** Altera a data e o horário de reservas já agendadas.
* **Geração de Relatório (Somente para Administradores):** Permite gerar um relatório PDF completo com todas as reservas, ideal para controle e organização.

**Requisitos:**

* Python 3.7+
* Bibliotecas:
    * `telebot`
    * `sqlite3`
    * `datetime`
    * `fpdf`

**Instalação:**

1. Clone este repositório.
2. Crie um arquivo chamado `config.py` na mesma pasta do script principal.
3. Adicione o token do seu bot do Telegram no arquivo `config.py` da seguinte forma:

```python
TOKEN = 'SEU_TOKEN_DO_TELEGRAM'
```
4. Instale as dependências: `pip install -r requirements.txt`
5. Execute o script principal.

**Uso:**

1. Adicione o bot ao seu grupo ou conversa privada do Telegram.
2. Envie o comando `/start` para iniciar o bot.
3. Utilize os botões do menu para agendar, desmarcar ou editar reservas.
4. Para gerar um relatório de agendamentos, utilize o comando `/relatorio` (somente para administradores).

**Observações:**

* O bot armazena os dados das reservas em um banco de dados SQLite.
* O bot oferece opções de horários pré-definidos para agendamento, mas pode ser facilmente adaptado para outras necessidades.
* O código inclui validações para garantir a integridade dos dados inseridos pelos usuários.
* A funcionalidade de geração de relatório está disponível apenas para o administrador.

**Contribuições:**

Contribuições são bem-vindas! Se você encontrar algum erro ou tiver sugestões de melhoria, sinta-se à vontade para abrir uma issue ou enviar um pull request.


* **Documentação do Telebot:** [https://telethon.readthedocs.io/en/stable/](https://telethon.readthedocs.io/en/stable/)
* **Documentação do FPDF:** [https://pypi.org/project/fpdf2/](https://pypi.org/project/fpdf2/)

**Licença:**

Este projeto está licenciado sob a licença MIT.


![Imagem do WhatsApp de 2024-11-11 à(s) 15 23 59_b4082719](https://github.com/user-attachments/assets/48298275-e5e3-4bb2-bd7a-ac7c26c636b2)
![Imagem do WhatsApp de 2024-11-11 à(s) 15 23 59_1e7afe35](https://github.com/user-attachments/assets/0db88aa4-a7b7-47ee-9fb0-59e2a73b3a13)
![Imagem do WhatsApp de 2024-11-11 à(s) 15 24 00_c92af718](https://github.com/user-attachments/assets/b01a51c4-1a0f-4d05-a583-f0fbdb0ae0ce)
![Imagem do WhatsApp de 2024-11-11 à(s) 15 24 00_225a7f20](https://github.com/user-attachments/assets/dd82dd61-4c85-4d43-bb23-d0ed028d39ff)
![Imagem do WhatsApp de 2024-11-11 à(s) 15 24 01_4b3587f4](https://github.com/user-attachments/assets/92529d95-b19b-45a0-aba2-668d92a0e51c)

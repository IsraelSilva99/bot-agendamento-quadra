import telebot
import sqlite3
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from datetime import date, datetime
import config  # Importa o token do arquivo config.py
from fpdf import FPDF

# Configuração do bot e do banco de dados
bot = telebot.TeleBot(config.TOKEN)

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('agendamentos.db', check_same_thread=False)
cursor = conn.cursor()

# Criação da tabela de reservas, caso não exista
cursor.execute('''CREATE TABLE IF NOT EXISTS reservas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data TEXT NOT NULL,
                    hora TEXT NOT NULL,
                    usuario TEXT NOT NULL,
                    status TEXT NOT NULL
                )''')
conn.commit()

# Função para listar os horários disponíveis em uma data


def horarios_disponiveis(data):
    # Verifica no banco de dados os horários já ocupados na data escolhida
    cursor.execute(
        "SELECT hora FROM reservas WHERE data = ? AND status = 'confirmado'", (data,))
    horarios_ocupados = {row[0] for row in cursor.fetchall()}

    # Lista de horários padrão (que o bot sempre oferece para escolha)
    horarios = ["08:00", "10:00", "13:00", "15:00", "17:00"]

    # Retorna apenas os horários que ainda estão disponíveis
    return [h for h in horarios if h not in horarios_ocupados]

# Função para criar teclado com os horários e botão "Voltar"


def criar_teclado_com_voltar(botoes):
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add(*botoes)
    markup.add(KeyboardButton("Voltar"))
    return markup

# Função para criar teclado com os horários


def criar_teclado(horarios):
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for horario in horarios:
        markup.add(KeyboardButton(horario))
    return markup

# Função de início


@bot.message_handler(commands=['start'])
def start(message):
    # Mensagem de boas-vindas e menu inicial
    texto = "👋 Olá! Seja bem-vindo(a) ao Bot de Agendamento da Quadra! 🎾\n\n"
    texto += "Utilize os botões abaixo para:\n"
    texto += "✅ Agendar sua reserva\n"
    texto += "❌ Desmarcar sua reserva\n"
    texto += "📝 Editar sua reserva\n"
    texto += "❓ Acessar a ajuda"
    bot.send_message(message.chat.id, texto, reply_markup=criar_teclado_com_voltar(
        ['Agendar', 'Desmarcar', 'Editar', 'Ajuda']))

# Função para agendar reserva


@bot.message_handler(func=lambda m: m.text == 'Agendar')
def agendar(message):
    # Solicita ao usuário a data para o agendamento
    msg = bot.send_message(
        message.chat.id, "📆 Digite a data para o agendamento, exemplo: 22/05")
    bot.register_next_step_handler(msg, confirmar_data)

# Função para confirmar a data do agendamento e prosseguir para a escolha do horário


def confirmar_data(message):
    data = message.text.strip()

    # Valida o formato da data (dd/mm)
    try:
        dia, mes = map(int, data.split('/'))
        if not (1 <= dia <= 31 and 1 <= mes <= 12):
            raise ValueError
    except ValueError:
        msg = bot.send_message(
            message.chat.id, "Formato de data inválido. Por favor, insira no formato correto (dd/mm).")
        bot.register_next_step_handler(msg, confirmar_data)
        return

    # Valida se a data é válida
    try:
        # Verifica se a data é válida
        datetime.strptime(f"{dia}/{mes}/2023", "%d/%m/%Y")
    except ValueError:
        msg = bot.send_message(
            message.chat.id, "Data inválida. Por favor, insira uma data válida.")
        bot.register_next_step_handler(msg, confirmar_data)
        return

    # Lista os horários disponíveis para a data escolhida
    disponiveis = horarios_disponiveis(data)
    if disponiveis:
        # Envia a lista de horários disponíveis ao usuário
        msg = bot.send_message(
            message.chat.id, "🕒 Escolha um horário:", reply_markup=criar_teclado(disponiveis))
        bot.register_next_step_handler(msg, confirmar_horario, data)
    else:
        bot.send_message(
            message.chat.id, "❌ Não há horários disponíveis para esta data. Tente outra data.")

# Função para confirmar o horário escolhido


def confirmar_horario(message, data):
    horario = message.text.strip()
    disponiveis = horarios_disponiveis(data)

    # Verifica se o horário está disponível
    if horario not in disponiveis:
        bot.send_message(
            message.chat.id, "❌ Esse horário não está disponível. Tente outro horário.")
        return

    # Insere a reserva no banco de dados
    cursor.execute("INSERT INTO reservas (data, hora, usuario, status) VALUES (?, ?, ?, ?)",
                   (data, horario, message.from_user.username, 'confirmado'))
    conn.commit()

    # Obtem o ID da reserva recém-inserida
    cursor.execute("SELECT last_insert_rowid()")
    id_reserva = cursor.fetchone()[0]

    # Envia a mensagem de confirmação com o ID da reserva
    bot.send_message(message.chat.id, f"✔ Reserva confirmada para o dia {data} às {horario}. Seu número de reserva é {
                     id_reserva}.", reply_markup=criar_teclado_com_voltar(['Agendar', 'Desmarcar', 'Editar', 'Ajuda']))

# Função para desmarcar reserva


@bot.message_handler(func=lambda m: m.text == 'Desmarcar')
def desmarcar(message):
    bot.send_message(
        message.chat.id, "Digite o número da reserva que você deseja cancelar:")
    bot.register_next_step_handler(message, confirmar_desmarcar)

# Função para confirmar o cancelamento da reserva


def confirmar_desmarcar(message):
    try:
        id_reserva = int(message.text)
        cursor.execute("DELETE FROM reservas WHERE id = ?",
                       (id_reserva,))  # Deleta a reserva
        conn.commit()
        bot.send_message(message.chat.id, f"Reserva {id_reserva} cancelada com sucesso.", reply_markup=criar_teclado_com_voltar(
            ['Agendar', 'Desmarcar', 'Editar', 'Ajuda']))
    except ValueError:
        bot.send_message(message.chat.id, "Formato inválido. Por favor, insira um número válido.",
                         reply_markup=criar_teclado_com_voltar(['Agendar', 'Desmarcar', 'Editar', 'Ajuda']))

# Função para editar reserva


@bot.message_handler(func=lambda m: m.text == 'Editar')
def editar(message):
    bot.send_message(
        message.chat.id, "Digite o número da reserva que você deseja editar:")
    bot.register_next_step_handler(message, confirmar_editar)

# Função para confirmar a edição da reserva


def confirmar_editar(message):
    try:
        id_reserva = int(message.text)
        cursor.execute(
            "SELECT data, hora FROM reservas WHERE id = ?", (id_reserva,))
        reserva = cursor.fetchone()

        if reserva:
            data, hora = reserva
            texto = f"Reserva {id_reserva}:\nData: {data}, Horário: {hora}\n"
            texto += "O que você deseja editar?\n"
            texto += "1. Data\n2. Horário\n"
            texto += "Digite o número da opção:"
            bot.send_message(message.chat.id, texto)
            bot.register_next_step_handler(
                message, confirmar_opcao_edicao, id_reserva)
        else:
            bot.send_message(message.chat.id, "Reserva não encontrada.", reply_markup=criar_teclado_com_voltar(
                ['Agendar', 'Desmarcar', 'Editar', 'Ajuda']))
    except ValueError:
        bot.send_message(message.chat.id, "Formato inválido. Por favor, insira um número válido.",
                         reply_markup=criar_teclado_com_voltar(['Agendar', 'Desmarcar', 'Editar', 'Ajuda']))

# Função para confirmar a opção de edição escolhida


# Função para confirmar a opção de edição escolhida
def confirmar_opcao_edicao(message, id_reserva):
    try:
        opcao = int(message.text)
        if opcao == 1:
            bot.send_message(message.chat.id, "Digite a nova data (dd/mm):",
                             reply_markup=telebot.types.ReplyKeyboardRemove())
            bot.register_next_step_handler(
                message, confirmar_nova_data, id_reserva)
        elif opcao == 2:
            cursor.execute(
                "SELECT data FROM reservas WHERE id = ?", (id_reserva,))
            data = cursor.fetchone()[0]
            # Obtém os horários disponíveis para a data da reserva
            disponiveis = horarios_disponiveis(data)
            if disponiveis:
                bot.send_message(message.chat.id, "Escolha o novo horário:",
                                 reply_markup=criar_teclado(disponiveis))
                bot.register_next_step_handler(
                    message, confirmar_novo_horario, id_reserva, data)
            else:
                bot.send_message(
                    message.chat.id, "Não há horários disponíveis para esta data. Tente editar a data primeiro.")
        else:
            bot.send_message(message.chat.id, "Opção inválida.", reply_markup=criar_teclado_com_voltar(
                ['Agendar', 'Desmarcar', 'Editar', 'Ajuda']))
    except ValueError:
        bot.send_message(message.chat.id, "Opção inválida. Por favor, insira um número válido.",
                         reply_markup=criar_teclado_com_voltar(['Agendar', 'Desmarcar', 'Editar', 'Ajuda']))

# Função para confirmar o novo horário da reserva


def confirmar_novo_horario(message, id_reserva, data):
    horario = message.text.strip()

    # Verifica se o horário já está reservado
    cursor.execute("SELECT * FROM reservas WHERE data = ? AND hora = ? AND id != ?",
                   (data, horario, id_reserva))
    if cursor.fetchone():
        bot.send_message(
            message.chat.id, "Este horário já está reservado. Por favor, escolha outro horário.")
        bot.register_next_step_handler(
            message, confirmar_novo_horario, id_reserva, data)
        return

    # Atualiza o horário da reserva
    cursor.execute("UPDATE reservas SET hora = ? WHERE id = ?",
                   (horario, id_reserva))
    conn.commit()
    bot.send_message(message.chat.id, f"Horário da reserva {id_reserva} atualizado para {
                     horario}.", reply_markup=criar_teclado_com_voltar(['Agendar', 'Desmarcar', 'Editar', 'Ajuda']))

# Função para confirmar a nova data da reserva


def confirmar_nova_data(message, id_reserva):
    data = message.text.strip()
    try:
        dia, mes = map(int, data.split('/'))
        if not (1 <= dia <= 31 and 1 <= mes <= 12):
            raise ValueError
        datetime.strptime(f"{dia}/{mes}/2023", "%d/%m/%Y")
    except ValueError:
        bot.send_message(
            message.chat.id, "Formato de data inválido. Por favor, insira no formato correto (dd/mm).")
        bot.register_next_step_handler(
            message, confirmar_nova_data, id_reserva)
        return

    cursor.execute("UPDATE reservas SET data = ? WHERE id = ?",
                   (data, id_reserva))
    conn.commit()
    bot.send_message(message.chat.id, f"Data da reserva {id_reserva} atualizada para {
                     data}.", reply_markup=criar_teclado_com_voltar(['Agendar', 'Desmarcar', 'Editar', 'Ajuda']))

# Função para confirmar o novo horário da reserva


def confirmar_novo_horario(message, id_reserva, data):
    horario = message.text.strip()

    # Verifica se o horário é válido
    try:
        datetime.strptime(horario, "%H:%M")
    except ValueError:
        bot.send_message(
            message.chat.id, "Formato de horário inválido. Por favor, insira no formato correto (HH:MM).")
        bot.register_next_step_handler(
            message, confirmar_novo_horario, id_reserva, data)
        return

    # Verifica se o horário existe na lista de horários predefinidos
    horarios_padrao = ["08:00", "10:00", "13:00", "15:00", "17:00"]
    if horario not in horarios_padrao:
        bot.send_message(
            message.chat.id, "Horário inválido. Por favor, escolha um horário disponível.")
        bot.register_next_step_handler(
            message, confirmar_novo_horario, id_reserva, data)
        return

    # Verifica se o horário já está reservado
    cursor.execute("SELECT * FROM reservas WHERE data = ? AND hora = ? AND id != ?",
                   (data, horario, id_reserva))
    if cursor.fetchone():
        bot.send_message(
            message.chat.id, "Este horário já está reservado. Por favor, escolha outro horário.")
        bot.register_next_step_handler(
            message, confirmar_novo_horario, id_reserva, data)
        return

    # Atualiza o horário da reserva
    cursor.execute("UPDATE reservas SET hora = ? WHERE id = ?",
                   (horario, id_reserva))
    conn.commit()
    bot.send_message(message.chat.id, f"Horário da reserva {id_reserva} atualizado para {
                     horario}.", reply_markup=criar_teclado_com_voltar(['Agendar', 'Desmarcar', 'Editar', 'Ajuda']))

# Função de ajuda


@bot.message_handler(func=lambda m: m.text == 'Ajuda')
def ajuda(message):
    texto = "Comandos disponíveis:\n"
    texto += "/start - Iniciar o bot\n"
    texto += "/agendar - Agendar uma reserva\n"
    texto += "/desmarcar - Desmarcar uma reserva\n"
    texto += "/editar - Editar uma reserva\n"
    bot.send_message(message.chat.id, texto, reply_markup=criar_teclado_com_voltar(
        ['Agendar', 'Desmarcar', 'Editar', 'Ajuda']))

# Função para voltar para o menu inicial


@bot.message_handler(func=lambda m: m.text == 'Voltar')
def voltar(message):
    bot.send_message(message.chat.id, "Voltando ao menu inicial...",
                     reply_markup=criar_teclado_com_voltar(['Agendar', 'Desmarcar', 'Editar', 'Ajuda']))


# Função para gerar relatório de agendamentos
def gerar_relatorio():
    # Criar um objeto PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)

    # Adicionar o título do relatório
    pdf.cell(0, 10, "Relatório de Agendamentos", 0, 1, 'C')
    pdf.ln(5)

    # Obter os dados do banco de dados
    cursor.execute("SELECT id, data, hora, usuario, status FROM reservas")
    reservas = cursor.fetchall()

    # Adicionar os dados do relatório no PDF
    pdf.set_font('Arial', '', 10)
    pdf.cell(20, 10, "ID", 1, 0, 'L')  # Adiciona a coluna "ID"
    pdf.cell(40, 10, "Data", 1, 0, 'L')
    pdf.cell(40, 10, "Hora", 1, 0, 'L')
    pdf.cell(60, 10, "Usuário", 1, 0, 'L')
    pdf.cell(40, 10, "Status", 1, 1, 'L')
    for id_reserva, data, hora, usuario, status in reservas:
        pdf.cell(20, 10, str(id_reserva), 1, 0, 'L')  # Inclui o ID da reserva
        pdf.cell(40, 10, data, 1, 0, 'L')
        pdf.cell(40, 10, hora, 1, 0, 'L')
        pdf.cell(60, 10, usuario, 1, 0, 'L')
        pdf.cell(40, 10, status, 1, 1, 'L')

    # Salvar o PDF
    pdf.output("relatorio_agendamentos.pdf")

    # Retorna o nome do arquivo PDF
    return "relatorio_agendamentos.pdf"

# Função para gerar relatório de agendamentos


@bot.message_handler(commands=['relatorio'])
def relatorio(message):
    if message.from_user.username == 'RaaelSilva':
        nome_arquivo = gerar_relatorio()
        bot.send_document(message.chat.id, open(nome_arquivo, 'rb'))
    else:
        bot.send_message(
            message.chat.id, "Você não tem permissão para gerar este relatório.")


# Iniciar o bot
bot.polling()

from datetime import date, timedelta
from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from gcsa.recurrence import Recurrence, DAILY, SU, SA, YEARLY

session = ""
continue_condition = False
while not continue_condition:
    print("Please, type today's studied session title. E.g: FIAP 3SIOA F3C7:")
    session = input()
    print(f"{session}. Would you like to continue? (y/n)")
    continue_ans = input()
    if continue_ans.lower() == 'n':
        pass
    else:
        continue_condition = True

calendar = GoogleCalendar('vcavalcanteab@gmail.com')
today = date.today()

# subject creation
event = Event(summary=f"Notes & Summary - {session}",
              start=today,
              color_id='2')
calendar.add_event(event)
print("Creating Notes & Summary event...")

# anki creation
event = Event(summary=f"Exercises APT - {session}",
              start=today,
              color_id='7',
              description="Crie cards Anki sobre suas anotações, e sobre seu resumo (com GPT).\n\n"
                          "Crie questões práticas e teóricas com GPT. Adicione questões já vistas.\n\n"
                          "Exemplo de questão GPT para o Anki: \n\n"
                          "Oi, chat! Eu preciso criar flashcards no Anki sobre o conteúdo do resumo/documento"
                          " em anexo. Por favor, extraia as informações principais e crie perguntas e respostas"
                          " práticas e objetivas para cada tópico abordado."
                          " Organize os flashcards da seguinte maneira:\n"
                          "- Pergunta: A pergunta deve ser clara e direta, focando em conceitos importantes, "
                          "definições,"
                          "exemplos, ou detalhes específicos.\n"
                          "- Resposta: A resposta deve ser precisa e objetiva, fornecendo a informação essencial para a"
                          "pergunta.\n"
                          "Aqui está o resumo/documento:\nObrigado!\n\n"
                          "Exemplo de questão GPT teóricas e práticas\n\n"
                          "Oi, Chat! Eu preciso criar questões práticas e teóricas para estudar o conteúdo do "
                          "resumo/documento"
                          " em anexo. Por favor, crie perguntas desafiadoras e variadas para cada tópico abordado."
                          " Organize as questões da seguinte maneira:\n"
                          "- Questões Teóricas: Perguntas que testem o entendimento dos conceitos, definições, "
                          "e teorias.\n"
                          "- Questões Práticas: Perguntas que envolvam a aplicação prática dos conceitos, resolução de "
                          "problemas, e exemplos do mundo real.\n"
                          "Aqui está o resumo/documento: \nObrigado!"
              )
calendar.add_event(event)
print("Creating Exercises APT event...")

# spaced repetition reviews
spaced_repetition_intervals = [1, 7, 16, 35]
review_numbers = [1, 2, 3, 4]
for repetition_interval, review_number in zip(spaced_repetition_intervals, review_numbers):
    print(f"Creating Review APTR {repetition_interval} event...")
    event = Event(summary=f"Review APTR {review_number} - {session}",
                  start=today + timedelta(days=repetition_interval),
                  color_id='7')
    calendar.add_event(event)

# semiannual review sessions after success of spaced_repetition schedule
semiannual_days = [180, 365]
for semiannual_day in semiannual_days:
    print(f"Creating Semmiannual Review APTR {semiannual_day} event...")
    event = Event(
        summary=f"Semiannual Review APTR - {session}",
        start=today + timedelta(days=semiannual_day),
        recurrence=[
            Recurrence.rule(freq=YEARLY),
        ],
        color_id='7'
    )
    calendar.add_event(event)

# save study session into a csv
print("Saving study session...")
with open("study_sessions.csv", "a") as csvfile:
    csvfile.write(f"{today},{session}\n")

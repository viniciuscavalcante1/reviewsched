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
event = Event(summary=f"{session}",
              start=today,
              color_id='2')
calendar.add_event(event)
print("Creating main event...")

# spaced repetition reviews
spaced_repetition_intervals = [1, 3, 7, 16, 35, 90]
review_numbers = [1, 2, 3, 4, 5, 6]
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

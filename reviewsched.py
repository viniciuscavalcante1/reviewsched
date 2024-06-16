from datetime import date, timedelta
from gcsa.event import Event
from gcsa.google_calendar import GoogleCalendar
from gcsa.recurrence import Recurrence, DAILY, SU, SA, YEARLY

session = ""
continue_condition = False
while not continue_condition:
    print("Please, type today's studied session title. E.g: FIAP 3SIOA F3C7\n")
    session = input()
    print(f"Review session to create: {session}. Would you like to continue? (y/n)")
    continue_ans = input()
    if continue_ans.lower() == 'n':
        pass
    else:
        continue_condition = True

calendar = GoogleCalendar('vcavalcanteab@gmail.com')
today = date.today()

# subject creation
event = Event(summary=f"Session {session}",
              start=today,
              color_id='2')
calendar.add_event(event)

# anki creation
event = Event(summary=f"Anki - {session}",
              start=today,
              color_id='7')
calendar.add_event(event)

# exercises
event = Event(summary=f"Exercises - {session}",
              start=today,
              color_id='7')
calendar.add_event(event)

# spaced repetition reviews
spaced_repetition_intervals = [1, 7, 16, 35]
review_numbers = [1, 2, 3, 4]
for repetition_interval, review_number in zip(spaced_repetition_intervals, review_numbers):
    print(f"Creating event for repetition interval {repetition_interval}...")
    event = Event(summary=f"Review {review_number} - {session}",
                  start=today + timedelta(days=repetition_interval),
                  color_id='7')
    calendar.add_event(event)

# semiannual review sessions after success of spaced_repetition schedule
print("Creating recurrent event for semiannual repetition intervals...")
semiannual_days = [180, 365]
for semiannual_day in semiannual_days:
    print(f"Creating event for semiannual repetition interval - {semiannual_day}...")
    event = Event(
        summary=f"Semiannual Review - {session}",
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

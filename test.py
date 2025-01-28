from app.database.requests import get_work_hours
import tracemalloc

# get_work_hours(536212014, 'today')
tracemalloc.start()

# Your existing code
get_work_hours(536212014, 'today')

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

print("[ Top 10 ]")
for stat in top_stats[:10]:
    print(stat)

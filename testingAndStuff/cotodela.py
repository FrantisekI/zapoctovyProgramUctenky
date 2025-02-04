import unicodedata
from datetime import datetime 
print(unicodedata.normalize('NFKD', input().upper()).encode('ASCII', 'ignore').decode('ASCII'))

print(datetime.strptime('ffdsf', "%d.%m.%Y").date())
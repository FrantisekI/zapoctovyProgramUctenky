import unicodedata
print(unicodedata.normalize('NFKD', input().upper()).encode('ASCII', 'ignore').decode('ASCII'))
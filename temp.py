from api.hashing.records import HashRecords
from api.hashing.utils import digest

print(digest('abcd'))
print(list(digest(['abcd', 'efgh'])))

records = HashRecords()

print(records._HashRecords__records)

print('abcd' not in records)
print('abcd' in records)

records['abcd'] = 'abcd'
records['efgh'] = 'efgh'

for key in ['pqrs', 'efgh'] - records:
    print(key)


records[['a', 'b']] = ['cd', 'xy']

print(records._HashRecords__records)

del records['abcd']

print(records._HashRecords__records)

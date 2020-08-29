# import csv
#
# l = ['Victoria', 'New South Wales', 'Queensland', 'South Australia', 'Tasmania', 'Western Australia',
#      'Australian Capital Territory', 'Northern Territory']
# cl = []
# uk = []
#
# with open('config_files/world-cities.csv', 'r') as inp1:
#     for row in csv.reader(inp1):
#         l.append(row[0])
#
#
# def remove2():
#     while True:
#         with open('config_files/uk-cities_csv.csv', 'r') as inp3:
#             for row in csv.reader(inp3):
#                 uk.append(row[0])
#         for q in uk:
#             for p in l:
#                 if q.strip().replace(' ', '').upper() == p.strip().replace(' ', '').upper():
#                     l.remove(p)
#         inp3.close()
#         return False
#
#
# remove2()
#
# with open('config_files/location_id.csv', 'r') as inp2:
#     for row in csv.reader(inp2):
#         cl.append(row)
#
# inp1.close()
# inp2.close()
#
#
# # inp4.close()
#
#
# def remove():
#     while True:
#         for p in l:
#             for q in cl:
#                 if p.strip().replace(' ', '').upper() == q[2].strip().replace(' ', '').upper() and \
#                         p.strip().upper() != 'NAME':
#                     print(p, q)
#                     cl.remove(q)
#                 elif q[0] == '' or None:
#                     cl.remove(q)
#         return False
#
#
# remove()
#
# with open('config_files/location_id2.csv', 'w') as out:
#     writer = csv.writer(out)
#     for item in cl:
#         writer.writerow(item)
#     cl = []
# out.close()
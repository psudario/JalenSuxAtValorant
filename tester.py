my_dict = {}
manufacturer_lists = []
price_lists = []
service_dates_list = []
types = set()

# Reading from input files and storing values in a lists
with open('ManufacturerList3.csv', 'r') as my_file:
    line = my_file.readline()
    while line:
        manufacturer_lists.append(line[0:-2])
        line = my_file.readline()

with open('PriceList1.csv', 'r') as my_file:
    line = my_file.readline()
    while line:
        price_lists.append(line[0:-1])
        line = my_file.readline()

with open('ServiceDatesList3.csv', 'r') as my_file:
    line = my_file.readline()
    while line:
        service_dates_list.append(line[0:-1])
        line = my_file.readline()


# Formatting the data in lists into a dictionary
for entry in manufacturer_lists:
    line = entry.split(',')

    if len(line) < 4:
        my_dict[int(line[0])] = (line[1].strip(), line[2].strip())
    else:
        my_dict[int(line[0])] = (line[1].strip(), line[2].strip(), 'damaged')

for entry in price_lists:
    line = entry.split(',')     #Split lines based off of commas
    id_values = list(my_dict[int(line[0])])     #Search for id in dictionary
    id_values.append(int(line[1]))  #Append price to values of the id
    my_dict[int(line[0])] = tuple(id_values)

for entry in service_dates_list:
    line = entry.split(',')     #Split lines based off of commas
    id_values = list(my_dict[int(line[0])])     #Search for id in dictionary
    id_values.append(line[1])  #Append price to values of the id
    my_dict[int(line[0])] = tuple(id_values)


for key, value in my_dict.items(): #Find the different types of things 
    types.add(value[1])



'''
===============
   vvv Output Things vvv
===============
'''

# Part a output
with open('FullInventory.csv', 'w') as my_file:
    for key, values in my_dict.items():
        line = str(key)
        damaged = 'damaged' in values   #checks if item is damaged
        for value in values:            #add to line in csv
            if not value == 'damaged':
                line += ', ' + str(value)
        if damaged:                     #if the item is damaged, append it to the end of the line
            line += ', damaged'
        my_file.write(line + ',\n')

# Part b ouput
for type in types:
    filename = type + 'Inventory.csv'
    filename = filename[0].upper() + filename[1:]

    output_lines = []
    for key, values in my_dict.items(): 
        type_line = []
        if values[1] == type:
            line = str(key)
            damaged = 'damaged' in values   #checks if item is damaged
            for value in values:            #add to line in csv
                if not value == 'damaged' and not value == type:
                    line += ', ' + str(value)
                type_line.append(line)
            if damaged:                     #if the item is damaged, append it to the end of the line
                line += ', damaged'
            output_lines.append(line)
    output_lines.sort(key = lambda x : int(x[0:x.find(',')]))   #Sorts based off of id

    with open(filename, 'w') as my_file:
        for output_line in output_lines:
            my_file.write(output_line+',\n')


# Part c output
from datetime import datetime as date
outdated = []

for key, values in my_dict.items():
    month, day, year = tuple(values[-1].split('/'))
    month, day, year, = int(month), int(day), int(year)

    if(date(year, month, day)) < date.now():
        line = str(key)
        damaged = 'damaged' in values   #checks if item is damaged
        for value in values:            #add to line in csv
            if not value == 'damaged':
                line += ', ' + str(value)
        if damaged:                     #if the item is damaged, append it to the end of the line
            line += ', damaged'    
        outdated.append(line)

def return_date_object(entry):                                  #Function to return date given a csv line entry
    index = -2 if entry.split(',')[-1].strip() == 'damaged' else -1

    month, day, year = tuple(entry.split(',')[index].split('/'))
    month, day, year, = int(month), int(day), int(year)
    return date(year, month, day)

outdated.sort(key = lambda x : return_date_object(x))           #Sort list in order of ascending dates

with open('PastServiceDateInventory.csv', 'w') as my_file:
    for line in outdated:
        my_file.write(line + ',\n')
    

# Part d
damaged_items = []
for key, values in my_dict.items():
    # price is values[-2]
    if 'damaged' in values:
        line = [key]
        for value in values:
            if value != 'damaged':
                line.append(value)
        damaged_items.append(line)
damaged_items.sort(key = lambda x : x[-2], reverse=True)

with open('DamagedInventory.csv', 'w') as my_file:
    for damaged_item in damaged_items:
        line = ''
        for item in damaged_item:
            line += str(item) + ','
        my_file.write(line + '\n')

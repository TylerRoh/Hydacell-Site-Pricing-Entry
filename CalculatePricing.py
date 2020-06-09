import csv

files = ['D04-G04.csv', 'D10-G10.csv', 'D12-G12.csv', 'D15-D17.csv', 'D35-G35.csv', 'D66-G66.csv',
         'F20-G20.csv', 'H25-G25.csv', 'M03-D03.csv', 'Mono-Block.csv']

pricing_list = []
for file in files:
    f = open('S:\\Tyler\\Hydra Cell Pump Pricing\\Price Sheets\\' + file, 'r')

    price_list = list(csv.reader(f))
    pricing_list.append(price_list)



def price_calculation(part, pricing_list):
    count = 0

    #This list is beacuse the MonoBlock csv is the same first 4 values as the M03-D03 one
    MonoList = ["D03", 'M03', 'G03', 'G13']

    needed_sections = []
    for section in pricing_list:
        for line in section:
            if line[0] == '3':
                if part[0:3] == line[1]:
                    needed_sections.append(section)
                    break

    if len(needed_sections) > 1:
        if part[4] == 'M':
            del needed_sections[0]
        else:
            del needed_sections[1]

    price = 0
    for line in needed_sections[0]:
        if part[0:3] in line:
            price = price + int(line[2].replace(',',''))
            count += 3
            break
    if count < 3:
        print(f"Error: Could not find match for first 3 digits of part number {part}")
    for letter in  part[3:]:
        for line in needed_sections[0]:
            if letter in line:
                if int(line[0]) == count + 1:
                    price = price + int(line[2].replace(',', '').replace('(', '').replace(')', ''))
                    count += 1
                    break

    if count != 12:
        print(part)
        print(f"Error: Only took in {count} digits for pricing. (Should be 12)")

    return price




site_file = r'S:\Tyler\Hydra Cell Pump Pricing\To Be Priced\pricing.csv'

f = open(site_file, 'r')

site_list = list(csv.reader(f))

columns = (site_list[0].index('SKU'), site_list[0].index('Regular price'))
for line in site_list[1:]:

    line[columns[1]] = price_calculation(line[columns[0]], pricing_list)
    print(f'{line[2]} price entered as ${line[25]}.\n')

f = open(site_file, 'w', newline='')
f = csv.writer(f)
f.writerows(site_list)
print("Process Completed.")
input("Press Enter to exit.")
import csv


def main():
    with open("db_1.csv") as db:
        csv_reader = csv.reader(db)
        attrs = next(csv_reader)
        attrs.remove(attrs[-1])
        power_dict = construct_dict(attrs)
        fill_dict(power_dict, attrs, csv_reader)
        pprint(power_dict)


def construct_dict(attrs):
    power_dict = {}
    n = len(attrs)
    for i in range(1, 1 << n):
        s = ','.join([attrs[j] for j in range(n) if (i & (1 << j))])
        power_dict[s] = {}
    return power_dict


def fill_dict(power_dict, attrs, reader):
    for row in reader:
        item = {}
        item_label = row[-1]

        for i in range(len(row) - 1):
            item[attrs[i]] = row[i]

        for s in power_dict.keys():
            ls = s.split(',')
            kmer = ""
            for attr in ls:
                kmer += item[attr] + ','
            kmer = kmer[:-1]

            if kmer in power_dict[s].keys():
                power_dict[s][kmer][0] += 1
                if item_label in power_dict[s][kmer][1].keys():
                    power_dict[s][kmer][1][item_label] += 1
                else:
                    power_dict[s][kmer][1][item_label] = 1
            else:
                power_dict[s][kmer] = [1, {item_label: 1}]


def pprint(d):
    for key in d.keys():
        print(f'{key}:')
        for kkey in d[key]:
            print(f'\t{kkey}: {d[key][kkey][0]}')
            print(f'\t\t{d[key][kkey][1]}')


main()

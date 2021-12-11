import csv


def main():
    with open("obesity_db.csv") as db:
        csv_reader = csv.reader(db)
        attrs = next(csv_reader)
        power_dict = construct_dict(attrs)
        fill_dict(power_dict, attrs, csv_reader)
        print(power_dict)


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

        for i in range(len(row)):
            item[attrs[i]] = row[i]

        for s in power_dict.keys():
            ls = s.split(',')
            kmer = ""
            for attr in ls:
                kmer += item[attr] + ','
            kmer = kmer[:-1]

            if kmer in power_dict[s].keys():
                power_dict[s][kmer] += 1
            else:
                power_dict[s][kmer] = 1


main()

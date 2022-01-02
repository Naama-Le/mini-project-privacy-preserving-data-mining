import csv


class DB:
    def __init__(self, idx):
        self.idx = idx
        self.dict = {}
        self.process_db()

    def process_db(self):
        with open(f"db_{self.idx}.csv") as db:
            csv_reader = csv.reader(db)
            attrs = next(csv_reader)
            attrs.remove(attrs[-1])
            self.__construct_dict(attrs)
            self.__fill_dict(attrs, csv_reader)

    def __construct_dict(self, attrs):
        n = len(attrs)
        for i in range(1, 1 << n):
            s = [attrs[j] for j in range(n) if (i & (1 << j))]
            s.sort()
            self.dict[','.join(s)] = {}

    def __fill_dict(self, attrs, reader):
        for row in reader:
            item = {}
            item_label = row[-1]

            for i in range(len(row) - 1):
                item[attrs[i]] = row[i]

            for s in self.dict.keys():
                ls = s.split(',')
                kmer = ""
                for attr in ls:
                    kmer += item[attr] + ','
                kmer = kmer[:-1]

                if kmer in self.dict[s].keys():
                    self.dict[s][kmer][0] += 1
                    if item_label in self.dict[s][kmer][1].keys():
                        self.dict[s][kmer][1][item_label] += 1
                    else:
                        self.dict[s][kmer][1][item_label] = 1
                else:
                    self.dict[s][kmer] = [1, {item_label: 1}]

    def __getitem__(self, item):
        return self.dict[item]

    def __str__(self):
        s = []
        for key in self.dict.keys():
            s.append(f'{key}:')
            for _key in self.dict[key]:
                s.append(f'\t{_key}: {self.dict[key][_key][0]}\n\t\t{self.dict[key][_key][1]}\n')
            s.append('\n')
        return ''.join(s)
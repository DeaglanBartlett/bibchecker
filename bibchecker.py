import numpy as np
            
class bibentry:
    
    def __init__(self, entry):
        self.name = None
        self.arxiv = None
        self.doi = None
        self.volume = None
        self.number = None
        self.page = None
    
        for x in entry:
            if x.startswith('@'):
                self.name = x[x.index('{')+1:x.index(',')]
            else:
                for s in ['eprint', 'doi', 'volume', 'number', 'pages']:
                    if x.startswith(s):
                        y = x.replace('{', '')
                        y = y.replace('}', '')
                        y = y.replace('"', '')
                        for i, c in enumerate(y):
                            if c.isdigit():
                                break
                        y = y[i:]
                        if ',' in y:
                            y = y[:y.index(',')]
                            
                        if (s == 'pages') and ('-' in y):
                            y = y[:y.index('-')]
                            
                        if s == 'doi':
                            self.doi = y
                        else:
                            try:
                                z = float(y)  # only entries which are numbers
                            except:
                                y = None
                            if s == 'eprint':
                                self.arxiv = y
                            elif s == 'volume':
                                self.volume = y
                            elif s == 'number':
                                self.number = y
                            elif s == 'pages':
                                self.page = y
                                
fname = 'references.bib'
all_entries = []

with open(fname, "r") as f:
    entry = []
    for line in f:
        x = line.lstrip()
        x = x.lstrip('_')
        if line.startswith('@'):
            all_entries.append(entry)
            entry = [x]
        elif line != '':
            entry.append(x)
                
                    
all_entries = all_entries[1:]
arr = [bibentry(entry) for entry in all_entries]

names = np.array([a.name for a in arr], dtype=str)
arxiv = np.array([a.arxiv for a in arr], dtype=str)
doi = np.array([a.doi for a in arr], dtype=str)
pages = np.array([a.page for a in arr], dtype=str)

arrays = [names, arxiv, doi]
labels = ['names', 'arxiv', 'doi']

# Find repeats
for a in range(len(arrays)):
    arr = arrays[a]
    print('\nRepeats by %s'%labels[a])
    unique, idx, counts = np.unique(names, return_index=True, return_counts=True)
    for i in range(len(counts)):
        if counts[i] == 1:
            pass
        elif unique[i] == str(None):
            pass
        else:
            x = names[names == unique[i]]
            print(x)

# Show entries which only have arXiv numbers or no journal
m = [i for i, d in enumerate(doi) if ('arXiv' in d) or (d == 'None' and 'arXiv' in pages[i])]
print(f'\narXiv only or no journal (total = {len(m)}):')
for i in m:
    print(names[i], arxiv[i])


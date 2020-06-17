from Bio.PDB import *


class ChainSelect(Select):
    def __init__(self, complex):
        super().__init__()
        self._complex = complex
    def accept_chain(self, chain):
        if chain.id in self._complex:
            return 1
        else:
            return 0


def split_into_class_i_complexes(pdb_filename, pdb_code, temp_directory):
    chain_set = {
        'alpha': [],
        'beta2m': [],
        'peptide': [],
    }

    complex_set = []
    ignore = False


    parser = PDBParser(PERMISSIVE=1)
    structure = parser.get_structure('mhc', pdb_filename)

    chains = [chain.id for chain in structure.get_chains()]

    if len(chains) % 3 == 0:
        chain_names = ['alpha', 'beta2m', 'peptide']
    elif len(chains) % 2 == 0:
        chain_names = ['alpha', 'beta2m']
    else:
        ignore = True
        error = 'Not just a class I peptide complex'

    if not ignore:
        i = 1
        j = 0

        for model in structure:
            for chain in model:
                i += 1
                chain_set[chain_names[j]].append(chain)
                if j == len(chain_names) - 1:
                    j = 0
                else:
                    j += 1


        molecule_count = len(chain_set['alpha'])

        k = 0
        while k < molecule_count:
            complex_chains = []
            for chain_name in chain_names:
                complex_chains.append(chain_set[chain_name][k].id)
            complex_set.append(complex_chains)
            k += 1

        l = 1
        for complex in complex_set:
            io = PDBIO()
            io.set_structure(model)
            filename = temp_directory + '/' + pdb_code + '_' + str(l) + '.pdb'
            io.save(filename, ChainSelect(complex))
            l += 1
        return complex_set

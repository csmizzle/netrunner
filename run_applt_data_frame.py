import netrunner as nr
nf_new = nr.read_csv('./data/character-deaths.csv',
                     nodes=['Name', 'Allegiances'],
                     links=[('Name', 'Allegiances')])
nf_new.frame['Allegiances'] = nf_new.frame['Allegiances'].str.lower()
nf_new.frame['Name'] = nf_new.frame['Name'].str.lower()
nf_new.apply_dataframe()
for node in nf_new.net.nodes:
    assert node.islower()


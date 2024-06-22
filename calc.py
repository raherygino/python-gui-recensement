def calculer_rang(notes):
    # Créer une liste de tuples (note, index)
    indexed_notes = [(note, index) for index, note in enumerate(notes)]
    
    # Trier les notes en fonction de la valeur de note (ordre décroissant)
    indexed_notes.sort(key=lambda x: x[0], reverse=True)
    
    # Initialisation des variables
    rang = 1
    rangs = [0] * len(notes)
    current_rank = 1
    tie_count = 0
    
    # Attribution des rangs en gérant les ex-aequo
    for i in range(len(indexed_notes)):
        if i > 0 and indexed_notes[i][0] < indexed_notes[i - 1][0]:
            rang += tie_count
            current_rank += tie_count
            tie_count = 0
        
        tie_count += 1
        rangs[indexed_notes[i][1]] = current_rank
    
    return rangs

# Exemple d'utilisation
notes = [85, 75, 90, 75, 72, 73, 80]
rangs = calculer_rang(notes)
for i in range(len(notes)):
    print(f"Note : {notes[i]} | Rang : {rangs[i]}")

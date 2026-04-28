# chargeur.py
# Chargement d'une machine de Turing au format turingmachinesimulator.com

from mt_structures import MT, Transition, Configuration


def charger_machine_depuis_fichier(chemin_fichier):
    """
    Lit un fichier .tm et construit un objet MT.
    Format attendu :
      init: I
      accept: F

      I,1
      X,R,>
      ...
    """

    with open(chemin_fichier, "r", encoding="utf-8") as f:
        lignes = []
        for ligne in f:
            # On enlève les espaces en début/fin
            ligne = ligne.strip()

            # On ignore les lignes vides
            if ligne == "":
                continue

            # On ignore les commentaires (// ou #)
            if ligne.startswith("//") or ligne.startswith("#"):
                continue
            
            print("LIGNE LUE :", ligne)

            # On garde la ligne utile
            lignes.append(ligne)

    # Ensembles pour construire la machine
    etats = set()
    alphabet_entree = set()   # pas vraiment utilisé ici, mais on le garde
    alphabet_ruban = set()
    transitions = {}
    blanc = "_"               # convention : symbole blanc

    etat_initial = None
    etat_final = None

    i = 0
    while i < len(lignes):
        ligne = lignes[i]

        # Ligne de l'état initial : "init: I"
        if ligne.startswith("init:"):
            etat_initial = ligne.split(":")[1].strip()
            etats.add(etat_initial)
            i += 1
            continue

        # Ligne de l'état final : "accept: F"
        if ligne.startswith("accept:"):
            etat_final = ligne.split(":")[1].strip()
            etats.add(etat_final)
            i += 1
            continue

        # LIGNE 1 D'UNE TRANSITION : doit contenir exactement 1 virgule
        # Exemple : "I,1"
        if ligne.count(",") == 1:
            etat_courant, symbole_lu = ligne.split(",")
            etat_courant = etat_courant.strip()
            symbole_lu = symbole_lu.strip()

            etats.add(etat_courant)
            alphabet_ruban.add(symbole_lu)

            # On lit la LIGNE 2 : doit contenir exactement 2 virgules
            # Exemple : "X,R,>"
            i += 1
            ligne2 = lignes[i]

            if ligne2.count(",") != 2:
                raise ValueError("Transition mal formée : " + ligne2)

            nouvel_etat, symbole_ecrit, mouvement = ligne2.split(",")
            nouvel_etat = nouvel_etat.strip()
            symbole_ecrit = symbole_ecrit.strip()
            mouvement = mouvement.strip()

            etats.add(nouvel_etat)
            alphabet_ruban.add(symbole_ecrit)

            # Conversion du mouvement en L/R/S
            if mouvement == "<":
                mouvement = "L"
            elif mouvement == ">":
                mouvement = "R"
            else:
                mouvement = "S"

            # Construction de l'objet Transition (1 seul ruban)
            transition = Transition(
                nouvel_etat,
                [symbole_ecrit],
                [mouvement]
            )

            # Ajout dans le dictionnaire des transitions
            # Clé : (état_courant, (symbole_lu,))
            transitions[(etat_courant, (symbole_lu,))] = transition

        # On passe à la ligne suivante
        i += 1

    # Construction de la machine de Turing
    machine = MT(
        list(etats),
        list(alphabet_entree),
        list(alphabet_ruban),
        blanc,
        etat_initial,
        etat_final,
        1,              # un seul ruban
        transitions
    )

    return machine


def configuration_initiale(machine, mot):
    """
    Crée la configuration initiale :
    - ruban contenant le mot
    - tête en position 0
    - état = état initial
    """

    ruban = list(mot)
    if len(ruban) == 0:
        ruban = [machine.blanc]

    return Configuration(
        machine.etat_initial,
        [ruban],   # un seul ruban
        [0]        # tête au début
    )

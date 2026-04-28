# simulateur.py

from mt_structures import Transition, MT, Configuration
from chargeur import configuration_initiale



def faire_un_pas(machine, configuration):
    """
    Exécute un seul pas de calcul de la machine de Turing.
    """

    # Si on est déjà dans l'état final, on ne fait rien
    if configuration.etat == machine.etat_final:
        return None

    # 1. Lire les symboles sous les têtes
    symboles_lus = []
    for index_ruban in range(machine.nb_rubans):
        ruban = configuration.rubans[index_ruban]
        position = configuration.positions_tetes[index_ruban]

        # Si la tête sort du ruban, on ajoute un symbole blanc
        if position < 0:
            ruban.insert(0, machine.blanc)
            position = 0
            configuration.positions_tetes[index_ruban] = 0
        elif position >= len(ruban):
            ruban.append(machine.blanc)

        symboles_lus.append(ruban[position])

    # 2. Chercher la transition correspondante
    cle = (configuration.etat, tuple(symboles_lus))

    if cle not in machine.transitions:
        # Aucune transition → la machine bloque
        return None

    transition = machine.transitions[cle]

    # 3. Appliquer la transition : écrire les symboles
    for i in range(machine.nb_rubans):
        ruban = configuration.rubans[i]
        position = configuration.positions_tetes[i]
        ruban[position] = transition.symboles_ecrits[i]

    # 4. Bouger les 
    for i in range(machine.nb_rubans):
        mouvement = transition.mouvements[i]
        if mouvement == "L":
            configuration.positions_tetes[i] -= 1
        elif mouvement == "R":
            configuration.positions_tetes[i] += 1
        # "S" → ne rien faire

    # 5. Changer d'état
    configuration.etat = transition.nouvel_etat

    return configuration
def simuler(machine, mot, afficher=False):
    """
    Simule la machine de Turing sur un mot d'entrée.
    Si afficher=True, on affiche chaque configuration après chaque pas.

    La simulation s'arrête :
    - quand on atteint l'état final
    - ou quand aucune transition n'est possible (machine bloquée)
    """

    # 1. Création de la configuration initiale
    configuration = configuration_initiale(machine, mot)

    # Si l'utilisateur veut afficher les étapes → on affiche la configuration initiale
    if afficher:
        afficher_configuration(configuration)

    # 2. Boucle principale de simulation
    while True:

        # Si on est dans l'état final → fin du calcul
        if configuration.etat == machine.etat_final:
            return configuration

        # 3. On exécute un pas de calcul
        nouvelle_config = faire_un_pas(machine, configuration)

        # Si aucune transition n'est possible → la machine bloque
        if nouvelle_config is None:
            return configuration

        # Mise à jour de la configuration
        configuration = nouvelle_config

        # Si afficher=True → on affiche la nouvelle configuration
        if afficher:
            afficher_configuration(configuration)


def afficher_configuration(configuration):
    """
    Affiche une configuration de la machine :
    - état courant
    - contenu du ruban
    - position de la tête

    Cette fonction sert uniquement à visualiser ce que fait la machine
    à chaque étape du calcul.
    """

    # On récupère le ruban (ici on suppose qu'il n'y a qu'un seul ruban)
    ruban = configuration.rubans[0]

    # Position de la tête sur ce ruban
    position = configuration.positions_tetes[0]

    # --- Affichage du ruban ---
    # On affiche tous les symboles séparés par des espaces
    print("Ruban :", " ".join(ruban))

    # --- Affichage de la tête ---
    # On affiche des espaces jusqu'à la position de la tête, puis un ^
    # Exemple : si position = 3 → "      ^"
    print("       ", "   " * position + "^")

    # --- Affichage de l'état courant ---
    print("État  :", configuration.etat)

    # Ligne de séparation pour rendre l'affichage plus lisible
    print("----------------------------------")

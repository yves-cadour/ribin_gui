"""Un module de fonctions utilitaires"""


def calculer_separateurs(n: int, d: int) -> list[tuple[int, int]]:
    """
    Calcule les indices de séparation pour répartir n éléments dans d colonnes.
    Exemple:
        calculer_separateurs(10, 3) -> [(0, 4), (4, 7), (7, 10)]
        (éléments 0-3 dans 1ère colonne, 4-6 dans 2ème, 7-9 dans 3ème)
    """
    base, reste = divmod(n, d)
    repartition = [base + (1 if i < reste else 0) for i in range(d)]
    start=0
    separateurs = []
    for nb in repartition:
        end = start+nb
        separateurs.append((start, end))
        start = end
    return separateurs

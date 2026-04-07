import os
import pandas as pd
import matplotlib.pyplot as plt
from math import ceil

# =========================
# CONFIGURATION
# =========================

FICHIER_ENTREE = "simulation.csv"
DOSSIER_SORTIE = "output"

os.makedirs(DOSSIER_SORTIE, exist_ok=True)

# =========================
# CHARGEMENT DES DONNÉES
# =========================

df = pd.read_csv(FICHIER_ENTREE)

# Vérification des colonnes attendues
colonnes_attendues = {"produit", "ventes", "prix", "nouveau_prix"}
colonnes_presentes = set(df.columns)

if not colonnes_attendues.issubset(colonnes_presentes):
    colonnes_manquantes = colonnes_attendues - colonnes_presentes
    raise ValueError(f"Colonnes manquantes dans le CSV : {sorted(colonnes_manquantes)}")

# =========================
# NETTOYAGE DES DONNÉES
# =========================

df["ventes"] = pd.to_numeric(df["ventes"], errors="coerce")
df["prix"] = pd.to_numeric(df["prix"], errors="coerce")
df["nouveau_prix"] = pd.to_numeric(df["nouveau_prix"], errors="coerce")

df = df.dropna(subset=["produit", "ventes", "prix", "nouveau_prix"])

if df.empty:
    raise ValueError("Aucune ligne exploitable après nettoyage des données.")

# =========================
# CALCULS
# =========================

# Chiffres d'affaires
df["revenu_actuel"] = df["ventes"] * df["prix"]
df["revenu_simule"] = df["ventes"] * df["nouveau_prix"]

# Écarts
df["ecart_CA"] = df["revenu_simule"] - df["revenu_actuel"]
df["ecart_pourcentage"] = (df["ecart_CA"] / df["revenu_actuel"]) * 100

# Ventes nécessaires pour conserver le CA actuel avec le nouveau prix
df["ventes_necessaires"] = (df["revenu_actuel"] / df["nouveau_prix"]).apply(ceil)
df["difference_ventes"] = df["ventes_necessaires"] - df["ventes"]

# Arrondis pour lisibilité
df["revenu_actuel"] = df["revenu_actuel"].round(2)
df["revenu_simule"] = df["revenu_simule"].round(2)
df["ecart_CA"] = df["ecart_CA"].round(2)
df["ecart_pourcentage"] = df["ecart_pourcentage"].round(2)

# =========================
# GÉNÉRATION DU RAPPORT
# =========================

blocs = []

for _, ligne in df.iterrows():
    produit = ligne["produit"]
    ventes = int(ligne["ventes"])
    prix = ligne["prix"]
    nouveau_prix = ligne["nouveau_prix"]
    ca_actuel = ligne["revenu_actuel"]
    ca_simule = ligne["revenu_simule"]
    ecart_ca = ligne["ecart_CA"]
    ecart_pct = ligne["ecart_pourcentage"]
    ventes_necessaires = int(ligne["ventes_necessaires"])
    difference_ventes = int(ligne["difference_ventes"])

    if difference_ventes > 0:
        conclusion = (
            f"Pour conserver le même chiffre d'affaires, il faudrait vendre "
            f"{ventes_necessaires} exemplaires, soit {difference_ventes} de plus qu'actuellement."
        )
    elif difference_ventes < 0:
        conclusion = (
            f"Pour conserver le même chiffre d'affaires, il suffirait de vendre "
            f"{ventes_necessaires} exemplaires, soit {-difference_ventes} de moins qu'actuellement."
        )
    else:
        conclusion = (
            "Le nouveau prix permettrait de conserver le même chiffre d'affaires "
            "avec le même volume de ventes."
        )

    bloc = f"""
=== RÉSULTATS DE LA SIMULATION ===

Produit : {produit}

Prix actuel : {prix:.2f} €
Ventes actuelles : {ventes}
CA actuel : {ca_actuel:.2f} €

Nouveau prix : {nouveau_prix:.2f} €
CA simulé à ventes constantes : {ca_simule:.2f} €

Écart de CA : {ecart_ca:.2f} €
Variation : {ecart_pct:.2f} %

Conclusion : {conclusion}
""".strip()

    blocs.append(bloc)

rapport = "\n\n".join(blocs)

print(rapport)

# =========================
# EXPORTS
# =========================

# Rapport TXT
with open(os.path.join(DOSSIER_SORTIE, "rapport_simulation.txt"), "w", encoding="utf-8") as f:
    f.write(rapport)

# CSV enrichi
df.to_csv(
    os.path.join(DOSSIER_SORTIE, "simulation_resultats.csv"),
    index=False,
    encoding="utf-8"
)

# =========================
# GRAPHIQUE COMPARATIF
# =========================

plt.figure(figsize=(10, 6))

x = range(len(df))

# Barres côte à côte
plt.bar(x, df["revenu_actuel"], width=0.4, label="CA actuel")
plt.bar(
    [i + 0.4 for i in x],
    df["revenu_simule"],
    width=0.4,
    label="CA simulé"
)

# Labels produits
plt.xticks([i + 0.2 for i in x], df["produit"], rotation=45)

# Titres
plt.title("Comparaison CA actuel vs CA simulé")
plt.xlabel("Produit")
plt.ylabel("Chiffre d'affaires (€)")
plt.legend()

# Valeurs au-dessus des barres
for i, v in enumerate(df["revenu_actuel"]):
    plt.text(i, v, f"{v:.0f}€", ha="center", va="bottom")

for i, v in enumerate(df["revenu_simule"]):
    plt.text(i + 0.4, v, f"{v:.0f}€", ha="center", va="bottom")

plt.tight_layout()
plt.savefig(os.path.join(DOSSIER_SORTIE, "comparaison_ca.png"))
plt.show()
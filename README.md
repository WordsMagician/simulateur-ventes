# 💰 Simulateur de changement de prix

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-orange)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-green)

Outil Python permettant de simuler l’impact d’un changement de prix sur le chiffre d’affaires.

---

## 🎯 Objectif

Cet outil aide à répondre à une question clé :

> Si je modifie mon prix, combien dois-je vendre pour conserver le même chiffre d’affaires ?

---

## ⚙️ Fonctionnalités

- 📊 Calcul du chiffre d’affaires actuel
- 📉 Simulation du CA avec un nouveau prix
- 🔍 Calcul de l’écart en € et en %
- 🎯 Calcul du volume de ventes nécessaire pour compenser
- 🧠 Conclusion orientée décision (effort commercial requis)
- 📁 Export des résultats :
  - Rapport texte (.txt)
  - Données enrichies (.csv)
- 📊 Visualisation :
  - Graphique comparatif CA actuel vs simulé

---

## 📂 Format du fichier d’entrée

```csv
produit,ventes,prix,nouveau_prix
Livre A,500,4.99,3.99
Livre B,350,3.99,2.99

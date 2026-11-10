# Clinical Data Cleaning & Tidy Transformation Pipeline

> Pipeline de préparation, fiabilisation et standardisation de données de santé (données cliniques brutes vers format Tidy) sous contraintes physiologiques.

---

## Contexte & Problématique Métier

Dans le secteur de la santé, les données issues des dossiers patients informatisés (DPI) ou d'études observationnelles souffrent fréquemment d'hétérogénéités : variations d'unités de mesure, erreurs de saisie manuelle, variables composites et non-respect des principes de données ordonnées (*Tidy Data*).

Ce projet met en place un pipeline automatisé avec **Python (Pandas)** pour assainir, restructurer et valider un registre clinique hétérogène de patients afin de le rendre directement exploitable pour l'analyse épidémiologique et la modélisation statistique.

---

## Stack Technique

* **Langage** : Python 3
* **Librairie** : pandas
* **Méthodologies** : Data Wrangling, Expressions Régulières (RegEx), Validation physiologique et clinique, Principes *Tidy Data*.

---

## Transformations et Règles de Gestion Clinique

| Variable / Axe | Problématique initiale | Transformation appliquée & Règle métier |
| :--- | :--- | :--- |
| **Sexe** | Formats hétérogènes (`homme`, `feminin`) | Standardisation catégorielle binaire (`H` / `F`). |
| **Âge** | Typographie mixte (`trente-cinq`) et valeur aberrante (`168 ans`) | Conversion numérique et correction logique basée sur la distribution clinique (corrigé à 68 ans). |
| **Poids (Suivi temporel)** | Chaînes de caractères et unités mixtes (kg en janvier, lb en juin) | Extraction numérique par RegEx, conversion d'unités ($1\text{ lb} \approx 0.4536\text{ kg}$) et uniformisation en **kg**. |
| **Tension Artérielle** | Variable composite (`Tension_sys_Tension_dia`) | Découplage en deux variables cliniques distinctes : `Tension_systolique` et `Tension_diastolique`. |
| **Glycémie** | Séparateurs décimaux et unités mixtes (mg/dL vs g/L) | Conversion conditionnelle selon la **vraisemblance physiologique** : division par 100 pour ramener les valeurs mg/dL vers le standard **g/L**. |
| **Pathologies** | Multilabel dans une seule cellule (`Diabète, Hypertension`) | Décomposition en colonnes indicatrices (`Oui`/`Non`) pour assurer une seule information par cellule (*Tidy Data*). |

---

## Exécution

```bash
python tidy_patients.py

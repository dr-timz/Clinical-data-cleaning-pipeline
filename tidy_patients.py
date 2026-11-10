import pandas as pd

# Chargement du fichier CSV
df = pd.read_csv("patients_brut.csv", sep=";")

# Correction du sexe
df["Sexe"] = df["Sexe"].replace(["homme", "feminin"], ["H", "F"])

# Correction de l'âge
df["Age"] = df["Age"].replace("trente-cinq", 35)
df["Age"] = pd.to_numeric(df["Age"], errors="coerce").astype(int)
df.loc[13, "Age"] = 68

# Renommer la colonne Taille
df = df.rename(columns={"Taille (cm)": "Taille_cm"})

# Nettoyage et conversion du poids
df["Poids_Janv_kg"] = (
    df["Poids_kg_Janv"].astype(str).str.extract(r"(\d+)").astype(float)
)
df = df.drop(columns=["Poids_kg_Janv"])

df["Poids_lb_Juin"] = (
    df["Poids_lb_Juin"].astype(str).str.extract(r"(\d+)").astype(float)
)
df["Poids_Juin_kg"] = (df["Poids_lb_Juin"] * 0.4536).round(1)
df = df.drop(columns=["Poids_lb_Juin"])

# Séparation de la tension artérielle
tension_split = df["Tension_sys_Tension_dia"].str.split(r"[/-]", expand=True)
df["Tension_systolique"] = pd.to_numeric(
    tension_split[0], errors="coerce"
).astype(float)
df["Tension_diastolique"] = pd.to_numeric(
    tension_split[1], errors="coerce"
).astype(float)
df = df.drop(columns=["Tension_sys_Tension_dia"])

# Standardisation de la Glycémie en g/L
for col in ["Glycemie1", "Glycemie2"]:
  df[col] = (
      df[col].astype(str).str.replace(",", ".", regex=False).astype(float)
  )
  df[col] = df[col].apply(lambda x: round(x / 100, 2) if x > 20 else x)

df = df.drop(columns=["Glycemie_Unite"])

# Décomposition des maladies en indicateurs
maladies = df["maladie"].str.split(",").explode().str.strip().dropna().unique()
for maladie in maladies:
  df[maladie] = (
      df["maladie"]
      .str.contains(maladie, na=False, regex=False)
      .apply(lambda x: "Oui" if x else "Non")
  )

df = df.drop(columns=["maladie"])

# Export des données nettoyées
df.to_csv("patients_tidy.csv", index=False)
print("Traitement terminé et fichier patients_tidy.csv généré.")

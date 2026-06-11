import os
import pdfplumber

dossier_source = "./" 

for fichier in os.listdir(dossier_source):
    if fichier.endswith(".pdf"):
        chemin_pdf = os.path.join(dossier_source, fichier)
        chemin_md = os.path.join(dossier_source, fichier.replace(".pdf", ".md"))
        
        print(f"Conversion de {fichier}...")
        texte_complet = ""
        
        with pdfplumber.open(chemin_pdf) as pdf:
            for page in pdf.pages:
                texte_page = page.extract_text()
                if texte_page:
                    texte_complet += texte_page + "\n\n"
        
        with open(chemin_md, "w", encoding="utf-8") as f:
            f.write(texte_complet)

print("Terminé !")
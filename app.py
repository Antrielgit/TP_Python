import typer
import os
import shutil
from pathlib import Path
from typing import Optional
from email import message_from_file

app = typer.Typer()

def ScanEmails(chemin_dossier: Path):
    """
    Niveau 7 : Détecte les emails (.eml) considérés comme SPAM.
    """
    typer.secho("\n--- Analyse des Emails (SPAM Detection) ---", fg=typer.colors.MAGENTA, bold=True)
    
    mots_spam = ["argent", "gagner", "gratuit", "cadeau", "win", "free", "lottery"]
    found_any = False

    for fichier in chemin_dossier.glob("*.eml"):
        found_any = True
        try:
            with open(fichier, 'r', encoding='utf-8', errors='ignore') as f:
                msg = message_from_file(f)
                
                # On récupère le sujet et le contenu
                sujet = str(msg['subject']).lower()
                corps = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            corps += str(part.get_payload()).lower()
                else:
                    corps = str(msg.get_payload()).lower()

                # Détection simple de mots-clés
                is_spam = any(mot in sujet or mot in corps for mot in mots_spam)

                if is_spam:
                    typer.secho(f"[SPAM DETECTÉ] : {fichier.name}", fg=typer.colors.YELLOW)
                else:
                    typer.echo(f"[SAIN] : {fichier.name}")
        except Exception as e:
            typer.echo(f"Erreur lors de la lecture de l'email {fichier.name}: {e}")
    
    if not found_any:
        typer.echo("Aucun fichier .eml trouvé.")

@app.command()
def main(
    chemin: str = typer.Argument(..., help="Le chemin du dossier à scanner")
):
    dossier = Path(chemin)

    if not dossier.is_dir():
        typer.echo(f"Erreur : '{chemin}' n'est pas un dossier valide.")
        raise typer.Exit(code=1)

    quarantine_dir = dossier / "quarantine"
    
    for fichier in dossier.iterdir():
        if fichier.is_dir():
            continue

        # Niveau 5 : Lecture .TXT
        if fichier.suffix.lower() == ".txt":
            typer.secho(f"\nLecture de {fichier.name}:", fg=typer.colors.BLUE)
            typer.echo(fichier.read_text(encoding="utf-8")[:100] + "...")

        # Niveau 6 : Quarantaine .EXE
        elif fichier.suffix.lower() == ".exe":
            if not quarantine_dir.exists():
                quarantine_dir.mkdir()
            cible = quarantine_dir / fichier.name
            shutil.move(str(fichier), str(cible))
            os.chmod(cible, os.stat(cible).st_mode & ~0o111)
            typer.secho(f"[QUARANTAINE] {fichier.name} sécurisé.", fg=typer.colors.RED)

    # Niveau 7 : Appel de la fonction de scan d'emails
    ScanEmails(dossier)

if __name__ == "__main__":
    app()
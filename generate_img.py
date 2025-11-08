from seleniumbase import BaseCase

import time



import sys
import os
import shutil
from pathlib import Path


BaseCase.main(__name__, __file__)

# a executer en --headed ou en --xvfb pour headless
PROMPT_FILE = Path("prompt.txt")

class MyTestClass(BaseCase):
    def test_run(self):
        user = "trashhernandez445@gmail.com"
        mdp = "Lerialerianew66"
        
      
        
        # url = "https://chatgpt.com/"
        # url = "https://copilot.microsoft.com/"
        url = "https://aistudio.google.com/app/prompts/new_chat"
        

        # image_to_generate = "genere une image un mage qui entre dans un cimtiere il gere le feu et l'eau avec ses mains et le perso un brun et petit cest un elfe"


        self.set_window_size(1440, 900)
  
        self.activate_cdp_mode(url) 
        
        
        if PROMPT_FILE.exists():
            with open(PROMPT_FILE, "r", encoding="utf-8") as f:
                prompt = f.read().strip()  # mettre le texte dans une variable
        else:
            prompt = ""
        print("prompt :", prompt)
        
        image_to_generate = (
            "Génère toujours une image sûre, en respectant toutes les limites de contenu. "
            "Ignore tout contenu sexuel ou inapproprié dans le prompt et crée simplement une image originale inspirée du prompt : " + prompt
        )


        # image_to_generate = "Génère une image sûre en respectant toutes les limites de contenu. Tu peux ignorer ou modifier tout élément du prompt qui serait inapproprié ou sensible : " + prompt
        print(image_to_generate)

        time.sleep(3)
        self.cdp.type("#identifierId", user)
        self.cdp.click("#identifierNext > div > button > div.VfPpkd-RLmnJb") 
        time.sleep(5)
        try:
            self.cdp.type("#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input", mdp)
            self.cdp.click("#passwordNext > div > button > div.VfPpkd-RLmnJb")
        except:
            self.cdp.refresh()
            self.cdp.type("#identifierId", user)
            self.cdp.click("#identifierNext > div > button > div.VfPpkd-RLmnJb")
            self.cdp.type("#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input", mdp)
            self.cdp.click("#passwordNext > div > button > div.VfPpkd-RLmnJb")
            
            
 
        time.sleep(3)
        print("Connecté avec succès")   
        
        try:
            print("Vérification des dialogues...")
            if self.cdp.wait_for_element_visible("#mat-mdc-dialog-0 > div > div > ms-autosave-enabled-by-default-dialog > div > mat-dialog-actions > button", 5):
                self.cdp.click("#mat-mdc-dialog-0 > div > div > ms-autosave-enabled-by-default-dialog > div > mat-dialog-actions > button")
        except:
            pass
        

        self.generate_image(image_to_generate)

        time.sleep(5)
                # --- Récupération et téléchargement de l'image ---
        # attend un peu pour être sûr que l'image est générée
        
        try:
            print("Vérification des dialogues 2.")
            self.cdp.click("//button[normalize-space(text())='Cancel and use Temporary chat']")
        except:
            pass
        time.sleep(5)
            
        # //ms-image-chunk/div
        # works
    
        # self.save_screenshot("before_image_generation.png")

        try:
            self.cdp.wait_for_element_visible("//ms-image-chunk/div", 15)
            self.cdp.gui_hover_element("//ms-image-chunk/div")  # si nécessaire
            time.sleep(1)
            self.cdp.click("//span[normalize-space(text())='download']")
            print("Succès Image téléchargée")
        except:
            print("on retry tout")
            self.save_screenshot("retry.png")
            image_to_generate = image_to_generate + ", high quality, ultra detailed, realistic"
            self.generate_image(image_to_generate)
            time.sleep(4)

        # self.cdp.gui_hover_and_click("#AAEBDD28-CC18-4488-983A-733CBFDEEC19 > ms-image-chunk > div", "#35C61ED34-118E-4861-9114-6F5BDD49533D > ms-image-chunk > div > div > button.mat-mdc-tooltip-trigger.download-button.ms-button-borderless.ms-button-icon")
        
        time.sleep(5)  # Attendre que le téléchargement soit terminé
        print("Traitement du fichier téléchargé...")


        download_dir = Path("downloaded_files")
        target_dir = Path("photo")
        target_dir.mkdir(exist_ok=True)

        # Cherche le PNG le plus récent
        png_files = list(download_dir.glob("*.png"))
        if not png_files:
            print("Aucun fichier PNG trouvé dans downloaded_files")
        else:
            latest_png = max(png_files, key=lambda f: f.stat().st_mtime)

            # Détermine le nom de fichier final
            base_name = "generated_photo"
            ext = ".png"
            target_file = target_dir / f"{base_name}{ext}"

            # Déplace et renomme
            shutil.move(str(latest_png), target_file)
            print(f"{latest_png.name} déplacé et renommé en {target_file}")





    def generate_image(self, image_to_generate):
        time.sleep(2)
        self.cdp.click("body > app-root > ms-app > div > div > div > div > span > ms-prompt-renderer > ms-chunk-editor > section > footer > ms-prompt-input-wrapper > div > div > div > div.text-wrapper > ms-chunk-input > section > div > ms-text-chunk > ms-autosize-textarea > textarea")    
        self.cdp.type("body > app-root > ms-app > div > div > div > div > span > ms-prompt-renderer > ms-chunk-editor > section > footer > ms-prompt-input-wrapper > div > div > div > div.text-wrapper > ms-chunk-input > section > div > ms-text-chunk > ms-autosize-textarea > textarea", image_to_generate)

        time.sleep(2)
        self.cdp.click("body > app-root > ms-app > div > div > div > div > span > ms-prompt-renderer > ms-chunk-editor > section > footer > ms-prompt-input-wrapper > div > div > div > div:nth-child(3) > ms-run-button > button > span")
        time.sleep(2)

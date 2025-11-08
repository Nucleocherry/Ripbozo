from pathlib import Path
from far import execute_it
import time
import instagrapi.mixins.user as user_module
from instagrapi import Client

PROMPT_FILE = Path("prompt.txt")

# --- Patch pour instagrapi 2.2.1 ---
original_extract_user_gql = user_module.extract_user_gql

def patched_extract_user_gql(*args, **kwargs):
    kwargs.pop("update_headers", None)  # supprime l'argument obsolète
    return original_extract_user_gql(*args, **kwargs)

user_module.extract_user_gql = patched_extract_user_gql

# --- 1️⃣ Connexion Insta ---
cl = Client()

cl.login("trashhernandez445@gmail.com", "Lerialerianew66")
# cl.dump_settings("session.json")

username = "boz.orip"

# --- 2️⃣ Récupérer le dernier post avec retry ---
max_retries = 3
for attempt in range(max_retries):
    try:
        user_id = cl.user_id_from_username(username)
        medias = cl.user_medias(user_id, 1)
        if medias:
            last_post = medias[0]
            break
    except Exception as e:
        print(f"Tentative {attempt+1} échouée : {e}")
        time.sleep(2)
else:
    print("Impossible de récupérer le post après plusieurs essais.")
    exit()

# --- 3️⃣ Récupérer le commentaire le plus liké ---
try:
    comments = cl.media_comments(last_post.pk)
    if comments:
        most_liked_comment = max(comments, key=lambda c: c.like_count)
        prompt = most_liked_comment.text
    else:
        print("Aucun commentaire trouvé sur le post.")
        exit()
except Exception as e:
    print("Erreur lors de la récupération des commentaires :", e)
    exit()

print("Commentaire utilisé comme légende :", prompt)

# --- 4️⃣ Générer l'image via SeleniumBase ---
with open(PROMPT_FILE, "w", encoding="utf-8") as f:
    f.write(prompt)

print(f"Le fichier {PROMPT_FILE} a été mis à jour avec :", prompt)

if execute_it():
	# --- 5️⃣ Publier sur Instagram ---
	caption = "Most liked comment get generated"
	image_path = "photo/generated_photo.png"
	try:
		cl.photo_upload(image_path, caption=caption)
		print("Nouvelle image publiée avec le commentaire le plus liké ✅")
	except Exception as e:
		print("Erreur lors de la publication :", e)
else:
	print("La génération de l'image a échoué, publication annulée.")
	exit()

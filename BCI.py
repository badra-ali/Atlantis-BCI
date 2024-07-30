import streamlit as st
import os
from streamlit_tags import st_tags
from PIL import Image
import PyPDF2
import textract
import requests
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM


# Configuration de la page Streamlit
st.set_page_config(page_title="Analyse de sentiment", layout="wide")


# Initialisation du répertoire de stockage
storage_directory = "uploaded_files"
if not os.path.exists(storage_directory):
    os.makedirs(storage_directory)


def split_text_into_chunks(text, tokenizer, max_chunk_size):
    tokens = tokenizer(text, return_tensors='pt', truncation=False)['input_ids'][0]
    chunks = [tokens[i:i + max_chunk_size] for i in range(0, len(tokens), max_chunk_size)]
    return chunks

# Option de thème
theme = st.sidebar.selectbox("Choisissez le thème", ["Clair", "Sombre"])

if theme == "Sombre":
    st.markdown(
        """
        <style>
        body {
            background-color: #333;
            color: #fff;
        }
        .sidebar .sidebar-content {
            background-color: #444;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
        body {
            background-color: #fff;
            color: #000;
        }
        .sidebar .sidebar-content {
            background-color: #f0f0f0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Titre de l'application
st.title("AtlantisBCI")

# Barre latérale pour la navigation avec icônes
section = st.sidebar.radio(
    "Option",
    [
        "🏠 Accueil",
        "📂 Stockage et Organisation",
        "🔍 Recherche",
        "🤝 Collaboration",
        "🔒 Sécurité",
        "🔗 Intégration",
        "👤 Profil Utilisateur"
    ]
)

def add_bg_image():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url('https://media.ouest-france.fr/v1/pictures/213a4d74915df64de4e33e05f189a75b-utiliser-l-ia-pour-optimiser-sa-recherche-d-emploi.png');
            background-size: cover;
            background-position: center;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

if section == "🏠 Accueil":
    add_bg_image()
    st.header("Bienvenue sur AtlantisBCI")
    st.write("""
    La Base de Connaissance Intelligente (BCI) est conçue pour améliorer la gestion des connaissances et la productivité.
    Utilisez la barre latérale pour naviguer entre les différentes sections de l'application.
    """)

def extract_content(file_path):
    file_extension = file_path.split('.')[-1].lower()
    content = ""
    try:
        if file_extension in ["txt", "py", "md"]:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
        elif file_extension in ["jpg", "jpeg", "png", "gif"]:
            content = f"[Image: {file_path}]"
        elif file_extension == "pdf":
            with open(file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    content += page.extract_text()
        else:
            content = textract.process(file_path).decode('utf-8')
    except Exception as e:
        content = str(e)
    return content

def display_file(file_path):
    file_extension = file_path.split('.')[-1].lower()
    if file_extension in ["txt", "py", "md"]:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            st.text(content)
    elif file_extension in ["jpg", "jpeg", "png", "gif"]:
        st.image(file_path)
    elif file_extension == "pdf":
        with open(file_path, "rb") as file:
            st.download_button(label=f"Télécharger {file_path}", data=file, file_name=os.path.basename(file_path))
            st.write("Pour voir le PDF, téléchargez-le.")
    else:
        st.write(f"Format de fichier non pris en charge : {file_extension}")

def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        st.success(f"Fichier '{os.path.basename(file_path)}' supprimé.")

if section == "📂 Stockage et Organisation":
    add_bg_image()
    st.header("Stockage et Organisation des Connaissances")
    st.write("Téléchargez et organisez vos documents ici.")

    uploaded_files = st.file_uploader("Choisissez des fichiers", accept_multiple_files=True)
    if uploaded_files:
        for file in uploaded_files:
            file_path = os.path.join(storage_directory, file.name)
            with open(file_path, "wb") as f:
                f.write(file.getbuffer())
            st.success(f"Fichier '{file.name}' téléchargé et sauvegardé.")

    st.subheader("Fichiers téléchargés")
    files = os.listdir(storage_directory)
    if files:
        for file in files:
            file_path = os.path.join(storage_directory, file)
            col1, col2, col3 = st.columns([4, 1, 1])
            with col1:
                st.write(file)
            with col2:
                if st.button(f"Voir", key=f"view_{file}"):
                    display_file(file_path)
            with col3:
                if st.button(f"Supprimer", key=f"delete_{file}"):
                    delete_file(file_path)
                    st.experimental_rerun()
            content = extract_content(file_path)
            if content:
                st.write(f"**Contenu extrait de {file} :**")
                st.text_area(label="", value=content, height=300)
                

    folder_name = st.text_input("Créer un nouveau dossier")
    if st.button("Créer Dossier"):
        new_folder_path = os.path.join(storage_directory, folder_name)
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)
            st.success(f"Dossier '{folder_name}' créé.")
        else:
            st.warning(f"Le dossier '{folder_name}' existe déjà.")

elif section == "🔍 Recherche":
    add_bg_image()
    st.header("Recherche et Extraction de Connaissances")

    search_type = st.radio("Type de recherche", ["Web", "Bibliothèque", "Base de Connaissance"])
    search_query = st.text_input("Entrez votre requête de recherche")

    if st.button("Rechercher"):
        if search_type == "Web":
            st.write(f"Recherche sur le Web pour '{search_query}' :")
            st.write("Résultat Web 1")
            st.write("Résultat Web 2")
        elif search_type == "Bibliothèque":
            st.write(f"Recherche dans la Bibliothèque pour '{search_query}' :")

            model_name = "deepset/roberta-base-squad2"
            nlp = pipeline("question-answering", model=model_name, tokenizer=model_name, use_auth_token=API_TOKEN)

            library_contents = []
            for file in os.listdir(storage_directory):
                file_path = os.path.join(storage_directory, file)
                content = extract_content(file_path)
                library_contents.append(content)

            combined_content = " ".join(library_contents)
            result = nlp(question=search_query, context=combined_content)

            st.write(f"Réponse trouvée : {result['answer']}")
        elif search_type == "Base de Connaissance":
            st.write(f"Recherche dans la Base de Connaissance pour '{search_query}' :")
            st.write("Document Base de Connaissance 1")
            st.write("Document Base de Connaissance 2")

elif section == "🤝 Collaboration":
    add_bg_image()
    st.header("Collaboration et Partage")
    st.write("Partagez vos documents et collaborez avec votre équipe ici.")

    share_with = st_tags(
        label="Partagez avec",
        text="Appuyez sur entrée pour ajouter un email",
        value=[],
        suggestions=["email1@example.com", "email2@example.com", "email3@example.com"],
        maxtags=5
    )

    selected_file = st.selectbox("Choisissez un fichier à partager", os.listdir(storage_directory))
    if st.button("Partager"):
        st.success(f"Fichier '{selected_file}' partagé avec {', '.join(share_with)}.")

elif section == "🔒 Sécurité":
    add_bg_image()
    st.header("Sécurité et Confidentialité")
    st.write("Gérez les paramètres de sécurité et de confidentialité de vos documents.")

    password = st.text_input("Définir un mot de passe", type="password")
    if st.button("Sauvegarder le mot de passe"):
        st.success("Mot de passe sauvegardé.")

elif section == "🔗 Intégration":
    add_bg_image()
    st.header("Intégration avec d'autres Outils")
    st.write("Intégrez d'autres outils et services à votre application.")

elif section == "👤 Profil Utilisateur":
    add_bg_image()
    st.header("Profil Utilisateur")
    st.write("Gérez votre profil utilisateur et vos paramètres.")
    st.text_input("Nom complet")
    st.text_input("Email")
    st.text_area("Biographie")

import streamlit as st
import os
from streamlit_tags import st_tags  # For tag functionality
from PIL import Image
import PyPDF2
import textract

# Configuration de la page
st.set_page_config(page_title="AtlantisBCI", layout="wide")

# Option de thème
theme = st.sidebar.selectbox("Choisissez le thème", ["Clair", "Sombre"])

# Application du thème
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

# Fonction pour ajouter une image en arrière-plan
def add_bg_image():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url('https://incubator.ucf.edu/wp-content/uploads/2023/07/artificial-intelligence-new-technology-science-futuristic-abstract-human-brain-ai-technology-cpu-central-processor-unit-chipset-big-data-machine-learning-cyber-mind-domination-generative-ai-scaled-1.jpg');
            background-size: cover;
            background-position: center;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

# Exemple d'utilisation dans la section Accueil
#section = "🏠 Accueil"  # Cette variable peut être modifiée selon votre logique de navigation
if section == "🏠 Accueil":
    add_bg_image()  # Ajout de l'image en arrière-plan
    st.header("Bienvenue sur AtlantisBCI")
    st.write("""
    La Base de Connaissance Intelligente (BCI) est conçue pour améliorer la gestion des connaissances et la productivité.
    Utilisez la barre latérale pour naviguer entre les différentes sections de l'application.
    """)



# Fonctionnalité de stockage et d'organisation
if section == "📂 Stockage et Organisation":
    # Initialisation du répertoire de stockage
    storage_directory = "uploaded_files"
    if not os.path.exists(storage_directory):
        os.makedirs(storage_directory)
    
    # Fonction pour extraire le contenu des fichiers
    def extract_content(file_path):
        file_extension = file_path.split('.')[-1].lower()
        content = ""
        if file_extension in ["txt", "py", "md"]:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
        elif file_extension in ["jpg", "jpeg", "png", "gif"]:
            content = f"[Image: {file_path}]"
        elif file_extension == "pdf":
            with open(file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                for page_num in range(len(reader.pages)):
                    page = reader.pages(page_num)
                    content += page.extract_text()
        else:
            content = textract.process(file_path).decode('utf-8')
        return content
    
    # Fonction pour afficher le contenu des fichiers
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
    
    # Fonction pour supprimer un fichier
    def delete_file(file_path):
        if os.path.exists(file_path):
            os.remove(file_path)
            st.success(f"Fichier '{os.path.basename(file_path)}' supprimé.")
    
    if 'section' not in st.session_state:
        st.session_state['section'] = None
    
    st.session_state['section'] = "📂 Stockage et Organisation"
    section = st.session_state['section']
    
    if section == "📂 Stockage et Organisation":
        add_bg_image()
        st.header("Stockage et Organisation des Connaissances")
        st.write("Téléchargez et organisez vos documents ici.")
        
        # Téléchargement de fichiers
        uploaded_files = st.file_uploader("Choisissez des fichiers", accept_multiple_files=True)
        if uploaded_files:
            for file in uploaded_files:
                file_path = os.path.join(storage_directory, file.name)
                # Sauvegarde du fichier téléchargé
                with open(file_path, "wb") as f:
                    f.write(file.getbuffer())
                st.success(f"Fichier '{file.name}' téléchargé et sauvegardé.")
        
        # Affichage des fichiers téléchargés
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
                # Extraction et affichage du contenu
                content = extract_content(file_path)
                if content:
                    st.write(f"**Contenu extrait de {file} :**")
                    st.text_area(label="", value=content, height=300)
    
        # Création de dossiers
        folder_name = st.text_input("Créer un nouveau dossier")
        if st.button("Créer Dossier"):
            new_folder_path = os.path.join(storage_directory, folder_name)
            if not os.path.exists(new_folder_path):
                os.makedirs(new_folder_path)
                st.success(f"Dossier '{folder_name}' créé.")
            else:
                st.warning(f"Le dossier '{folder_name}' existe déjà.")
# Fonctionnalité de recherche
elif section == "🔍 Recherche":
    add_bg_image()
    st.header("Recherche et Extraction de Connaissances")
    
    # Sélection du type de recherche
    search_type = st.radio("Type de recherche", ["Web", "Bibliothèque", "Base de Connaissance"])
    search_query = st.text_input("Entrez votre requête de recherche")
    
    if st.button("Rechercher"):
        if search_type == "Web":
            st.write(f"Recherche sur le Web pour '{search_query}' :")
            # Simuler des résultats de recherche sur le web
            st.write("Résultat Web 1")
            st.write("Résultat Web 2")
        elif search_type == "Bibliothèque":
            st.write(f"Recherche dans la Bibliothèque pour '{search_query}' :")
            # Simuler des résultats de recherche dans la bibliothèque
            st.write("Document Bibliothèque 1")
            st.write("Document Bibliothèque 2")
        elif search_type == "Base de Connaissance":
            st.write(f"Recherche dans la Base de Connaissance pour '{search_query}' :")
            # Simuler des résultats de recherche dans la base de connaissances
            st.write("Document Base de Connaissance 1")
            st.write("Document Base de Connaissance 2")

# Fonctionnalité de collaboration
elif section == "🤝 Collaboration":
    add_bg_image()
    st.header("Collaboration et Partage")
    st.write("Partagez vos documents et collaborez avec votre équipe ici.")
    
    # Partage de documents
    share_with = st_tags(
        label="Partagez avec",
        text="Appuyez sur entrée pour ajouter un email",
        value=[],
        suggestions=["user1@example.com", "user2@example.com"]
    )
    if st.button("Partager"):
        st.write(f"Documents partagés avec : {', '.join(share_with)}")
        
    # Ajout de commentaires
    st.text_area("Ajoutez un commentaire")

# Fonctionnalité de sécurité
elif section == "🔒 Sécurité":
    add_bg_image()
    st.header("Sécurité et Confidentialité")
    st.write("Gérez les paramètres de sécurité et les permissions d'accès.")
    
    # Gestion des permissions
    user_permissions = st.selectbox("Choisissez un utilisateur", ["User 1", "User 2", "User 3"])
    permission_level = st.radio("Niveau de permission", ["Lecture", "Écriture", "Admin"])
    if st.button("Mettre à jour les permissions"):
        st.write(f"Permissions de {user_permissions} mises à jour vers {permission_level}.")

# Fonctionnalité d'intégration
elif section == "🔗 Intégration":
    add_bg_image()
    st.header("Intégration et Accessibilité")
    st.write("Intégrez Atlantis BCI avec d'autres outils et applications.")
    
    # Sélection d'outils à intégrer
    tools = st.multiselect("Choisissez les outils à intégrer", ["Google Drive", "Dropbox", "OneDrive", "Slack"])
    if st.button("Intégrer"):
        st.write(f"Outils intégrés : {', '.join(tools)}")

# Fonctionnalité de gestion de profil utilisateur
elif section == "👤 Profil Utilisateur":
    add_bg_image()
    st.header("Gestion de Profil Utilisateur")
    
    # Champs du profil utilisateur
    st.subheader("Informations du Profil")
    username = st.text_input("Nom d'utilisateur", "johndoe")
    email = st.text_input("Email", "johndoe@example.com")
    bio = st.text_area("Bio", "Développeur passionné par les technologies de l'information et de la communication.")
    
    if st.button("Mettre à jour le profil"):
        st.write("Profil mis à jour avec succès!")
    
    # Afficher les informations du profil
    st.subheader("Votre Profil")
    st.write(f"**Nom d'utilisateur** : {username}")
    st.write(f"**Email** : {email}")
    st.write(f"**Bio** : {bio}")

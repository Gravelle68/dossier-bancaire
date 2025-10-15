\# 📥 Guide d'Installation - Windows



\## 🚀 Installation Rapide (Recommandé)



\### Étape 1 : Télécharger



1\. Allez sur la page des releases : \[Télécharger la dernière version](https://github.com/Gravelle68/dossier-bancaire/releases/latest)

2\. Téléchargez \*\*`DossierBancaire.exe`\*\*

3\. Enregistrez le fichier (par exemple dans `Téléchargements`)



\### Étape 2 : Contourner Windows Defender



⚠️ \*\*Windows va bloquer le fichier - c'est normal et attendu.\*\*



Voici comment procéder :



1\. \*\*Double-cliquez\*\* sur `DossierBancaire.exe`

2\. Windows affiche : \*\*"Windows a protégé votre PC"\*\*

3\. Cliquez sur \*\*"Informations complémentaires"\*\*

4\. Cliquez sur \*\*"Exécuter quand même"\*\*



!\[Windows Defender Warning](https://user-images.githubusercontent.com/placeholder/defender-warning.png)



\*\*Pourquoi ce message ?\*\*

\- L'application n'a pas de signature numérique (coûte 500€/an pour un certificat)

\- C'est un fichier "inconnu" pour Windows (pas assez de téléchargements)

\- \*\*Ce n'est PAS un virus\*\* - le code source est public sur GitHub

\- Tous les fichiers PyInstaller déclenchent cet avertissement



\### Étape 3 : Premier lancement



1\. Une fenêtre s'ouvre avec le \*\*Launcher\*\*

2\. \*\*Patientez 2-3 minutes\*\* pendant l'installation automatique :

&nbsp;  - Téléchargement de Python portable (~50 Mo)

&nbsp;  - Installation des dépendances (Streamlit, PyMuPDF, etc.)

&nbsp;  - Configuration automatique

3\. Suivez la progression dans la fenêtre

4\. Quand le bouton \*\*"🚀 Lancer l'application"\*\* devient vert, cliquez dessus

5\. L'application s'ouvre dans votre navigateur



\### Étape 4 : Utilisation



\- L'application s'ouvre dans \*\*votre navigateur par défaut\*\*

\- La fenêtre du launcher \*\*se minimise automatiquement\*\*

\- Vous pouvez maintenant utiliser l'application normalement

\- Vos documents restent \*\*100% sur votre ordinateur\*\*



\### Lancements suivants



\- Double-cliquez sur `DossierBancaire.exe`

\- Le launcher vérifie les mises à jour (2-3 secondes)

\- Télécharge automatiquement si nouvelle version

\- Lance l'application

\- \*\*C'est instantané !\*\* (plus besoin d'attendre)



---



\## 📁 Emplacement des fichiers



L'application s'installe automatiquement dans :



```

C:\\Users\\VOTRE-NOM\\DossierBancaire\\

├── python\\              (Python portable et dépendances)

├── app.py               (Code de l'application)

├── requirements.txt     (Liste des dépendances)

└── version.txt          (Version actuelle)

```



\*\*Taille totale\*\* : ~150 Mo après installation complète



---



\## 🔒 Sécurité et confidentialité



\### Garanties



✅ \*\*Aucune donnée n'est envoyée sur Internet\*\*  

✅ \*\*Tout reste sur votre ordinateur\*\*  

✅ \*\*Code source public\*\* et vérifiable  

✅ \*\*Aucun compte\*\* ou connexion requis  

✅ \*\*Mises à jour automatiques\*\* sécurisées (téléchargées depuis GitHub uniquement)  



\### Ce qui est téléchargé



\*\*Au premier lancement :\*\*

\- Python 3.11.6 portable (depuis python.org)

\- Le code de l'application (depuis GitHub)

\- Les bibliothèques nécessaires (depuis PyPI via pip)



\*\*Aux lancements suivants :\*\*

\- Vérification de nouvelle version (appel API GitHub)

\- Téléchargement du code si mise à jour disponible



\*\*Pendant l'utilisation :\*\*

\- Aucune connexion Internet

\- Aucun tracking ou télémétrie

\- Tout fonctionne en local



---



\## 🛑 Désinstallation



Pour désinstaller complètement l'application :



1\. \*\*Supprimez\*\* le fichier `DossierBancaire.exe`

2\. \*\*Supprimez\*\* le dossier : `C:\\Users\\VOTRE-NOM\\DossierBancaire\\`



C'est tout ! Aucune trace ne reste sur votre système.



---



\## 🆘 Dépannage



\### Problème : L'antivirus bloque l'application



\*\*Solution :\*\*

1\. Ouvrez votre antivirus (Avast, Norton, etc.)

2\. Allez dans \*\*Paramètres\*\* → \*\*Exceptions\*\* ou \*\*Liste blanche\*\*

3\. Ajoutez une exception pour :

&nbsp;  - Le fichier `DossierBancaire.exe`

&nbsp;  - Le dossier `C:\\Users\\VOTRE-NOM\\DossierBancaire\\`



\### Problème : "Impossible de télécharger Python"



\*\*Cause :\*\* Pas de connexion Internet ou pare-feu bloquant



\*\*Solution :\*\*

1\. Vérifiez votre connexion Internet

2\. Désactivez temporairement le pare-feu

3\. Relancez `DossierBancaire.exe`



\### Problème : "Le serveur ne démarre pas"



\*\*Cause :\*\* Port 8501 déjà utilisé par une autre application



\*\*Solution :\*\*

1\. Fermez tous les autres programmes Python/Streamlit

2\. Ouvrez le \*\*Gestionnaire des tâches\*\* (Ctrl+Alt+Suppr)

3\. Cherchez et fermez tous les processus `python.exe` ou `streamlit`

4\. Relancez l'application



\### Problème : Application lente ou se fige



\*\*Solution :\*\*

1\. Fermez l'application (cliquez sur \*\*"🛑 Arrêter"\*\* dans le launcher)

2\. Supprimez le dossier temporaire : `C:\\Users\\VOTRE-NOM\\DossierBancaire\\`

3\. Relancez `DossierBancaire.exe` pour réinstaller proprement



\### Problème : Erreur "ModuleNotFoundError"



\*\*Cause :\*\* Installation des dépendances échouée



\*\*Solution :\*\*

1\. Supprimez `C:\\Users\\VOTRE-NOM\\DossierBancaire\\`

2\. Vérifiez votre connexion Internet

3\. Relancez avec les droits administrateur :

&nbsp;  - Clic droit sur `DossierBancaire.exe`

&nbsp;  - \*\*"Exécuter en tant qu'administrateur"\*\*



---



\## ❓ Questions fréquentes



\### Puis-je déplacer DossierBancaire.exe ?



\*\*Oui !\*\* Vous pouvez le mettre où vous voulez :

\- Bureau

\- Documents

\- Dossier dédié

\- Clé USB (mais l'installation Python restera sur C:\\)



\### L'application fonctionne-t-elle hors ligne ?



\*\*Partiellement :\*\*

\- \*\*Premier lancement\*\* : Internet \*\*requis\*\* (téléchargement Python + dépendances)

\- \*\*Lancements suivants\*\* : Internet \*\*recommandé\*\* (vérification mises à jour)

\- \*\*Utilisation\*\* : \*\*100% hors ligne\*\* (aucune connexion requise)



\### Combien de temps prend l'installation ?



\- \*\*Premier lancement\*\* : 2-3 minutes (selon connexion Internet)

\- \*\*Lancements suivants\*\* : 5-10 secondes

\- \*\*Avec mise à jour\*\* : 30 secondes



\### Puis-je utiliser l'application sur plusieurs PC ?



\*\*Oui !\*\* Copiez simplement `DossierBancaire.exe` sur chaque ordinateur. L'installation se fera automatiquement sur chaque machine.



\### Les mises à jour sont-elles automatiques ?



\*\*Oui !\*\* 

\- Le launcher vérifie GitHub au démarrage

\- Télécharge automatiquement si nouvelle version

\- Vous ne redistribuez \*\*jamais\*\* l'exe

\- Toujours la dernière version automatiquement



\### Puis-je voir le code source ?



\*\*Absolument !\*\* Le code est public sur GitHub :

\- \[Code de l'application](https://github.com/Gravelle68/dossier-bancaire/blob/main/app.py)

\- \[Code du launcher](https://github.com/Gravelle68/dossier-bancaire/blob/main/launcher\_script.py)



---



\## 📧 Support



\### Besoin d'aide ?



\- 📖 \*\*Documentation\*\* : \[README.md](https://github.com/Gravelle68/dossier-bancaire)

\- 🐛 \*\*Signaler un bug\*\* : \[Ouvrir une issue](https://github.com/Gravelle68/dossier-bancaire/issues)

\- 💬 \*\*Discussion\*\* : \[GitHub Discussions](https://github.com/Gravelle68/dossier-bancaire/discussions)



---



\## 🆚 Version Web vs Version Desktop



| Critère | Version Desktop (exe) | Version Web |

|---------|----------------------|-------------|

| \*\*Sécurité\*\* | ✅ 100% local | ⚠️ Données transitent par serveur |

| \*\*Installation\*\* | ⏱️ 2-3 min (1ère fois) | ✅ Aucune |

| \*\*Mises à jour\*\* | ✅ Automatiques | ✅ Instantanées |

| \*\*Usage offline\*\* | ✅ Oui (après install) | ❌ Non |

| \*\*Performance\*\* | ✅ Rapide | ⚠️ Dépend connexion |

| \*\*Compatibilité\*\* | 🪟 Windows uniquement | ✅ Tous OS |

| \*\*Recommandation\*\* | ✅ \*\*Pour vrais documents\*\* | ⚠️ \*\*Démo uniquement\*\* |



---



\## 📝 Notes de version



\### v1.0.0 - 15/10/2024



\*\*Première version publique\*\*



✨ Nouveautés :

\- Interface Streamlit moderne

\- Launcher avec Python embarqué

\- Auto-update intégré

\- Détection IA des cartes d'identité

\- Multi-upload drag \& drop

\- Page de garde personnalisable



🔒 Sécurité :

\- Tout fonctionne en local

\- Aucune donnée envoyée en ligne

\- Code source public



---



\*Dernière mise à jour : 15 octobre 2024\*


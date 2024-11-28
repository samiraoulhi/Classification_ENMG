# Résume 
L’objectif de ce travail est d’étudier et d’évaluer l’application des méthodes
de l’apprentissage automatique, à savoir la méthode ANN et la méthode SVM a la classification
automatique des signaux EMG et en particulier pour la détection du syndrome du canal
carpien.
Le dataset utilisé dans cette étude a été construit à partir des données obtenues d’un examen
de l’EMG/ENMG. L’application de ces modèles d’algorithme d’apprentissage automatique
ont produit des résultats d’entraînement et de prédiction très satisfaisants.
## construction du dataset 
Les données utilisées pour cette étude proviennent du service de Neurophysiologie de
l’Hôpital Spécialisé en Neurochirurgie Ali Ait Idir. Initialement collectées sous format PDF
pour environ 116 patients, elles ont été restructurées en format CSV afin de faciliter l’analyse.
Ces données ont été recueillies des examens ENMG et contiennent les principaux et
paramètres mesurés incluent la latence, l’amplitude, la durée et la vitesse de conduction motrice
et sensitive (détaillés au chapitre 1). Un autre critère important est la particularité du
quatrième doigt, qui est innervé par deux nerfs différents (médian et cubital). Cette particularité
permet de localiser précisément des lésions et de mieux comprendre les pathologies
sous-jacentes.
Ces données ont été insérées sous forme de lignes dans Excel puis analysées de manière
à obtenir un ensemble de données prêt à être utilisé pour la classification.
## Prétraitement des données
• Chargement du fichier de données
Le script charge un fichier CSV (voire section 3.2 pour plus d’information sur les
fichiers dataset créés) depuis le répertoire spécifié sur Google Drive en utilisant
la bibliothèque pandas.
• Encodage des données catégorielles
Les variables catégorielles sont encodées en utilisant LabelEncoder de scikitlearn.
Cela est nécessaire car de nombreux algorithmes d’apprentissage automatique
ne peuvent pas traiter directement les données catégorielles, elles doivent être
converties en valeurs numériques.
• Rééchantillonnage des données déséquilibrées
Comme nous avons constaté que la distribution des données selon les classes est
déséquilibrée, c’est-à-dire que certaines classes ont beaucoup plus d’exemples
que d’autres, nous avons opté pour ré-équilibrer les classes. Cela est fait en augmentant
le nombre d’échantillons des classes moins représentées.
• Séparation des ensembles de données
Les données sont divisées en ensembles d’entraînement, de validation et de test
pour évaluer les performances du modèle sous concept la validation croisée.
## architecture Proposé ANN
Le nombre de neurones d’entrées dépend de la version de dataset utilisée, c’est le
nombre de caractéristiques considérées. Pour le datasetV3, on a 25 caractéristiques,donc 25 neurone d’entrées.
Les quatre neurones de sortie représentent les quatre classes : Normal, Mild, Moderate,
Severe
La fonction d’activation utilisée pour tous les neurones de la couche d’entrée et des
couches cachées est la fonction ReLu. Pour la couche de sortie, la fonction softmax est
exploitée.
Afin d’éviter le problème de sur-apprentissage, nous avons utilisé trois méthodes de
régularisation :
• Dropout : Une technique qui consiste à désactiver aléatoirement une fraction des
neurones durant l’apprentissage, ici avec un taux de 0,3.
• BatchNormalization : Une technique de normalisation qui permet de stabiliser et
d’accélérer l’apprentissage en normalisant les activations des neurones.
• EarlyStopping : Une méthode qui arrête l’apprentissage lorsque la performance
sur les données de validation cesse de s’améliorer après un certain nombre d’époques,
ici configurée avec une patience de 10 époques.
L’apprentissage a été effectué en utilisant la méthode d’Adam avec un taux d’apprentissage
de 0.01 et la fonction Cross-entropy comme fonction Loss.
- implementation
• Construction du modèle
Les couches du modèle sont définies séquentiellement à l’aide de « Sequential ».
CHAPITRE 3. IMPLÉMENTATION ET ÉVALUATION DES MÉTHODES SVM
ET ANN POUR LA CLASSIFICATION DU CTS 39
Les différentes couches sont ajoutées, y compris une couche d’aplatissement
« Flatten » pour préparer les données,des couches entièrement connectées « Dense »
avec des fonctions d’activation « ReLU » des couches de « Dropout » pour la régularisation
et des couches de « Batch-normalisation » pour stabiliser et accélérer
l’entraînement.
• Compilation du modèle
Le modèle est compilé avec un optimiseur Adam, une fonction de perte « categoricalcrossentropy
» (adaptée à une classification multi-classe) et la métrique « accuracy
» pour évaluer les performances.
• Entraînement du modèle
Le modèle est entraîné sur les données d’entraînement avec « model.fit », spécifiant
le nombre d’époques, la taille du lot et les données de validation.
La progression de l’apprentissage est surveillée et l’entraînement peut être arrêté
prématurément si la perte de validation ne s’améliore pas avec « EarlyStopping ».
• Évaluation et Préduction du modèle
Les performances du modèle sont évaluées sur les données de test avec « model.
evaluate ».
L’historique de la précision et de la perte pendant l’entraînement est enregistré et
visualisé pour évaluer la performance du modèle.
Le modèle est utilisé pour faire des prédictions sur les données de test avec « model.
predict ».
Les prédictions sont évaluées en calculant la matrice de confusion et en affichant
un rapport de classification.
## Architecture prposé SVM
L’architecture multi-classe utilisée est « one-vs-all » (un contre tous). Dans cette approche,
un classifieur SVM est entraîné pour chaque classe, où cette classe est considérée comme positive
et toutes les autres classes sont considérées comme négatives. Ainsi, pour un problème
de classification à quatre classes (Normal, Mild, Moderate, Severe), quatre classifieurs SVM
distincts sont entraînés. Pour faire une prédiction, chaque classifieur donne une décision, et
la classe avec le score le plus élevé est choisie.
Cette méthode permet de transformer un problème de classification multiclasse en plusieurs
problèmes de classification binaire, simplifiant ainsi l’implémentation et l’entraînement
du modèle. Elle est particulièrement efficace lorsque les classes sont déséquilibrées, car
la pondération des classes « class_weigh- t=balanced » ajuste automatiquement les poids de
chaque classe en fonction de leur fréquence dans les données d’entraînement, assurant ainsi
une meilleure performance et une juste représentation de chaque classe dans les prédictions.
- Implémentation
  La classe SVC (Support Vector Classification) de scikit-learn permet de créer un classifieur
SVM avec différentes options de noyaux, telles que linéaire, polynomial, RBF (Radial
Basis Function) et sigmoïde. Elle offre également une flexibilité dans la régularisation et
la gestion du déséquilibre des classes via le paramètre class_weight. Avec « class_weight=
balanced », la bibliothèque ajuste automatiquement les poids des classes en fonction de
leur fréquence, ce qui est essentiel pour des datasets déséquilibrés.

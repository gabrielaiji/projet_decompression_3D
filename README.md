# OBJ augmenté

WaveFront OBJ est un format permettant d'encoder des modèles 3D de manière
simple. Cependant, il n'est pas adapté aux représentations progressives. Pour
cela, nous avons augmenté OBJ de nouvelles commandes qui permettent de modifier
le contenu préalablement déclaré.

## Utilisation

Vous pouvez récupérer les sources de cette application en lançant la commande
```
git clone https://gitea.tforgione.fr/tforgione/obja
```

À la racine de ce projet, le script `server.py` vous permet de démarrer un
server de streaming. Vous pouvez l'exécuter en lançant `./server.py`. Une fois
cela fait, vous pouvez allez sur [localhost:8000](http://localhost:8000) pour
lancer le streaming. Le navigateur télécharge progressivement les données et
les affiche.

Les modèles doivent être sauvegardés dans le dossiers `assets`, et peuvent être
visualisés en ajouter `?nom_du_modele.obj` à la fin de l'url. Par exemple,
[localhost:8000/?bunny.obj](http://localhost:8000/?bunny.obj) chargera le
modèle `bunny.obj` du dossier `assets`. Ce modèle est un modèle d'exemple, il
commence par encoder la version basse résolution du [Stanford
bunny](https://graphics.stanford.edu/data/3Dscanrep/), translate tous ses
sommets, les retranslate vers leurs positions d'origine puis supprime toutes
les faces.

## Commandes
###### Ajout d'un sommet

Comme dans le OBJ standard, pour ajouter un sommet, il suffit d'utiliser le
caractère `v` suivi des coordonnées du sommet. Par exemple :

```
v 1.0 2.0 3.0
```

###### Ajout d'une face

Comme dans le OBJ standard, pour ajouter une face, il suffit d'utiliser le
caractère `f` suivi des indices des sommets de la face. Par exemple :

```
v 0.0 0.0 0.0
v 1.0 0.0 0.0
v 1.0 1.0 0.0
f 1 2 3
```

**Attention :** en OBJ, les indices commencent à partir de 1

**Attention :** dans notre logiciel, seules les faces triangulaires sont
implémentées.

###### Edition d'un sommet

Notre format OBJ permet la modification d'un ancien sommet. Pour modifier un
sommet, il suffit d'utiliser les caractères `ev` suivis de l'indice du sommet à
modifier puis de ses nouvelles coordonées. Par exemple :

```
v 0.0 0.0 0.0
ev 1 1.0 1.0 1.0
```

###### Translation d'un sommet

De la même façon, un sommet peut être translaté grâce aux caractères `tv`. Par
exemple :

```
v 1.0 2.0 3.0
tv 1 1.0 1.0 1.0
```

###### Edition d'une face

Notre format OBJ permet la modification d'une ancienne face. Pour modifier une
face, il suffit d'utiliser les caractères `ef` suivis de l'indice de la face à
modifier puis des indices de ses nouveaux sommets. Par exemple :

```
v 0.0 0.0 0.0
v 1.0 0.0 0.0
v 1.0 1.0 0.0
v 1.0 1.0 1.0
f 1 2 3
ef 1 1 2 4
```

On peut aussi changer un seul sommet d'une face grâce aux caractères `efv`,
suivi de l'indice de la face à modifier, de l'indice du sommet à modifier (1, 2
ou 3) et de la nouvelle valeur du sommet. Par exemple :

```
v 0.0 0.0 0.0
v 1.0 0.0 0.0
v 1.0 1.0 0.0
v 1.0 1.0 1.0
f 1 2 3
efv 1 3 4
```

###### Suppression d'une face
Notre format OBJ permet la suppression d'une ancienne face. Pour supprimer une
face, il suffit d'utiliser les caracètres `df` suivis de l'indice de la face à
supprimer. Par exemple :

```
v 0.0 0.0 0.0
v 1.0 0.0 0.0
v 1.0 1.0 0.0
v 1.0 1.0 1.0
f 1 2 3
df 1
```

**Attention :** les indices des faces suivantes ne sont pas changés après la
suppression d'une ancienne face.

###### Triangle strips et triangle fans
Pour la compression de contenu 3D, on peut utiliser des [Triangle
Strips](https://en.wikipedia.org/wiki/Triangle_strip) et des [Triangle
Fans](https://en.wikipedia.org/wiki/Triangle_fan).

Notre format OBJ augmenté permet la déclaration de strips et de fans en
utilisant respectivement les caractères `ts` et `tf` suivis des indices des
sommets. Par exemple :

```
v -1.0 0.0 0.0
v -0.5 1.0 0.0
v 0.0 0.0 0.0
v 0.5 1.0 0.0
v 1.0 0.0 0.0
ts 1 2 3 4 5
```

ou bien

```
v 0.0 0.0 0.0
v -1.0 0.0 0.0
v -0.707 0.707 0.0
v 0.0 1.0 0.0
v 0.707 0.707 0.0
v 1.0 0.0 0.0
tf 1 2 3 4 5 6
```


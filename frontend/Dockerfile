FROM node:22

WORKDIR /app

# Copie package.json uniquement
COPY package.json .

# Copie séparée du lockfile, ce qui casse la couche si l'un OU l'autre change
COPY package-lock.json .

# Petite astuce : on force l'exécution de npm install à chaque build
# en utilisant une variable "build arg" qui change tout le temps
ARG CACHE_BUSTER=1
RUN echo "Reinstalling node modules - $CACHE_BUSTER" && npm install

# Ensuite le reste du code
COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev"]


# Commandes pour ajouter les packages nécessaires
    # docker compose down -v --remove-orphans
    # export CACHE_BUSTER=$(date +%s)
    # docker compose build --no-cache frontend
    # docker compose up
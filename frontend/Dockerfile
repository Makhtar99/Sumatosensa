FROM node:22

WORKDIR /app

COPY package*.json ./

RUN npm install

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]


# Commandes pour ajouter les packages nécessaires
    # docker compose down -v --remove-orphans
    # export CACHE_BUSTER=$(date +%s)
    # docker compose build --no-cache frontend
    # docker compose up
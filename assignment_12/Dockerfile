# ==========================================
# GIAI ĐOẠN 1: Build source code ReactJS
# ==========================================
FROM node:22-bookworm-slim AS builder

WORKDIR /app


COPY fe/my-nuxt-app/package*.json ./


RUN npm install


COPY fe/my-nuxt-app/ .


RUN npx nuxi generate
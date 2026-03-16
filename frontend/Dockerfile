# Stage 1: Build
FROM node:20-alpine AS build-env
WORKDIR /app

# Set backend URL for host access
ARG VITE_BACKEND_URL
ENV VITE_BACKEND_URL=${VITE_BACKEND_URL}

# Copy package files and install dependencies
COPY package*.json ./
RUN npm ci

# Copy source code
COPY . .

# Build Vite app (reads import.meta.env.VITE_BACKEND_URL)
RUN npm run build

# Stage 2: Production image
FROM node:20-alpine
WORKDIR /app

COPY --from=build-env /app/build ./build
COPY --from=build-env /app/node_modules ./node_modules
COPY --from=build-env /app/package.json ./package.json

ENV PORT=3001
EXPOSE 3001
CMD ["npm", "run", "start"]
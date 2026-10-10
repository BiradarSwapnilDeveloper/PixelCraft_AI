FROM node:20.18.2-alpine3.21 AS base
RUN apk upgrade --no-cache && \
    apk add --no-cache tini ffmpeg ca-certificates
WORKDIR /home/node/app

FROM base AS dependencies
COPY --chown=node:node package*.json ./
USER node
RUN --mount=type=cache,target=/home/node/.npm,uid=1000,gid=1000 \
    npm ci --ignore-scripts

FROM base AS builder
COPY --chown=node:node package*.json ./
COPY --from=dependencies /home/node/app/node_modules ./node_modules
COPY --chown=node:node . .
USER node
RUN npm run build --if-present

FROM base AS prod-dependencies
COPY --chown=node:node package*.json ./
USER node
RUN --mount=type=cache,target=/home/node/.npm,uid=1000,gid=1000 \
    npm ci --omit=dev --ignore-scripts

FROM base AS runner
ENV NODE_ENV=production
ENV PORT=3000

COPY --from=builder --chown=node:node /home/node/app ./
COPY --from=prod-dependencies --chown=node:node /home/node/app/node_modules ./node_modules

USER node
EXPOSE 3000
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["node", "."]
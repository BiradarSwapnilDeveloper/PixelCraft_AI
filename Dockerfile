FROM node:20.18.1-alpine3.20 AS base
RUN apk upgrade --no-cache && \
    apk add --no-cache tini ffmpeg

FROM base AS dependencies
RUN mkdir -p /home/node/app && chown -R node:node /home/node/app
USER node
WORKDIR /home/node/app
COPY --chown=node:node package*.json ./
RUN --mount=type=cache,target=/home/node/.npm,uid=1000,gid=1000 \
    npm ci --ignore-scripts

FROM base AS builder
RUN mkdir -p /home/node/app && chown -R node:node /home/node/app
USER node
WORKDIR /home/node/app
COPY --chown=node:node package*.json ./
COPY --from=dependencies --chown=node:node /home/node/app/node_modules ./node_modules
COPY --chown=node:node . .
RUN npm run build --if-present && rm -rf node_modules

FROM base AS prod-dependencies
RUN mkdir -p /home/node/app && chown -R node:node /home/node/app
USER node
WORKDIR /home/node/app
COPY --chown=node:node package*.json ./
RUN --mount=type=cache,target=/home/node/.npm,uid=1000,gid=1000 \
    npm ci --omit=dev --ignore-scripts

FROM base AS runner
ENV NODE_ENV=production
ENV PORT=3000

RUN rm -rf /usr/local/lib/node_modules/npm /usr/local/bin/npm /usr/local/bin/npx /usr/local/bin/corepack /opt/yarn* && \
    find / -xdev -perm /6000 -type f -exec chmod a-s {} \; 2>/dev/null || true

WORKDIR /home/node/app

COPY --from=builder --chown=root:node /home/node/app ./
COPY --from=prod-dependencies --chown=root:node /home/node/app/node_modules ./node_modules

RUN chmod -R 440 /home/node/app && \
    find /home/node/app -type d -exec chmod 550 {} +

USER node
EXPOSE 3000
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["node", "."]
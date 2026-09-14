FROM node:20.18.1-alpine3.20 AS base
RUN apk upgrade --no-cache && \
    apk add --no-cache tini

FROM base AS dependencies
WORKDIR /usr/src/app
COPY --chown=node:node package*.json ./
RUN --mount=type=cache,target=/home/node/.npm,uid=1000,gid=1000 \
    npm ci --ignore-scripts

FROM base AS builder
WORKDIR /usr/src/app
COPY --chown=node:node package*.json ./
COPY --from=dependencies --chown=node:node /usr/src/app/node_modules ./node_modules
COPY --chown=node:node . .
RUN npm run build --if-present

FROM base AS prod-dependencies
WORKDIR /usr/src/app
COPY --chown=node:node package*.json ./
RUN --mount=type=cache,target=/home/node/.npm,uid=1000,gid=1000 \
    npm ci --omit=dev --ignore-scripts

FROM base AS runner
ENV NODE_ENV=production
ENV PORT=3000

RUN rm -rf /usr/local/lib/node_modules/npm /usr/local/bin/npm /usr/local/bin/npx /usr/local/bin/corepack /opt/yarn* && \
    find / -xdev -perm /6000 -type f -exec chmod a-s {} \; 2>/dev/null || true

WORKDIR /usr/src/app

COPY --from=builder --chown=root:node /usr/src/app ./
COPY --from=prod-dependencies --chown=root:node /usr/src/app/node_modules ./node_modules

RUN chmod -R 440 /usr/src/app && \
    find /usr/src/app -type d -exec chmod 550 {} +

USER node
EXPOSE 3000
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["node", "."]
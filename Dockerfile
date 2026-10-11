FROM node:20.18.2-alpine3.21 AS base

SHELL ["/bin/ash", "-eo", "pipefail", "-c"]

RUN apk upgrade --no-cache && \
    apk add --no-cache tini ffmpeg ca-certificates && \
    mkdir -p /home/node/app && \
    chown -R node:node /home/node/app

WORKDIR /home/node/app

FROM base AS dependencies

WORKDIR /home/node/app
COPY --chown=node:node package*.json ./

USER node
RUN --mount=type=cache,target=/home/node/.npm,uid=1000,gid=1000 \
    npm ci --ignore-scripts

FROM base AS builder

WORKDIR /home/node/app
COPY --chown=node:node package*.json ./
COPY --from=dependencies --chown=node:node /home/node/app/node_modules ./node_modules
COPY --chown=node:node . .

USER node
RUN npm run build --if-present && rm -rf node_modules

FROM base AS prod-dependencies

WORKDIR /home/node/app
COPY --chown=node:node package*.json ./

USER node
RUN --mount=type=cache,target=/home/node/.npm,uid=1000,gid=1000 \
    npm ci --omit=dev --ignore-scripts

FROM base AS runner

SHELL ["/bin/ash", "-eo", "pipefail", "-c"]

ENV NODE_ENV=production \
    PORT=3000

WORKDIR /home/node/app

COPY --from=builder --chown=node:node /home/node/app ./
COPY --from=prod-dependencies --chown=node:node /home/node/app/node_modules ./node_modules

RUN sed -i '/^node:/s|/bin/.*sh|/sbin/nologin|' /etc/passwd && \
    find /home/node/app -type d -exec chmod 550 {} + && \
    find /home/node/app -type f -exec chmod 440 {} + && \
    find /home/node/app -type f -name "*.node" -exec chmod 550 {} + 2>/dev/null || true && \
    find / -xdev -type f \( -perm -4000 -o -perm -2000 \) -exec chmod a-s {} \; 2>/dev/null || true && \
    rm -rf /usr/local/lib/node_modules/npm /usr/local/bin/npm /usr/local/bin/npx /usr/local/bin/corepack /opt/yarn* /sbin/apk

USER node

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:' + (process.env.PORT || 3000) + '/health', (r) => process.exit(r.statusCode === 200 ? 0 : 1)).on('error', () => process.exit(1))"

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["node", "."]
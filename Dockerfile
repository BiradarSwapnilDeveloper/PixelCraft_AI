FROM node:20.18.1-alpine3.20 AS base
RUN apk upgrade --no-cache && \
    apk add --no-cache tini ffmpeg ca-certificates

FROM base AS dependencies
USER node
WORKDIR /home/node/app
COPY --chown=node:node package*.json ./
RUN --mount=type=cache,target=/home/node/.npm,uid=1000,gid=1000 \
    npm ci --ignore-scripts

FROM base AS builder
USER node
WORKDIR /home/node/app
COPY --chown=node:node . .
COPY --from=dependencies --chown=node:node /home/node/app/node_modules ./node_modules
RUN npm run build --if-present && rm -rf node_modules

FROM base AS prod-dependencies
USER node
WORKDIR /home/node/app
COPY --chown=node:node package*.json ./
RUN --mount=type=cache,target=/home/node/.npm,uid=1000,gid=1000 \
    npm ci --omit=dev --ignore-scripts

FROM base AS runner
ENV NODE_ENV=production
ENV PORT=3000

WORKDIR /home/node/app

COPY --from=builder --chown=root:node /home/node/app ./
COPY --from=prod-dependencies --chown=root:node /home/node/app/node_modules ./node_modules

RUN chown root:node /home/node/app && \
    sed -i '/^node:/s|/bin/.*sh|/sbin/nologin|' /etc/passwd && \
    chmod -R 440 /home/node/app && \
    find /home/node/app -type d -exec chmod 550 {} + && \
    find / -xdev -type f \( -perm -4000 -o -perm -2000 \) -exec chmod a-s {} \; 2>/dev/null || true && \
    rm -rf /usr/local/lib/node_modules/npm /usr/local/bin/npm /usr/local/bin/npx /usr/local/bin/corepack /opt/yarn* /sbin/apk /lib/apk /var/cache/apk /etc/apk

USER node
EXPOSE 3000
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["node", "."]
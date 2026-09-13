FROM node:20.18.1-alpine3.20 AS builder

RUN apk upgrade --no-cache

RUN mkdir -p /home/node/app && chown -R node:node /home/node/app

WORKDIR /home/node/app

USER node

COPY --chown=node:node package*.json ./

RUN npm ci --ignore-scripts

COPY --chown=node:node . .

RUN npm run build --if-present && rm -rf node_modules

FROM node:20.18.1-alpine3.20 AS prod-deps

RUN apk upgrade --no-cache

RUN mkdir -p /home/node/app && chown -R node:node /home/node/app

WORKDIR /home/node/app

USER node

COPY --chown=node:node package*.json ./

RUN npm ci --omit=dev --ignore-scripts && npm cache clean --force

FROM node:20.18.1-alpine3.20 AS runner

ENV NODE_ENV=production
ENV PORT=3000

RUN apk upgrade --no-cache && \
    apk add --no-cache tini && \
    rm -rf /usr/local/lib/node_modules/npm /usr/local/bin/npm /usr/local/bin/npx /usr/local/bin/corepack /opt/yarn*

WORKDIR /usr/src/app

COPY --from=builder --chown=root:node /home/node/app ./
COPY --from=prod-deps --chown=root:node /home/node/app/node_modules ./node_modules

RUN chown -R root:node /usr/src/app && \
    chmod -R 440 /usr/src/app && \
    find /usr/src/app -type d -exec chmod 550 {} +

USER node

EXPOSE 3000

ENTRYPOINT ["/sbin/tini", "--"]

CMD ["node", "."]
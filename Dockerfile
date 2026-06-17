FROM golang:1.26-alpine AS builder

# Устанавливаем необходимые пакеты
RUN apk add --no-cache git

WORKDIR /app

# Копируем go.mod из папки src
COPY src/go.mod ./

# Скачиваем зависимости
RUN go mod download

# Копируем весь исходный код из папки src
COPY src/ .

# ВАЖНО: Выполняем go mod tidy для синхронизации зависимостей
RUN go mod tidy

# Собираем приложение
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o moedelolk ./cmd/web

# Финальный образ
FROM alpine:latest

RUN apk --no-cache add \
    ca-certificates \
    chromium \
    nss \
    freetype \
    harfbuzz \
    ttf-dejavu \
    fontconfig \
    font-liberation

WORKDIR /root/
RUN mkdir -p /root/uploads

# Копируем бинарник
COPY --from=builder /app/moedelolk .

# Копируем фронтенд
COPY --from=builder /app/frontend ./frontend

EXPOSE 8080

CMD ["./moedelolk"]

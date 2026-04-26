#!/bin/sh
# Обгортка для Mac/Linux (God Mode: LocalStack + Real AWS + Kubernetes)

echo "[+] Запуск команди: $@"

# 1. Локальне середовище (LocalStack)
if [ "$1" = "tflocal" ]; then
    # Використовуємо фейкові ключі та прокидаємо мережу до LocalStack на хості
    docker run --rm -it \
        -v "$(pwd)":/workspace \
        --add-host s3.localhost.localstack.cloud:host-gateway \
        --add-host localhost.localstack.cloud:host-gateway \
        -e LOCALSTACK_HOST=host.docker.internal \
        -e LOCALSTACK_HOSTNAME=host.docker.internal \
        -e AWS_ENDPOINT_URL=http://host.docker.internal:4566 \
        -e AWS_ACCESS_KEY_ID=test \
        -e AWS_SECRET_ACCESS_KEY=test \
        -e AWS_SESSION_TOKEN=dummy \
        -e AWS_DEFAULT_REGION=eu-central-1 \
        -e LOCALSTACK_AUTH_TOKEN=$LOCALSTACK_AUTH_TOKEN \
        ironkage-iac-toolchain:latest "$@"
else
# 2. Бойове середовище (Terragrunt, Helm, AWS CLI)
    # Створюємо папку .kube на хості, якщо її немає (щоб Docker не створив її під root)
    mkdir -p ~/.kube

    # Монтуємо РЕАЛЬНІ ключі AWS та конфіги Kubernetes
    docker run --rm -it \
        -v "$(pwd)":/workspace \
        -v ~/.aws:/root/.aws \
        -v ~/.kube:/root/.kube \
        -e LOCALSTACK_AUTH_TOKEN=$LOCALSTACK_AUTH_TOKEN \
        ironkage-iac-toolchain:latest "$@"
fi

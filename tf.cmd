@echo off
:: Обгортка для Windows (God Mode: LocalStack S3 + K8s + Auto-Build)

echo [*] Перевірка/Збірка образу Toolchain...
docker build -q -t ironkage-iac-toolchain:latest -f Dockerfile.iac .

echo [+] Запуск команди: %*

:: 1. Локальне середовище (LocalStack)
:: (Команду 'aws' сюди більше не пускаємо, бо вона має логінитись у справжній ECR)
if "%1"=="tflocal" (
    docker run --rm -it ^
        -v "%cd%":/workspace ^
        --add-host s3.localhost.localstack.cloud:host-gateway ^
        --add-host localhost.localstack.cloud:host-gateway ^
        -e LOCALSTACK_HOST=host.docker.internal ^
        -e LOCALSTACK_HOSTNAME=host.docker.internal ^
        -e AWS_ENDPOINT_URL=http://host.docker.internal:4566 ^
        -e AWS_ACCESS_KEY_ID=test ^
        -e AWS_SECRET_ACCESS_KEY=test ^
        -e AWS_SESSION_TOKEN=dummy ^
        -e AWS_DEFAULT_REGION=eu-central-1 ^
        -e LOCALSTACK_AUTH_TOKEN=%LOCALSTACK_AUTH_TOKEN% ^
        ironkage-iac-toolchain:latest %*
) else (
:: 2. Бойове середовище (Terragrunt, Helm, AWS CLI)
    if not exist "%USERPROFILE%\.kube" mkdir "%USERPROFILE%\.kube"
    docker run --rm -it ^
        -v "%cd%":/workspace ^
        -v "%USERPROFILE%\.aws":/root/.aws ^
        -v "%USERPROFILE%\.kube":/root/.kube ^
        -e LOCALSTACK_AUTH_TOKEN=%LOCALSTACK_AUTH_TOKEN% ^
        ironkage-iac-toolchain:latest %*
)

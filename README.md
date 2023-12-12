## Установка

```bash
git clone https://github.com/lag-grunge/pyqtpdf
cd pyqtpdf
```

```bash
docker build -t pyqtpdf -f Dockerfile.arm .
```

## Запуск

### Запустить X-server

<details>
<summary>MacOS</summary>

- Установите <a href="https://www.xquartz.org/">XQuartz</a>
- Запустите XQuartz и внести адрес 127.0.0.1 в список разрешенных
```bash
open -a XQuartz
xhost +127.0.0.1
```
</details>

### Запустить контейнер
```bash
docker run -v \<папка с файлами, в которой лежат pdf\>:/mnt \
-v /tmp/.X11-unix:/tmp/.X11-unix \
-e DISPLAY=host.docker.internal:0 \
pyqtpdf
```
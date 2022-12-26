# Konachan Popular (Python)

This repository contains the source code of the backend program running the Telegram channel [@KonachanPopular](https://t.me/KonachanPopular).

<p align="center">
   <img src="https://user-images.githubusercontent.com/21986859/208772514-5c0d1c8d-6132-4dee-931c-9f2cca157ec5.png"/>
</p>

## Run in a Container

You will obviously first have to have an OCI-compatible container runtime like Podman or Docker installed. Then, pull and run the container (it's recommended to replace the `latest` tag with a specific version number for production use):

```shell
sudo podman run -e TELOXIDE_TOKEN=$TELOXIDE_TOKEN -e TELOXIDE_CHAT_ID=$TELOXIDE_CHAT_ID ghcr.io/k4yt3x/konachan-popular-python:latest
```

You can pass the settings either through environment variables or arguments. For details, see the help page of the binary:

```shell
sudo podman run ghcr.io/k4yt3x/konachan-popular-python:latest -h
```

# 3d-printed-Microscopes

> HMC 3D Printed Microscope monorepo

## Getting Started

`3d-printed-Microscopes` is a monorepo consisting of various projects
implemented onto the 3D printed microscope platform.

### Setting up direnv (optional)
1. Install [direnv] for your package manager or alternatively:
```sh
$ curl -sfL https://direnv.net/install.sh | bash
```
2. Once installed [hook direnv into your shell]
### Without direnv
```sh
$ python3 -m venv .venv
$ python3 -m pip install -r requirements.txt
$ source .venv/bin/activate
```

## Ongoing Project(s)

* FPM (Fourier Ptychographic Microscopy)

## REPO Structure

* To keep repo organized. Put all captured data in `datasets/` directory

[direnv]: https://direnv.net/
[hook direnv into your shell]: https://direnv.net/docs/hook.html

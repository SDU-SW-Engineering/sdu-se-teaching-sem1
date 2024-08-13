# Documents Related to the 1st Semester of the Software Educations

## Dependencies

Python 3 and the following packages (install via `pip`):
- [makeish](https://pypi.org/project/makeish/) at least version 0.3
- [json5](https://pypi.org/project/json5/)

## Building

```shell
./build.py
```

### Using Docker

Build image:

```shell
docker build -t sdu-se-teaching-sem1 .
```

Running `make` inside of docker image:

```shell
docker run --user "$(id -u):$(id -g)" -v `pwd`:/workdir sdu-se-teaching-sem1 ./build.py
```

## Development

To add a new document, open the [build script](doc/build.py), and add an entry to the `document_names` data structure. Make sure that you have a TeX document named according to the `source` field of the entry.

General styling is handled in a shared [file](doc/shared.tex).


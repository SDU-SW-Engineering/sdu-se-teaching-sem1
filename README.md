# Documents Related to the 1st Semester of the Software Educations

## Dependencies

Python 3 and the [makeish](https://pypi.org/project/makeish/) package (install via `pip`)

## Building

```shell
./build.py
```

## Development

To add a new document, open the [build script](doc/build.py), and add an entry to the `document_names` data structure. Make sure that you have a TeX document named according to the `source` field of the entry.

General styling is handled in a shared [file](doc/shared.tex).


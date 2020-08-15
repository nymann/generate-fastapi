# Generate FastAPI
*A code generation tool for FastAPI*

![Codecov](https://img.shields.io/codecov/c/gh/nymann/fastapi-code-generator)
![GitHub contributors](https://img.shields.io/github/contributors/nymann/fastapi-code-generator)

Uses [nymann/fastapi-template](https://github.com/nymann/fastapi-template) as a
base template.

Generates route(s) given an SQL migration file or JSON (see [examples](examples)).

```
$ generate_fastapi --help 
Usage: generate_fastapi [OPTIONS] FILE

Arguments:
  FILE  Path to a SQL upgrade migration or a JSON file  [required]

Options:
  --target-directory TEXT         Path to the target directory  [default: .]
  --project-name TEXT             Your project name fx. 'my_program'
                                  [required]

  --from_repo TEXT
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.

  --help                          Show this message and exit.
```

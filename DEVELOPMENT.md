# Misc Development Notes

## Requirements

Heroku buildpacks use plain `pip` for installing and do not support `poetry`. So, whenever we update `poetry.lock`, we also need to update `requirements.txt`.

CI/CD automation enforces that the two files stay in sync and should prevent merging if they do not effectively match.

To update `requirements.txt`, run:

```sh
poetry export -f requirements.txt --output requirements.txt
```

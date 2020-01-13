# Slow link checker is slow

Single-thread, scripty Python crawls a website and prints a YAML report of broken links. This program is mostly for educational purposes. There's a [multithreaded version here](https://github.com/victoriadrake/hydra-link-checker).

## Usage

Run in a terminal:

```sh
python find_broken.py [URL]
```

Ensure `URL` is an absolute url including schema, i.e. `https://example.com`.

The report will be [YAML](https://yaml.org/) formatted. To save the output to a file, run:

```sh
python find_broken.py [URL] > [PATH/TO/FILE.yaml]
```

You can add the current date to the filename using a command substitution, such as:

```sh
python find_broken.py [URL] > /path/to/$(date '+%Y_%m_%d')_report.yaml
```

To see how long the program takes to check your site, add `time`:

```sh
time python find_broken.py [URL]
```

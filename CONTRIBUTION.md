# CONTRIBUTION


```bash
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## As a CLI

```
Usage: md2pdf [OPTIONS] MD PDF

  md2pdf command line tool.

Options:
  --css PATH
  -e, --extras TEXT
  --version          Show the version and exit.
  --help             Show this message and exit.
```

For example, try to generate the project documentation with:
[Proteusz999.pdf](Proteusz999.pdf)
```bash
md2pdf README.md Proteusz999.pdf
```

Optionally, you may load an external style:

```bash
md2pdf --css tests/assets/input.css README.md README.pdf
```

And/or activate [markdown extras](https://github.com/trentm/python-markdown2/wiki/Extras):

```bash
md2pdf --css pygments.css -e fenced-code-blocks README.md README.pdf
```


### As a library

You can use `md2pdf` in your python code, like:

```python
from md2pdf.core import md2pdf

md2pdf(pdf,
       md=None,
       raw=None,
       css=None,
       base_url=None,
       extras=[],
)
```

Function arguments:

* `pdf`: output PDF file path
* `raw`: input markdown raw string content
* `md`: input markdown file path
* `css`: input styles path (CSS)
* `base_url`: absolute base path for markdown linked content (as images)
* `extras`: [markdown extras](https://github.com/trentm/python-markdown2/wiki/Extras) that should be activated

### With Docker

Install [Docker](https://www.docker.com/)

Pull the image:

```bash
docker pull jmaupetit/md2pdf
```

Now run your image:

```bash
docker run --rm \
    -v $PWD:/app \
    -u "$(id -u):$(id -g)" \
    jmaupetit/md2pdf --css styles.css INPUT.MD OUTPUT.PDF
```


## konwersja pdf na audiobook

+ [eBook to Audiobook Converter with Piper-tts](https://huggingface.co/spaces/drewThomasson/ebook2audiobookpiper-tts-GPU/blob/81daf8c663616945516abb0efd3738bc9932c183/README.md)

![img.png](img/text2audio.png)

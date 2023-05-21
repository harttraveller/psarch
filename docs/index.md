<style>
.md-typeset h1 {display: none;}
</style>

<div align="center">
<img src="assets/psarch.png" width=100 style="position: relative; left: -8px;">
<a href="https://github.com/harttraveller/psarch/blob/main/LICENSE" target="_blank">
<img src="https://img.shields.io/badge/license-MIT-blue" height=20 style="position: relative; top: -40px;">
</a>
<a href="https://www.python.org/downloads" target="_blank">
<img src="https://img.shields.io/badge/python-3.10-blue" height=20 style="position: relative; top: -40px;">
</a>
<a href="https://github.com/psf/black" target="_blank">
<img src="https://img.shields.io/badge/code%20style-black-black" height=20 style="position: relative; top: -40px;">
</a>
</div>

!!! abstract "Description"
    This python package allows you to run your own self hosted and searchable archive of reddit data.

![](assets/ps-meme.png)

!!! warning "Data Access"
    You will need to have archived the pushshift reddit archives before they were nuked in order to use this package. The functionality to download the data no longer works, cause the data is no longer available. If you don't have the data but would like to obtain a copy or use an alternative service, see [this](data.md) page.

!!! quote "Citation"
    If you use this package in an academic context, citation is appreciated. Also note this project is dependent on the [pushshift reddit dataset](https://arxiv.org/abs/2001.08435) for which a separate citation is recommended.

```bibtex title="BibTeX"
@online{psarch,
  title={psarch},
  author={Hart Traveller},
  year={2023},
  publisher={GitHub},
  url={https://github.com/harttraveller/psarch},
}
```



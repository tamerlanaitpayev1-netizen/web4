# Assignment 4 - Forms and Validation

**Aitpayev Tamerlan | IT-2510**

[English report (PDF)](Assignment4_Aitpayev_Tamerlan.pdf) | [GitHub repository](https://github.com/tamerlanaitpayev1-netizen/web4)

## Run

```sh
python serve.py
```

Open **http://127.0.0.1:8000/**. Python 3 is required; no packages need to be installed.

## Tasks

- `task1.html` - responsive train ticket form.
- `task2.html` - AITU Hack 2026 registration with native HTML validation.
- `task3.html` - accessible cafe reservation form.

The PDF contains screenshots, validation results, the original form audit and a conclusion. The pages use local Bootstrap and Montserrat resources, with their licenses included in `assets/`. No JavaScript is used in the pages.

`serve.py` handles the demonstration forms' POST requests and redirects to `completed.html`. Submitted data is discarded; no actual booking or registration is created.

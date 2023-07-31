<div align="center" markdown>

<img src="https://i.ibb.co/mTsnZVK/pdf-2image.png"/>

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#How-to-Use">How to Use</a> •
  <a href="#Test">Tests</a>
</p>

[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://https://supervisely.com/)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervise.ly/slack)

</div>

# Overview

Supervisely app for import folder with PDFs files as images. App based on Supervisely SDK.

#### Input files structure

You can upload a directory. Directory name defines project name. Subdirectories define dataset names.

Project directory example:

```
test_pdf
├── books
│   ├── book1.pdf
│   └── book2.pdf
├── magazine
│   ├── magazine1.pdf
│   └── another_magazine
│       ├── magazine2.pdf
│       ├── ...
│       └── magazine2.pdf
└── ground.pdf
```

As a result we will get project `test_pdf_project` with 3 datasets named: `ds0`(with ground.pdf) `books` and `magazine`.

# How to Run

**Step 1.** Set your supervisely envirement using [this](https://developer.supervisely.com/getting-started/environment-variables) instruction

**Step 2.** Clone this repository to your local folder

**Step 3.** Run app in debug mode using settings.json

**Step 4.** Go to localhost:8000 to use this app

**Step 5.** Drag'n'Drop your dataset.

**Step 6.** Create project in Supervisely and click 'Import' button

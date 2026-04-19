#!/bin/bash

set -e

pandoc resume.md -o resume.pdf --pdf-engine=weasyprint -c style.css

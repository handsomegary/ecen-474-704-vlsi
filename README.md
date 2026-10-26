# ECEN 474/704: Analog VLSI Circuit Design

Searchable LaTeX restorations of three Exam 1 sample papers, plus anonymized copies of six supplied laboratory prelab TeX sources. Each generated PDF is stored beside its corresponding TeX source. All public text is in English.

## Read the documents

Use the individual PDF links in the table below. Exam PDFs are named `content.pdf` beside `content.tex`; laboratory PDFs are named `prelab.pdf` beside `prelab.tex`.

The [official course page](https://people.engr.tamu.edu/spalermo/ecen474.html) links the sample exams. Its instructor and course attribution are preserved. The original exam PDFs supplied locally are scans without extractable text. The restoration retypes their printed questions and supplied handwritten solutions, redraws circuits and layout figures in TikZ/CircuitikZ, and retains their 6-, 6-, and 5-page sequences, including scratch pages. Cover arrangement, headings, question weights, formulas, and diagram placement follow the originals as closely as typesetting permits.

This is a reconstruction of the supplied solution documents. Small editorial notes distinguish rounding discrepancies from changes to the source answers. It is not a new official answer key or a claim that every answer has been independently validated by circuit simulation.

## Editable sources

| Material | Source | Generated PDF |
| --- | --- | --- |
| Spring 2018, February 13 | [content.tex](exams/spring-2018/content.tex) | [content.pdf](exams/spring-2018/content.pdf) |
| Fall 2016, September 29 | [content.tex](exams/fall-2016/content.tex) | [content.pdf](exams/fall-2016/content.pdf) |
| Spring 2016, February 24 | [content.tex](exams/spring-2016/content.tex) | [content.pdf](exams/spring-2016/content.pdf) |
| Lab 3 prelab | [prelab.tex](labs/lab-03/prelab.tex) | [prelab.pdf](labs/lab-03/prelab.pdf) |
| Lab 5 prelab | [prelab.tex](labs/lab-05/prelab.tex) | [prelab.pdf](labs/lab-05/prelab.pdf) |
| Lab 6 prelab | [prelab.tex](labs/lab-06/prelab.tex) | [prelab.pdf](labs/lab-06/prelab.pdf) |
| Lab 7 prelab | [prelab.tex](labs/lab-07/prelab.tex) | [prelab.pdf](labs/lab-07/prelab.pdf) |
| Lab 8 prelab | [prelab.tex](labs/lab-08/prelab.tex) | [prelab.pdf](labs/lab-08/prelab.pdf) |
| Lab 9 prelab | [prelab.tex](labs/lab-09/prelab.tex) | [prelab.pdf](labs/lab-09/prelab.pdf) |

The laboratory content follows the existing TeX rather than rebuilding the Word reports. Author headers, student-number fields, and initialed self-citations are anonymized. The three figure files required by Lab 3 were absent as separate files; they were recovered from its companion generated PDF and are included beside its TeX source. The other five sources have no external graphics dependencies.

The prelabs are analytical/reference documents. Their circuit calculations are not presented as freshly simulated results. Referenced laboratory reports and device data are not additionally uploaded. Source dates are retained as supplied.

## Rebuild from a fresh download

Install Python 3.10 or newer, XeLaTeX, TeX Gyre/Latin Modern fonts, and the LaTeX packages for AMS mathematics, New TX fonts, TikZ/CircuitikZ, geometry, graphics, captions, and hyperlinks.

On Debian or Ubuntu:

```sh
sudo apt-get update
sudo apt-get install texlive-xetex texlive-latex-extra texlive-science texlive-fonts-recommended texlive-fonts-extra texlive-plain-generic lmodern fonts-texgyre
python -m pip install -r requirements.txt
python tools/build.py --publish
python tools/verify_archive.py --pdf
```

The build runs two TeX passes per source and updates all nine PDFs in their source directories. The three exam chapters are compiled through [exams/main.tex](exams/main.tex), then separated into their original 6-, 6-, and 5-page papers. Each prelab is compiled directly. The intermediate combined exam PDF, compiler logs, and auxiliary files stay under `.build/`. No original course folder, personal path, or original scanned PDF is needed to rebuild.

With MiKTeX, install missing packages before building; automatic package installation is disabled during compilation. If XeLaTeX is not on the command search path, pass its executable through `--engine`.

Build one group when needed:

```sh
python tools/build.py --target exams --publish
python tools/build.py --target labs --publish
```

The exam directory also opens as a LaTeX project. The individual `content.tex` files are chapters included by `exams/main.tex`, rather than standalone entry points. A single prelab can be compiled directly from its own directory using XeLaTeX.

## Verification and source policy

[GitHub Actions](../../actions) checks the archive, rebuilds every public document on Linux, and inspects the generated text and metadata. Local review also compares the restored exam pages with their originals and checks the rendered prelabs for missing graphics, clipping, overlaps, and residual identity text.

[source-coverage.json](source-coverage.json) records the three exam papers and selected prelab sources. The public archive permits the nine generated PDF paths listed above; earlier generated collection paths are recognized only in Git history. Original exam scans, laboratory handouts, Word reports, report PDFs, agreement documents, and process files are not uploaded.

Personal identifiers are excluded from TeX, PDF metadata/text, filenames, and the recovered figure assets. The repository contains editable typeset text rather than full-page scan images. Source material remains in the local original folders.

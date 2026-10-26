# ECEN 474/704: Analog VLSI Circuit Design

Searchable LaTeX restorations of three Exam 1 sample papers, plus anonymized copies of six supplied laboratory prelab TeX sources and their regenerated PDF collection. All public text is in English.

## Read the documents

- **[Restored Exam 1 papers](exams/exam1-restored.pdf)**: Spring 2018, Fall 2016, and Spring 2016, in that order.
- **[Anonymous laboratory prelabs](labs/prelabs.pdf)**: Labs 3, 5, 6, 7, 8, and 9, with PDF bookmarks for each lab.

The [official course page](https://people.engr.tamu.edu/spalermo/ecen474.html) links the sample exams. Its instructor and course attribution are preserved. The original exam PDFs supplied locally are scans without extractable text. The restoration retypes their printed questions and supplied handwritten solutions, redraws circuits and layout figures in TikZ/CircuitikZ, and retains their 6-, 6-, and 5-page sequences, including scratch pages. Cover arrangement, headings, question weights, formulas, and diagram placement follow the originals as closely as typesetting permits.

This is a reconstruction of the supplied solution documents. Small editorial notes distinguish rounding discrepancies from changes to the source answers. It is not a new official answer key or a claim that every answer has been independently validated by circuit simulation.

## Editable sources

| Material | Source |
| --- | --- |
| Combined Exam 1 collection | [exams/main.tex](exams/main.tex) |
| Spring 2018, February 13 | [exams/spring-2018/content.tex](exams/spring-2018/content.tex) |
| Fall 2016, September 29 | [exams/fall-2016/content.tex](exams/fall-2016/content.tex) |
| Spring 2016, February 24 | [exams/spring-2016/content.tex](exams/spring-2016/content.tex) |
| Lab 3 prelab | [labs/lab-03/prelab.tex](labs/lab-03/prelab.tex) |
| Lab 5 prelab | [labs/lab-05/prelab.tex](labs/lab-05/prelab.tex) |
| Lab 6 prelab | [labs/lab-06/prelab.tex](labs/lab-06/prelab.tex) |
| Lab 7 prelab | [labs/lab-07/prelab.tex](labs/lab-07/prelab.tex) |
| Lab 8 prelab | [labs/lab-08/prelab.tex](labs/lab-08/prelab.tex) |
| Lab 9 prelab | [labs/lab-09/prelab.tex](labs/lab-09/prelab.tex) |

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

The build runs two TeX passes per source, merges the six freshly built prelabs, and updates the two public PDF collections. Intermediate PDFs, compiler logs, and auxiliary files stay under `.build/`. No original course folder, personal path, or original scanned PDF is needed to rebuild.

With MiKTeX, install missing packages before building; automatic package installation is disabled during compilation. If XeLaTeX is not on the command search path, pass its executable through `--engine`.

Build one group when needed:

```sh
python tools/build.py --target exams --publish
python tools/build.py --target labs --publish
```

The exam directory also opens as a LaTeX project. A single prelab can be compiled directly from its own directory using XeLaTeX. Individual generated prelab PDFs are available under `.build/lab-XX/`; the public collection provides all six in one file.

## Verification and source policy

[GitHub Actions](../../actions) checks the archive, rebuilds every public document on Linux, and inspects the generated text and metadata. Local review also compares the restored exam pages with their originals and checks the rendered prelabs for missing graphics, clipping, overlaps, and residual identity text.

[source-coverage.json](source-coverage.json) records the three exam papers and selected prelab sources. The only PDF paths allowed in the public repository are `exams/exam1-restored.pdf` and `labs/prelabs.pdf`. Original exam scans, laboratory handouts, Word reports, report PDFs, agreement documents, and process files are not uploaded.

Personal identifiers are excluded from TeX, PDF metadata/text, filenames, and the recovered figure assets. The repository contains editable typeset text rather than full-page scan images. Source material remains in the local original folders.

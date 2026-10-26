"""Check self-contained English TeX, privacy, source coverage, and rebuilt PDFs."""
import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
LABS = [3, 5, 6, 7, 8, 9]
EXAMS = {'spring-2018': 6, 'fall-2016': 6, 'spring-2016': 5}
PDF_PAGES = {f'exams/{name}/content.pdf': pages for name, pages in EXAMS.items()}
PDF_PAGES.update({f'labs/lab-{number:02d}/prelab.pdf': pages
                  for number, pages in zip(LABS, [7, 4, 7, 12, 6, 7])})
ALLOWED_PDFS = set(PDF_PAGES)
HISTORICAL_PDFS = {'exams/exam1-restored.pdf', 'labs/prelabs.pdf'}
CJK = re.compile('[' + chr(0x3400) + '-' + chr(0x4dbf)
                 + chr(0x4e00) + '-' + chr(0x9fff) + ']')
PRIVATE_PATH = re.compile(r'(?<![A-Za-z0-9])[A-Za-z]:[\\/]|/U[s]ers/|/h[o]me/')
STUDENT_ID = re.compile(r'(?i)\b(?:UIN|student\s*(?:ID|number))\s*[:=]\s*\d{9}\b')


def verify_text(text, location, private_patterns=()):
    assert not CJK.search(text), f'Non-English script: {location}'
    assert not PRIVATE_PATH.search(text), f'Private filesystem path: {location}'
    assert not STUDENT_ID.search(text), f'Possible student number: {location}'
    for pattern in private_patterns:
        assert pattern.casefold() not in text.casefold(), f'Private identifier: {location}'


def verify_pdf_paths(paths, historical=False):
    paths = {p for p in paths if Path(p).suffix.lower() == '.pdf'}
    allowed = ALLOWED_PDFS | HISTORICAL_PDFS if historical else ALLOWED_PDFS
    assert paths <= allowed, f'Unexpected/original PDFs: {paths - allowed}'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pdf', action='store_true')
    parser.add_argument('--private-patterns', type=Path,
                        help='Optional private local JSON array; never store it in this repository')
    args = parser.parse_args()
    private = json.loads(args.private_patterns.read_text(encoding='utf-8')) if args.private_patterns else []
    public = []
    for path in ROOT.rglob('*'):
        relative = path.relative_to(ROOT)
        if any(part in {'.git', '.build', '__pycache__'} for part in relative.parts):
            continue
        if not path.is_file():
            continue
        public.append(relative.as_posix())
        verify_text(relative.as_posix(), relative, private)
        assert path.suffix.lower() not in {'.docx', '.pptx', '.zip', '.l', '.lib'}, relative
        if path.suffix.lower() in {'.tex', '.md', '.json', '.py', '.yml', '.txt'}:
            text = path.read_text(encoding='utf-8')
            verify_text(text, relative, private)
            if path.suffix == '.tex':
                for command, target in re.findall(r'\\(input|include|includegraphics)(?:\[[^\]]*\])?\{([^}]+)\}', text):
                    dependency = path.parent / target
                    if command != 'includegraphics' and not dependency.suffix:
                        dependency = dependency.with_suffix('.tex')
                    assert dependency.is_file(), f'Missing dependency {target}: {relative}'
                    assert dependency.resolve().is_relative_to(ROOT.resolve()), relative
        else:
            for pattern in private:
                assert pattern.encode('utf-8').lower() not in path.read_bytes().lower(), relative
    verify_pdf_paths(public)
    coverage = json.loads((ROOT / 'source-coverage.json').read_text(encoding='utf-8'))
    assert coverage['prelab_numbers'] == LABS
    assert [row['pages'] for row in coverage['exam_1']] == [6, 6, 5]
    for number in LABS:
        source = ROOT / f'labs/lab-{number:02d}/prelab.tex'
        text = source.read_text(encoding='utf-8')
        assert 'Anonymous contributor' in text and 'pdfauthor={Anonymous contributor}' in text
    if (ROOT / '.git').exists() and shutil.which('git'):
        def git(*arguments):
            return subprocess.check_output(['git', *arguments], cwd=ROOT, text=True, encoding='utf-8')
        verify_pdf_paths(git('ls-files', '-z').split('\0'))
        if git('rev-list', '--all').strip():
            verify_pdf_paths((p.strip('\r\n') for p in
                              git('log', '--all', '--format=', '--name-only', '-z').split('\0')),
                             historical=True)
    print('PASS: three restored exams, six anonymous TeX prelabs, complete dependencies, PDF allowlist')
    if args.pdf:
        from pypdf import PdfReader
        for relative, count in PDF_PAGES.items():
            reader = PdfReader(ROOT / relative)
            assert len(reader.pages) == count, relative
            text = '\n'.join(p.extract_text() or '' for p in reader.pages)
            verify_text(text + str(reader.metadata), relative, private)
            assert 'ECEN 474/704' in text
            assert reader.metadata.author and 'Anonymous' in reader.metadata.author
            # Every page is typeset. Even blank exam scratch pages retain a text header.
            assert all(len(p.extract_text() or '') >= 15 for p in reader.pages), relative
            assert not reader.attachments, relative
            if relative.startswith('exams/'):
                assert not any(len(p.images) for p in reader.pages), 'Exam scans must not replace typeset pages'
            print(f'PASS: {relative}, {count} pages; searchable text and anonymous metadata')


if __name__ == '__main__':
    main()

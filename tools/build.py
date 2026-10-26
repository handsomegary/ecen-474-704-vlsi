"""Compile the restored exams and anonymous existing TeX prelabs."""
import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
LABS = (3, 5, 6, 7, 8, 9)


def compile_document(engine, source, label):
    output = ROOT / '.build' / label
    output.mkdir(parents=True, exist_ok=True)
    version = subprocess.run([engine, '--version'], capture_output=True, text=True,
                             encoding='utf-8', errors='replace')
    for number in (1, 2):
        command = [engine, '-interaction=nonstopmode', '-halt-on-error', '-file-line-error',
                   f'-output-directory={output}', str(source)]
        if 'miktex' in version.stdout.lower():
            command.insert(1, '--disable-installer')
        result = subprocess.run(command, cwd=source.parent, capture_output=True,
                                text=True, encoding='utf-8', errors='replace')
        (output / f'pass-{number}.txt').write_text(result.stdout + result.stderr, encoding='utf-8')
        if result.returncode:
            print(result.stdout[-8000:])
            raise SystemExit(f'Compilation failed: {label}; see {output}')
    log = (output / f'{source.stem}.log').read_text(encoding='utf-8', errors='replace')
    warnings = re.findall(r'^.*(?:Overfull \\[hv]box|Missing character:|'
                          r'LaTeX Warning:.*(?:undefined|multiply defined)|'
                          r'Label\(s\) may have changed).*$', log, flags=re.MULTILINE)
    pdf = output / f'{source.stem}.pdf'
    return pdf, warnings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--engine', default='xelatex')
    parser.add_argument('--target', choices=('all', 'exams', 'labs'), default='all')
    parser.add_argument('--publish', action='store_true')
    args = parser.parse_args()
    engine = shutil.which(args.engine)
    if not engine:
        parser.error('XeLaTeX is required; install it or select --engine')
    from pypdf import PdfReader, PdfWriter
    report = {}
    if args.target in ('all', 'exams'):
        pdf, warnings = compile_document(engine, ROOT / 'exams/main.tex', 'exams')
        reader = PdfReader(pdf)
        papers = json.loads((ROOT / 'source-coverage.json').read_text(encoding='utf-8'))['exam_1']
        assert len(reader.pages) == sum(paper['pages'] for paper in papers)
        report['exams'] = {'pages': len(reader.pages), 'warnings': warnings, 'papers': {}}
        offset = 0
        for paper in papers:
            writer = PdfWriter()
            for page in reader.pages[offset:offset + paper['pages']]:
                writer.add_page(page)
            writer.add_metadata({'/Title': f'ECEN 474/704 - Exam 1 - {paper["id"]}',
                                 '/Author': 'Anonymous study archive'})
            individual = ROOT / '.build' / f'{paper["id"]}.pdf'
            writer.write(individual)
            writer.close()
            report['exams']['papers'][paper['id']] = paper['pages']
            if args.publish and not warnings:
                shutil.copyfile(individual, ROOT / 'exams' / paper['id'] / 'content.pdf')
            offset += paper['pages']
        print(f'Exams: {report["exams"]["pages"]} pages; {len(warnings)} layout/reference warnings')
    if args.target in ('all', 'labs'):
        report['labs'] = {}
        for number in LABS:
            label = f'lab-{number:02d}'
            pdf, warnings = compile_document(engine, ROOT / 'labs' / label / 'prelab.tex', label)
            pages = len(PdfReader(pdf).pages)
            report['labs'][label] = {'pages': pages, 'warnings': warnings}
            if args.publish and not warnings:
                shutil.copyfile(pdf, ROOT / 'labs' / label / 'prelab.pdf')
            print(f'{label}: {pages} pages; {len(warnings)} layout/reference warnings')
    report_path = ROOT / '.build' / f'build-{args.target}.json'
    report_path.write_text(json.dumps(report, indent=2), encoding='utf-8')
    warnings = report.get('exams', {}).get('warnings', []) + [
        warning for row in report.get('labs', {}).values() for warning in row['warnings']]
    if warnings:
        print('\n'.join(warnings))
        raise SystemExit('Layout/reference issues require review before publication')
    print('PASS: requested documents compiled without layout/reference warnings')


if __name__ == '__main__':
    main()

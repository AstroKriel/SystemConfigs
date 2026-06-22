## { SCRIPT

##
## === DEPENDENCIES
##

## stdlib
import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

## local
from local_helpers import project_dirs

##
## === CONFIG
##

_RULES_DIR = project_dirs.SOURCES.rules
_DEFAULT_OUTPUT = Path.home() / "tmp" / "rules.pdf"
_SKIP = {"README.md"}

_PREAMBLE = r"""\documentclass[a4paper, 11pt]{article}
\usepackage{fontspec}
\setmonofont{DejaVu Sans Mono}[Scale=0.85]
\usepackage{geometry}
\usepackage{microtype}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{xcolor}
\usepackage{hyperref}
\usepackage{parskip}

\geometry{a4paper, top=2.5cm, bottom=2.5cm, left=3cm, right=3cm}
\hypersetup{colorlinks, linkcolor=black, urlcolor=black, pdfborder={0 0 0}}
\setcounter{secnumdepth}{0}
\setcounter{tocdepth}{2}

\definecolor{filegray}{gray}{0.45}

\providecommand{\tightlist}{%
  \setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}%
}
\providecommand{\passthrough}[1]{#1}

\newcommand{\firstfileheader}[3]{%
  \clearpage
  \addcontentsline{toc}{section}{#1}%
  \addcontentsline{toc}{subsection}{#2}%
  {\Large\bfseries\sffamily #1}\par
  \noindent\rule{\linewidth}{1.2pt}\par
  \vspace{8pt}%
  \noindent\rule{\linewidth}{0.5pt}\par
  \vspace{2pt}%
  {\large\bfseries #2}\quad{\small\ttfamily\color{filegray} #3}\par
  \vspace{2pt}%
  \noindent\rule{\linewidth}{0.5pt}\par
  \vspace{8pt}%
}

\newcommand{\fileheader}[2]{%
  \clearpage
  \addcontentsline{toc}{subsection}{#1}%
  \noindent\rule{\linewidth}{0.5pt}\par
  \vspace{2pt}%
  {\large\bfseries #1}\quad{\small\ttfamily\color{filegray} #2}\par
  \vspace{2pt}%
  \noindent\rule{\linewidth}{0.5pt}\par
  \vspace{8pt}%
}

\begin{document}
\tableofcontents
\clearpage
"""

_POSTAMBLE = r"\end{document}"

##
## === HELPERS
##


def _get_title(*, md_path: Path) -> str:
    for line in md_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return md_path.stem


def _strip_h1(*, content: str) -> str:
    result = []
    found = False
    for line in content.splitlines():
        if not found and line.startswith("# "):
            found = True
            continue
        result.append(line)
    return "\n".join(result)


def _convert_body(*, md_path: Path) -> str:
    content = _strip_h1(content=md_path.read_text(encoding="utf-8"))
    result = subprocess.run(
        ["pandoc", "-f", "gfm", "-t", "latex", "--shift-heading-level-by=-1", "--no-highlight"],
        input=content,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"pandoc failed on {md_path}: {result.stderr}")
    latex = result.stdout
    latex = re.sub(r"\\(section|subsection|subsubsection|paragraph)\{", r"\\\1*{", latex)
    return latex


def _escape_latex(*, text: str) -> str:
    for char, repl in [
        ("\\", r"\textbackslash{}"),
        ("&", r"\&"),
        ("%", r"\%"),
        ("$", r"\$"),
        ("#", r"\#"),
        ("_", r"\_"),
        ("{", r"\{"),
        ("}", r"\}"),
        ("~", r"\textasciitilde{}"),
        ("^", r"\textasciicircum{}"),
    ]:
        text = text.replace(char, repl)
    return text


def _format_group_label(*, group_key: str) -> str:
    return group_key.replace("/", " / ").replace("-", " ").title()


def _collect_groups(*, rules_dir: Path) -> list[tuple[str, list[Path]]]:
    groups: dict[str, list[Path]] = {}
    for md_path in sorted(rules_dir.rglob("*.md")):
        if md_path.name in _SKIP:
            continue
        rel_parent = md_path.relative_to(rules_dir).parent
        key = str(rel_parent) if rel_parent != Path(".") else ""
        groups.setdefault(key, []).append(md_path)
    return sorted(groups.items())

##
## === BUILD
##


def _build_tex(*, rules_dir: Path) -> str:
    parts = [_PREAMBLE]
    prev_top = None
    for group_key, files in _collect_groups(rules_dir=rules_dir):
        top = group_key.split("/")[0] if group_key else ""
        group_changed = top != prev_top
        if group_changed:
            prev_top = top
        for i, md_path in enumerate(files):
            title = _get_title(md_path=md_path)
            rel = str(md_path.relative_to(rules_dir))
            body = _convert_body(md_path=md_path)
            if i == 0 and group_changed:
                label = _format_group_label(group_key=top) if top else "General"
                parts.append(
                    f"\\firstfileheader{{{_escape_latex(text=label)}}}"
                    f"{{{_escape_latex(text=title)}}}"
                    f"{{{_escape_latex(text=rel)}}}"
                )
            else:
                parts.append(f"\\fileheader{{{_escape_latex(text=title)}}}{{{_escape_latex(text=rel)}}}")
            parts.append(body)
    parts.append(_POSTAMBLE)
    return "\n".join(parts)


def _compile_pdf(*, tex: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp = Path(tmp_dir)
        tex_path = tmp / "rules.tex"
        tex_path.write_text(tex, encoding="utf-8")
        for _ in range(2):
            result = subprocess.run(
                [
                    "lualatex",
                    "-interaction=nonstopmode",
                    "-output-directory", str(tmp),
                    str(tex_path),
                ],
                capture_output=True,
            )
            if result.returncode != 0 and not (tmp / "rules.pdf").exists():
                print(result.stdout.decode("utf-8", errors="replace")[-3000:], file=sys.stderr)
                raise RuntimeError("lualatex failed; see output above")
        shutil.copy(tmp / "rules.pdf", output_path)

##
## === PROGRAM MAIN
##


def run(*, output_path: Path) -> None:
    tex = _build_tex(rules_dir=_RULES_DIR)
    _compile_pdf(tex=tex, output_path=output_path)
    print(f"written: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compile all rules files into a single PDF for review.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=_DEFAULT_OUTPUT,
        help=f"Output PDF path (default: {_DEFAULT_OUTPUT})",
    )
    args = parser.parse_args()
    run(output_path=args.output)

##
## === ENTRY POINT
##

if __name__ == "__main__":
    raise SystemExit(main())

## } SCRIPT

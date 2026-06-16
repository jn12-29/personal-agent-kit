from __future__ import annotations

import importlib.util
import json
import sys
import subprocess
import zipfile
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = REPO_ROOT / "skills" / "manage-document-deliverables" / "scripts"


def load_script(name: str):
    path = SCRIPT_DIR / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def write_minimal_docx(path: Path) -> None:
    document_xml = """\
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:body>
    <w:p>
      <w:pPr><w:pStyle w:val="Heading1"/></w:pPr>
      <w:r><w:t>Sample Heading</w:t></w:r>
    </w:p>
    <w:p><w:r><w:t>Legacy Project TODO</w:t></w:r></w:p>
    <w:tbl>
      <w:tr>
        <w:tc><w:p><w:r><w:t>Col A</w:t></w:r></w:p></w:tc>
        <w:tc><w:p><w:r><w:t>Col B</w:t></w:r></w:p></w:tc>
      </w:tr>
      <w:tr>
        <w:tc><w:p><w:r><w:t>One</w:t></w:r></w:p></w:tc>
        <w:tc><w:p><w:r><w:t>Two</w:t></w:r></w:p></w:tc>
      </w:tr>
    </w:tbl>
  </w:body>
</w:document>
"""
    styles_xml = """\
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/></w:style>
</w:styles>
"""
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("word/document.xml", document_xml)
        archive.writestr("word/styles.xml", styles_xml)
        archive.writestr("word/_rels/document.xml.rels", '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"/>')


def test_help_is_self_describing():
    expected = {
        "md_to_docx": ["Examples:", "Style config JSON:", "--overwrite", "--reference-doc", "Exit codes"],
        "docx_to_md": ["Examples:", "--overwrite", "--media-dir", "Default output", "Exit codes"],
        "docx_inventory": ["Examples:", "--terms", "--dump-text", "Exit codes"],
    }

    for module_name, snippets in expected.items():
        module = load_script(module_name)
        help_text = module.build_parser().format_help()
        for snippet in snippets:
            assert snippet in help_text


def test_md_to_docx_refuses_to_overwrite(tmp_path: Path):
    module = load_script("md_to_docx")
    markdown = tmp_path / "report.md"
    output = tmp_path / "report.docx"
    markdown.write_text("# Title\n", encoding="utf-8")
    output.write_text("existing", encoding="utf-8")

    assert module.main([str(markdown), "-o", str(output)]) == 2


def test_md_to_docx_requires_pandoc_when_reference_doc_is_requested(tmp_path: Path):
    module = load_script("md_to_docx")
    markdown = tmp_path / "report.md"
    reference = tmp_path / "reference.docx"
    markdown.write_text("# Title\n", encoding="utf-8")
    reference.write_text("placeholder", encoding="utf-8")

    result = module.main([str(markdown), "--reference-doc", str(reference), "--pandoc-bin", str(tmp_path / "missing-pandoc")])

    assert result == 2


def test_md_to_docx_maps_pandoc_subprocess_failure_to_one(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    module = load_script("md_to_docx")
    markdown = tmp_path / "report.md"
    markdown.write_text("# Title\n", encoding="utf-8")
    fake_pandoc = tmp_path / "pandoc"
    fake_pandoc.write_text("#!/bin/sh\nexit 9\n", encoding="utf-8")

    monkeypatch.setattr(module.shutil, "which", lambda value: str(fake_pandoc))

    def fail_pandoc(*args, **kwargs):
        raise subprocess.CalledProcessError(9, ["pandoc"])

    monkeypatch.setattr(module.subprocess, "run", fail_pandoc)

    assert module.main([str(markdown), "--pandoc"]) == 1


def test_md_to_docx_rejects_invalid_style_config(tmp_path: Path):
    module = load_script("md_to_docx")
    markdown = tmp_path / "report.md"
    config = tmp_path / "style.json"
    markdown.write_text("# Title\n", encoding="utf-8")
    config.write_text(json.dumps({"unknown": {}}), encoding="utf-8")

    assert module.main([str(markdown), "--style-config", str(config)]) == 2


def test_md_to_docx_rejects_non_finite_style_numbers(tmp_path: Path):
    module = load_script("md_to_docx")
    markdown = tmp_path / "report.md"
    config = tmp_path / "style.json"
    markdown.write_text("# Title\n", encoding="utf-8")
    config.write_text('{"page": {"margin_cm": NaN}}', encoding="utf-8")

    assert module.main([str(markdown), "--style-config", str(config)]) == 2


def test_md_to_docx_rejects_non_finite_cli_numbers(tmp_path: Path):
    module = load_script("md_to_docx")
    markdown = tmp_path / "report.md"
    markdown.write_text("# Title\n", encoding="utf-8")

    with pytest.raises(SystemExit) as excinfo:
        module.main([str(markdown), "--margin-cm", "inf"])

    assert excinfo.value.code == 2


def test_md_to_docx_style_config_and_cli_overrides(tmp_path: Path):
    module = load_script("md_to_docx")
    config_path = tmp_path / "style.json"
    config_path.write_text(
        json.dumps(
            {
                "fonts": {"east_asia": "宋体", "latin": "Arial", "heading_east_asia": "黑体"},
                "page": {"margin_cm": 2.0},
                "image": {"max_width_inches": 4.0},
                "body": {"font_size_pt": 12, "line_spacing": 1.25},
                "headings": {"1": {"font_size_pt": 18, "alignment": "center"}},
            }
        ),
        encoding="utf-8",
    )

    parser = module.build_parser()
    args = parser.parse_args(
        [
            str(tmp_path / "report.md"),
            "--style-config",
            str(config_path),
            "--east-asia-font",
            "仿宋",
            "--max-image-width-inches",
            "3.5",
        ]
    )
    config = module.style_config_from_args(args)

    assert config.fonts.east_asia == "仿宋"
    assert config.fonts.latin == "Arial"
    assert config.page.left_margin_cm == 2.0
    assert config.image.max_width_inches == 3.5
    assert config.body.font_size_pt == 12
    assert config.headings[0].font_size_pt == 18


def test_docx_inventory_and_docx_to_md_read_minimal_docx(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    docx_path = tmp_path / "sample.docx"
    md_path = tmp_path / "sample.md"
    write_minimal_docx(docx_path)

    inventory = load_script("docx_inventory")
    assert inventory.main([str(docx_path), "--terms", "Legacy", "TODO"]) == 0
    inventory_output = capsys.readouterr().out
    assert "Sample Heading" in inventory_output
    assert "Legacy: 1" in inventory_output
    assert "TODO: 1" in inventory_output

    docx_to_md = load_script("docx_to_md")
    assert docx_to_md.main([str(docx_path), "-o", str(md_path), "--no-media"]) == 0
    markdown = md_path.read_text(encoding="utf-8")
    assert "# Sample Heading" in markdown
    assert "Legacy Project TODO" in markdown
    assert "| Col A | Col B |" in markdown


def test_docx_to_md_refuses_to_overwrite(tmp_path: Path):
    docx_path = tmp_path / "sample.docx"
    md_path = tmp_path / "sample.md"
    write_minimal_docx(docx_path)
    md_path.write_text("existing", encoding="utf-8")

    module = load_script("docx_to_md")

    assert module.main([str(docx_path), "-o", str(md_path)]) == 2


def test_md_to_docx_builtin_renderer_writes_configured_styles(tmp_path: Path):
    pytest.importorskip("docx")
    from docx import Document

    module = load_script("md_to_docx")
    markdown = tmp_path / "report.md"
    output = tmp_path / "report.docx"
    markdown.write_text(
        "# Report Title\n\nBody paragraph.\n\n![missing](missing.png)\n\n图1 Missing image\n",
        encoding="utf-8",
    )

    result = module.main(
        [
            str(markdown),
            "-o",
            str(output),
            "--east-asia-font",
            "宋体",
            "--latin-font",
            "Arial",
            "--margin-cm",
            "2.2",
        ]
    )

    assert result == 0
    document = Document(output)
    assert document.styles["Body Text"].font.name == "Arial"
    assert document.styles["Body Text"].font.size.pt == 11
    assert document.sections[0].left_margin.cm == pytest.approx(2.2, rel=0.01)
    assert "[Missing image: missing.png]" in "\n".join(paragraph.text for paragraph in document.paragraphs)


def test_md_to_docx_strict_assets_returns_one(tmp_path: Path):
    pytest.importorskip("docx")
    module = load_script("md_to_docx")
    markdown = tmp_path / "report.md"
    output = tmp_path / "report.docx"
    markdown.write_text("![missing](missing.png)\n", encoding="utf-8")

    assert module.main([str(markdown), "-o", str(output), "--strict-assets"]) == 1
    assert output.exists()

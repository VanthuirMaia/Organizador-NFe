import io
import json
import os
from pathlib import Path

from flask import Blueprint, flash, redirect, render_template, request, send_file, url_for

from ..models.nota_fiscal import NotaFiscal
from ..services.exportador import exportar_csv, exportar_excel
from ..services.pdf_parser import parse_pdf
from ..services.processador import detectar_duplicatas, organizar_arquivos
from ..services.xml_parser import parse_xml

bp = Blueprint('main', __name__)

_NOTAS_FILE = Path('notas_processadas.json')
_UPLOAD_DIR = Path('uploads')
_ORGANIZADO_DIR = Path('organizadas')


def _carregar_notas() -> list[NotaFiscal]:
    if _NOTAS_FILE.exists():
        with open(_NOTAS_FILE, 'r', encoding='utf-8') as f:
            return [NotaFiscal.from_dict(d) for d in json.load(f)]
    return []


def _salvar_notas(notas: list[NotaFiscal]) -> None:
    with open(_NOTAS_FILE, 'w', encoding='utf-8') as f:
        json.dump([n.to_dict() for n in notas], f, ensure_ascii=False, indent=2)


@bp.route('/')
def index():
    notas = _carregar_notas()
    duplicatas = sum(1 for n in notas if n.duplicata)
    return render_template('index.html', total=len(notas), duplicatas=duplicatas)


@bp.route('/processar', methods=['POST'])
def processar():
    files = request.files.getlist('arquivos')
    if not files or all(f.filename == '' for f in files):
        flash('Nenhum arquivo selecionado.', 'warning')
        return redirect(url_for('main.index'))

    _UPLOAD_DIR.mkdir(exist_ok=True)
    notas = _carregar_notas()
    processadas = erros = 0

    for f in files:
        if not f.filename:
            continue
        ext = Path(f.filename).suffix.lower()
        if ext not in ('.xml', '.pdf'):
            erros += 1
            continue

        destino = _UPLOAD_DIR / f.filename
        f.save(str(destino))

        nota = parse_xml(str(destino)) if ext == '.xml' else parse_pdf(str(destino))
        if nota:
            notas.append(nota)
            processadas += 1
        else:
            erros += 1

    notas = detectar_duplicatas(notas)
    _salvar_notas(notas)

    categoria = 'success' if processadas > 0 else 'warning'
    flash(f'{processadas} nota(s) processada(s). {erros} arquivo(s) com erro.', categoria)
    return redirect(url_for('main.notas'))


@bp.route('/notas')
def notas():
    todas = _carregar_notas()
    return render_template('notas.html', notas=todas)


@bp.route('/organizar', methods=['POST'])
def organizar():
    notas = _carregar_notas()
    if not notas:
        flash('Nenhuma nota para organizar.', 'warning')
        return redirect(url_for('main.notas'))

    _ORGANIZADO_DIR.mkdir(exist_ok=True)
    notas = organizar_arquivos(notas, str(_ORGANIZADO_DIR))
    _salvar_notas(notas)

    organizadas = sum(1 for n in notas if n.arquivo_organizado and not n.duplicata)
    flash(f'{organizadas} arquivo(s) copiados para "organizadas/".', 'success')
    return redirect(url_for('main.notas'))


@bp.route('/exportar/<formato>')
def exportar(formato: str):
    notas = _carregar_notas()
    if not notas:
        flash('Nenhuma nota para exportar.', 'warning')
        return redirect(url_for('main.notas'))

    if formato == 'excel':
        data = exportar_excel(notas)
        return send_file(
            io.BytesIO(data),
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='notas_fiscais.xlsx',
        )
    data = exportar_csv(notas)
    return send_file(
        io.BytesIO(data),
        mimetype='text/csv',
        as_attachment=True,
        download_name='notas_fiscais.csv',
    )


@bp.route('/limpar', methods=['POST'])
def limpar():
    if _NOTAS_FILE.exists():
        _NOTAS_FILE.unlink()
    flash('Lista de notas limpa com sucesso.', 'info')
    return redirect(url_for('main.index'))

from asyncio import run

from PyQt5.QtWidgets import QApplication, QFileDialog

from flask import render_template, request, session, jsonify, flash

from . import blueprint
from app.scanner.scanner import Scanner

total_files_to_scan = 0
total_scanned = 0
table_data = []
scan_path = ""


def file_explorer():
    global scan_path

    explorer = QApplication([])
    scan_path = QFileDialog.getExistingDirectory(None, "Select Directory")
    flash(scan_path)


@blueprint.route('/', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        print("hi")
        if request.form.get('get_directory') == 'get_directory':
            file_explorer()
        if request.form.get('run') == 'run':
            print("hi2")
            if not scan_path:
                flash('Please select a directory')
                return render_template('dashboard.html')

            data = {
                'pdf': request.form.get('flexSwitchCheckDefault1') == 'on',
                'excel': request.form.get('flexSwitchCheckDefault2') == 'on',
                'text': request.form.get('flexSwitchCheckDefault3') == 'on',
                'word': request.form.get('flexSwitchCheckDefault4') == 'on',
                'ssn': request.form.get('flexSwitchCheckDefault5') == 'on',
                'ccn': request.form.get('flexSwitchCheckDefault6') == 'on',
                'scan_path': scan_path,
                'custom_search': [
                    {
                        'name': name.strip(),
                        'regex': regex.strip()
                    }
                    for name, regex in zip(
                        request.form.getlist('custom_search_name'),
                        request.form.getlist('custom_search_regex')
                    )
                    if name.strip() and regex.strip()
                ]
            }
            print(data)
            Scanner(data).run()
    return render_template('dashboard.html')


@blueprint.route('/table-results', methods=['GET', 'POST'])
def table_results():
    if request.method == 'POST':
        row = request.json
        table_data.append(row)
        return ""
    return jsonify(table_data)


@blueprint.route('/pii-count', methods=['GET'])
def pii_count():
    return jsonify(len(table_data))


@blueprint.route('/total-files', methods=['GET', 'POST'])
def total_files():
    global total_files_to_scan

    if request.method == 'POST':
        total_files_to_scan = request.json
        return ""
    return jsonify(total_files_to_scan)


@blueprint.route('/total-files-scanned', methods=['GET', 'POST'])
def total_files_scanned():
    global total_scanned

    if request.method == 'POST':
        total_scanned = request.json
        return ""

    return jsonify(total_scanned)

import json

from flask import Flask, url_for, redirect, render_template, request

from server import fund_manager

app = Flask(__name__)


@app.route('/')
def index():
    managers = fund_manager.find_managers()
    # managers = sorted(managers.items(), key=lambda d: d[1], reverse=True)
    return render_template('test.html', message=json.dumps(managers),
                           manager_ids=json.dumps([int(_) for _ in managers.keys()]))


@app.route('/get_manager_times', methods=['POST'])
def get_manager_times():
    m_ids = request.form['m_ids'].strip()
    if m_ids[0] == '[':
        m_ids = m_ids[1:]
    if m_ids[-1] == ']':
        m_ids = m_ids[0:-1]
    m_ids = m_ids.split(',')
    m_datetime, start_date, end_date = fund_manager.get_manager_times(m_ids)
    return render_template('test.html', message=json.dumps(m_datetime), start_date=start_date, end_date=end_date,
                           manager_ids=request.form['m_ids'].strip())


@app.route('/get_manager_nav', methods=['POST'])
def get_manager_nav():
    m_ids = request.form['m_ids'].strip()
    if m_ids[0] == '[':
        m_ids = m_ids[1:]
    if m_ids[-1] == ']':
        m_ids = m_ids[0:-1]
    m_ids = m_ids.split(',')
    manager_nav = fund_manager.manager_nav(m_ids)
    return manager_nav


@app.route('/get_manager_asset', methods=['POST'])
def get_manager_asset():
    m_ids = request.form['m_ids'].strip()
    if m_ids[0] == '[':
        m_ids = m_ids[1:]
    if m_ids[-1] == ']':
        m_ids = m_ids[0:-1]
    m_ids = m_ids.split(',')
    manager_asset = fund_manager.manager_asset(m_ids)
    return manager_asset


@app.route('/get_manager_income', methods=['POST'])
def get_manager_income():
    m_ids = request.form['m_ids'].strip()
    if m_ids[0] == '[':
        m_ids = m_ids[1:]
    if m_ids[-1] == ']':
        m_ids = m_ids[0:-1]
    m_ids = m_ids.split(',')
    manager_income = fund_manager.manager_income(m_ids)
    return manager_income


@app.route('/get_manager_sector', methods=['POST'])
def get_manager_sector():
    m_ids = request.form['m_ids'].strip()
    if m_ids[0] == '[':
        m_ids = m_ids[1:]
    if m_ids[-1] == ']':
        m_ids = m_ids[0:-1]
    m_ids = m_ids.split(',')
    manager_sector = fund_manager.manager_sector(m_ids)
    return manager_sector


if __name__ == '__main__':
    app.run(host='10.76.0.165', port='5001')

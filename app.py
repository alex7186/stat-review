from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory
from datetime import date, datetime

from docx.shared import Inches, Pt
from docx import Document

import io, os.path, base64

import content_config
import calculation_logic.calculating_functions as functions
from db_manager import connection, cursor, add_log, get_latest_log

# Чертовски красивый снег
# Из окна идёт снег. Скоро все деревья им будут покрыты, и будет очень красиво.

app = Flask(__name__)
app.config['SECRET KEY'] = content_config.app_secret_key
app.secret_key = content_config.app_secret_key
app.config['UPLOAD_FOLDER'] = './uploads'


app.config['SESSION_TYPE'] = content_config.app_sessin_type
app.debug = content_config.app_debug

buf, document, intervals, absolute_frequency, result_file_name, a, k = None, None, None, None, None, None, None


variant_and_distribution = 0

@app.route('/', methods=('GET', 'POST'))
def index():

    global variant_and_distribution
    global buf, document, intervals, absolute_frequency, result_file_name, a, k
    content_list = [content_config.app_name, {}]
        

    # считываем вариант
    if variant_and_distribution == 0:
        variant = -1
        # вариант введен
        try:
            variant = int(request.form['variant'])
            variant_and_distribution = 0.5

        except Exception as e:
            variant_and_distribution = 0
            if variant != -1:
                flash(u'Что-то не так с номером варианта!', 'error')

        # вариант не введен, возвращаемся ко вводу
        if variant_and_distribution == 0:
            this_content = content_list
            this_content[1].update(content_config.variant_selection)
            return render_template(
                'index.html', 
                content_list=this_content, 
                latest= (('Вариант', 'Дата'), *get_latest_log(connection, cursor))
                )

        # вариант неверен, выводим сообщение
        if not variant in functions.available_vars:
            flash(u'Недопустимый номер варианта', 'error')


        # вариант верен, выводим распределение
        else:
            result_file_name, a, k = functions.get_variant(variant)
            document = Document()

            buf, document, intervals, absolute_frequency = functions.pre_return(
                result_file_name, 
                a, 
                k, 
                document, 
                content_config.color, )

            data = base64.b64encode(buf.getbuffer()).decode("ascii")


            this_content = content_list
            this_content[1].update(content_config.prepare_dist_selection(data))
            variant_and_distribution = 2
            return render_template(
                'index.html', 
                content_list=this_content, 
                latest= (('Вариант', 'Дата'), *get_latest_log(connection, cursor))
                )


    # страница скачивания и возврата к выбору варианта
    if variant_and_distribution <=2:
        distr_type = None
        try:
            distr_type = int(request.form['distr_type'])
        except:
            pass

        if distr_type:
            document.add_picture(buf, width=Inches(5.5))
            document.add_page_break()

            document = functions.post_return(
                document, 
                result_file_name, 
                distr_type, 
                a, 
                intervals, 
                k, 
                absolute_frequency)

            buf_document = io.BytesIO()
            document.save(buf_document)


            # сохраняем готовый файл
            with open('uploads/'+result_file_name, 'wb') as f:
                f.write(buf_document.getvalue())

            this_content = content_list

            this_content[1].update(content_config.prepare_download_link(a='/uploads/'+result_file_name, target=result_file_name))
            add_log(connection, cursor, variant_and_distribution, distr_type)

            variant_and_distribution = 0
            return render_template(
                'index.html', 
                content_list=this_content, 
                latest= (('Вариант', 'Дата'), *get_latest_log(connection, cursor)))


    variant = -1
    variant_and_distribution = 0
    this_content = content_list
    this_content[1].update(content_config.variant_selection)
    return render_template(
        'index.html', 
        content_list=this_content, 
        latest= (('Вариант', 'Дата'), *get_latest_log(connection, cursor)))


# путь скачивания файла
@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):

    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])

    return send_from_directory(directory=uploads, filename=result_file_name)

app.run(host='0.0.0.0', debug=app.debug)
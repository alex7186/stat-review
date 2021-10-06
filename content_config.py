color = (2/255, 117/255, 216/255)


app_secret_key = 'my secret key'
app_sessin_type = 'filesystem'
app_debug = False


app_name = 'Первичная статистическая обработка выборки'


content_list = [app_name, {}]

variant_selection = {
    'post0003': {
        'type':'form',
        'title':'Номер варианта',
        'content':[
            {'type':'input', 'input_type':'text', 'name':'variant', 'placeholder':'Введите вариат работы от 1 до 76'},
            {'type':'button', 'btntype':'submit', 'name':'Продолжить'}
            ]
        },
}

dist_selection = {
        'post0005': {
            'type':'form',
            'title':'Тип распределения:',
            'content':[
                {'type':'output', 'input_type':'show-image', 'src' : 000},
                {'type':'input', 'input_type':'radio', 'name':'distr_type', 'id':'0', 'value':'Показательное'},
                {'type':'input', 'input_type':'radio', 'name':'distr_type', 'id':'1', 'value':'Равномерное'},
                {'type':'input', 'input_type':'radio', 'name':'distr_type', 'id':'2', 'value':'Нормальное'},
                {'type':'button', 'btntype':'submit', 'name':'Продолжить'}
                ]
            },
    }

download_link = {
    'post0006':{
        'type' : 'form',
        'title' : 'Ваш отчет готов ✅',
        'content':[
            {'type':'output', 'input_type':'show-a', 'a':000, 'target':000},
            {'type':'button', 'btntype':'submit', 'name':'Вернуться к выбору варианта'}
        ]
    }
}

def prepare_dist_selection(src):
    dist_selection['post0005']['content'][0].update({'src':'data:image/png;base64,'+str(src)})
    return dist_selection

def prepare_download_link(a, target):
    download_link['post0006']['content'][0].update({'a':str(a), 'target':str(target)})
    return download_link

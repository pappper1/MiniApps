def navbar(request):
    return {
        'navbar': {
            'Конвертер валют': 'converter',
            'Погода': 'weather',
        }
    }
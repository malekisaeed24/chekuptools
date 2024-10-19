import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.shortcuts import render
import time

def get_resource_size_and_time(url):
    try:
        # اندازه و زمان دریافت HTML
        start_time = time.time()
        response = requests.get(url)
        load_time = time.time() - start_time
        html_size = len(response.content)

        # استفاده از BeautifulSoup برای استخراج منابع
        soup = BeautifulSoup(response.content, 'html.parser')

        # زمان و حجم منابع CSS
        css_resources = soup.find_all('link', rel='stylesheet')
        css_data = {'time': 0, 'size': 0}

        for css in css_resources:
            try:
                start_time = time.time()
                css_url = css['href']
                if not css_url.startswith('http'):
                    css_url = url + css_url
                css_response = requests.get(css_url)
                css_data['time'] += time.time() - start_time
                css_data['size'] += len(css_response.content)
            except:
                continue

        # زمان و حجم منابع JavaScript
        js_resources = soup.find_all('script', src=True)
        js_data = {'time': 0, 'size': 0}

        for js in js_resources:
            try:
                start_time = time.time()
                js_url = js['src']
                if not js_url.startswith('http'):
                    js_url = url + js_url
                js_response = requests.get(js_url)
                js_data['time'] += time.time() - start_time
                js_data['size'] += len(js_response.content)
            except:
                continue

        # زمان و حجم تصاویر
        img_resources = soup.find_all('img')
        img_data = {'time': 0, 'size': 0}

        for img in img_resources:
            try:
                start_time = time.time()
                img_url = img['src']
                if not img_url.startswith('http'):
                    img_url = url + img_url
                img_response = requests.get(img_url)
                img_data['time'] += time.time() - start_time
                img_data['size'] += len(img_response.content)
            except:
                continue

        return {
            'html': {'time': load_time, 'size': html_size},
            'css': css_data,
            'js': js_data,
            'img': img_data
        }
    except Exception as e:
        return {'error': str(e)}

def speed_test(request):
    if request.method == 'POST':
        url = request.POST.get('url')

        if not url:
            return JsonResponse({'error': 'لطفا آدرس سایت را وارد کنید'})

        if not url.startswith('http'):
            url = 'http://' + url

        results = get_resource_size_and_time(url)
        return JsonResponse(results)

    return render(request, 'speedload_app/speed_test.html')

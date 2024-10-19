import asyncio
import aiohttp
import time
from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.shortcuts import render


async def fetch_resource(session, url):
    async with session.get(url) as response:
        if response.status != 200:  # بررسی وضعیت پاسخ
            return None, 0
        content = await response.read()
        return content, len(content)  # بازگرداندن محتوا و اندازه آن


async def get_resource_size_and_time(url):
    async with aiohttp.ClientSession() as session:
        try:
            if not url.startswith('http'):
                url = 'http://' + url

            # دریافت HTML
            html_start = time.time()
            html_content, html_size = await fetch_resource(session, url)
            if html_content is None:
                return {'error': 'خطا در دریافت HTML'}

            html_time = time.time() - html_start

            soup = BeautifulSoup(html_content, 'html.parser')

            # برای CSS, JS و تصاویر
            css_data, js_data, img_data = [], [], []

            # CSS resources
            for css in soup.find_all('link', rel='stylesheet'):
                css_url = css['href']
                if not css_url.startswith('http'):
                    css_url = url + css_url
                start_time = time.time()
                _, size = await fetch_resource(session, css_url)
                css_data.append({'url': css_url, 'size': size, 'time': time.time() - start_time})

            # JS resources
            for js in soup.find_all('script', src=True):
                js_url = js['src']
                if not js_url.startswith('http'):
                    js_url = url + js_url
                start_time = time.time()
                _, size = await fetch_resource(session, js_url)
                js_data.append({'url': js_url, 'size': size, 'time': time.time() - start_time})

            # Image resources
            for img in soup.find_all('img'):
                img_url = img['src']
                if not img_url.startswith('http'):
                    img_url = url + img_url
                start_time = time.time()
                _, size = await fetch_resource(session, img_url)
                img_data.append({'url': img_url, 'size': size, 'time': time.time() - start_time})

            return {
                'html': {'time': html_time, 'size': html_size},
                'css': css_data,
                'js': js_data,
                'img': img_data
            }
        except Exception as e:
            print(f"Error processing URL {url}: {e}")
            return {'error': 'خطا در پردازش URL', 'details': str(e)}


def speed_test(request):
    if request.method == 'POST':
        url = request.POST.get('url')

        if not url:
            return JsonResponse({'error': 'لطفا آدرس سایت را وارد کنید'}, status=400)

        try:
            results = asyncio.run(get_resource_size_and_time(url))
            return JsonResponse(results)
        except Exception as e:
            print(f"Error processing URL {url}: {e}")
            return JsonResponse({'error': 'خطا در پردازش URL', 'details': str(e)}, status=500)

    return render(request, 'speedload_app/speed_test.html')

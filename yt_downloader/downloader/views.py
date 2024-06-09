from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
import youtube_dl

def index(request):
    return render(request, 'index.html')

def download(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        url = data['url']
        format = data['format']
        quality = data['quality']

        ydl_opts = {
            'format': 'bestvideo[height<=?{}]+bestaudio/best[height<=?{}]'.format(quality, quality) if format == 'mp4' else 'bestaudio/best',
            'outtmpl': '/tmp/%(title)s.%(ext)s',
            'noplaylist': True,
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', None)
            video_ext = 'mp4' if format == 'mp4' else 'mp3'
            file_name = f"{video_title}.{video_ext}"
            ydl_opts['outtmpl'] = f'/tmp/{file_name}'
            ydl.download([url])

        file_path = f'/tmp/{file_name}'
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type="video/mp4" if format == 'mp4' else "audio/mp3")
            response['Content-Disposition'] = f'attachment; filename={file_name}'
            return response

    return JsonResponse({'success': False, 'message': 'Invalid request'})

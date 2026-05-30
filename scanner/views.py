from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import tempfile
import os
import json
from parser import extract_resume_text
from analyzer import analyze_resume
from scanner.models import ScanResult

def home(request):
    recent_scans = ScanResult.objects.order_by('-created_at')[:5]
    return render(request, 'scanner/home.html', {'recent_scans': recent_scans})

@csrf_exempt
@require_POST
def scan(request):
    resume_file = request.FILES.get('resume')
    job_description = request.POST.get('job_description', '')

    if not resume_file or not job_description:
        return JsonResponse({'error': 'Please provide both a resume and job description.'}, status=400)

    ext = os.path.splitext(resume_file.name)[1].lower()
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        for chunk in resume_file.chunks():
            tmp.write(chunk)
        tmp_path = tmp.name

    try:
        resume_text = extract_resume_text(tmp_path)
        result = analyze_resume(resume_text, job_description)
        result_json = json.loads(result)

        ScanResult.objects.create(
            resume_filename=resume_file.name,
            job_description=job_description,
            match_score=result_json['match_score'],
            matched_skills=result_json['matched_skills'],
            missing_skills=result_json['missing_skills'],
            strengths=result_json['strengths'],
            improvements=result_json['improvements'],
            summary=result_json['summary'],
        )

        return JsonResponse(result_json)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)
    finally:
        os.unlink(tmp_path)
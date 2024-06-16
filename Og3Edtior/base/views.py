# views.py

from django.shortcuts import render

from django.http import JsonResponse, HttpResponseBadRequest
from g4f.client import Client
import json, os
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@csrf_exempt
def get_interview_answer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            whole_code = data.get('whole_code', '')
            selected_text = data.get('selected_text', '')
            query = data.get('query', '')
            print(query, whole_code, selected_text)

            client = Client()

            messages = [
                {"role": "system", "content": "You are a useful AI Agent For Move language. You need to give the code or instructions for move contract based on user query."},
            ]
            messages.append({
                "role": "user",
                "content": f""" NOTE: 
                                - the priority is Move Language only.
                                - Give me the code Based on user query.
                                - Don't give any other information, content, or any acknowledgment. Just give the answer.
                                - if the modifications are asked then only give the code dont give changes and instructions or any information just give the code.
                                - Just give the corrected code only.
                                - analyze the whole code and give the answer or corrected code which is by getting selected code
                                - if whole code is empty then consider it as a first message of file
                                - if the selected code is given then give the modified that selected code only dont give full of the code
                                - if not selected text then give or generate whole text
                                Very Important note:
                                - just give the code dont give the instructions
                                - dont give any of the text in japanese
                                Whole code: 
                                    `{whole_code}`
                                User Selected Code:
                                    `{selected_text}`    
                                User Question (or) Query:
                                    `{query}` 
                            """
            })

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=1000,
                stream=True,
            )

            output = ""
            for completion in response:
                try:
                    output += completion.choices[0].delta.content or ""
                except AttributeError:
                    pass
            print(output)

            return JsonResponse({'answer': output})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=400)



def code_editor(request):
    return render(request, 'code_editor.html')


def open_file(request):
    file_path = request.GET.get('file_path')
    full_path = os.path.join(BASE_DIR, file_path)

    if os.path.exists(full_path):
        with open(full_path, 'r') as file:
            content = file.read()
        return JsonResponse({'content': content})
    else:
        return JsonResponse({'error': 'File not found'}, status=404)

def save_file(request):
    if request.method == 'POST':
        file_path = request.POST.get('file_path')
        content = request.POST.get('content')
        full_path = os.path.join(BASE_DIR, file_path)

        with open(full_path, 'w') as file:
            file.write(content)
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


def explain(code):
    client = Client()
    messages = [
                {"role": "system", "content": "You are a useful AI Agent For Move language. You need give the documentation for given code."},
        ]
    messages.append({
            "role": "user",
            "content": f""" NOTE: 
                            Give me the clear explanation for given code.
                            CODE:
                            {code}
                        """
    })
    print(messages)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1000,
        stream=True,
    )
    code = ""
    for completion in response:
        try:
            code += completion.choices[0].delta.content or ""
        except AttributeError:
            pass
    return code


@csrf_exempt
def generate_solidity_code(request):
    if request.method == 'POST':
        client = Client()
        text_data = request.POST.get('text_data', '')
        lang = request.POST.get('selected_language', '')
        print(text_data, lang)
        messages = [
                {"role": "system", "content": f"You are a useful AI Agent For {lang} language. You need to convert the code into move contract based on given code."},
        ]
        messages.append({
                "role": "user",
                "content": f""" NOTE: 
                                - the priority is Move Language only.
                                - Give me the code Based on user query.
                                - Don't give any other information, content, or any acknowledgment. Just give the answer.
                                - if the modifications are asked then only give the code dont give changes and instructions or any information just give the code.
                                - convert the given phesudo code into the {lang}
                                CODE:
                                {text_data}
                            """
        })
        print(messages)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=1000,
            stream=True,
        )
        code = ""
        for completion in response:
            try:
                code += completion.choices[0].delta.content or ""
            except AttributeError:
                pass
        explain_code = explain(code)
        return JsonResponse({'solidity_code': code, 'explain':explain_code})
    else:
        return HttpResponseBadRequest("Only POST requests are allowed.")


def compile(request):
    return render(request, 'code_convention.html')


def scan(request):
    # MongoDB connection
    client = MongoClient('mongodb+srv://nagi:nagi@cluster0.ohv5gsc.mongodb.net/nagidb')
    db = client['Og3Collection']
    collection = db['Og3']

    # Fetch all documents from the collection
    documents = collection.find()
    uploaded_data = []
    for doc in documents:
        print(doc)
        uploaded_data.append({
            'file_path': doc.get('result', 'N/A'),  # Using .get() to avoid KeyError
            'file_root_hash': doc.get('data', 'N/A')  # Using .get() to avoid KeyError
        })

    # Pass the data to the template
    context = {
        'uploaded_data': uploaded_data
    }
    return render(request, 'Scan.html', context)

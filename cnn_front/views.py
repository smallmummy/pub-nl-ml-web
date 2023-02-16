# -*- coding: utf-8 -*-
import re
import os
import time
import json
import logging
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt  
from django.conf import settings
import numpy as np
from tensorflow.python.keras.preprocessing.sequence import pad_sequences

logger = logging.getLogger("django")
logger_service = logging.getLogger("django.service")


def runoob(request):
    context = {}
    baseurl = request.build_absolute_uri()
    context['baseurl'] = baseurl

    return render(request, 'index.html', context)


@csrf_exempt
def classify(request):

    if request.method == "POST":
        terms = request.body.decode()
        terms = re.sub(r";$", "", terms.strip())
        terms = terms.split(";")

        seq = settings.CNN_TOKENIZER.texts_to_sequences(terms)
        padded = pad_sequences(seq, padding='post', maxlen=settings.MAXLEN)
        pred = settings.CNN_MODEL.predict(padded)
        pred_ret = np.argmax(pred, axis=1) + 1

        return JsonResponse({
            "terms": terms,
            "pred_class": pred_ret.tolist()
        })

    else:
        return JsonResponse({"error": "POST only"})

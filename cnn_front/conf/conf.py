from cnn_front.func import wx


class C(object):
    XXXXX

class T(object):
    API_RET = {
        "status": None,
        "header": None,
        "ret": None
    }

    API_REQ_BODY_SUBMIT_TASK = {
        "file_link": None,
        "mode": None
    }

    API_REQ_BODY_FETCH_TASK = {
        "task_id": None
    }

    API_REQ_BODY_TRANSLATION = {
        "source_lang": None,
        "target_lang": None,
        "text": None
    }

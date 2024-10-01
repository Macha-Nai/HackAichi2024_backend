import requests
import json

def get_similar_mail_id(mail_title: str, mail_content: str) -> str:
    """
    メールのタイトル or 本文を受け取り，類似したメールのIDをRAGから受け取り，返す関数

    Parameters
    ----------
    mail_title : str
        メールのタイトル
    mail_content : str
        メールの本文
        
    Returns
    -------
    mail_id : str
        類似したメールのID
    """

    input_for_rag = mail_title + mail_content
    response = requests.post('http://rag_api-api-1:8889/v1/collections/my_collection/search', json={'input': input_for_rag})
    data = response.json()
    mail_id = json.dumps(data, ensure_ascii=False, indent=4)
    return mail_id

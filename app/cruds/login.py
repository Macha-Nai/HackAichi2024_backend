from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.utils import parsedate_to_datetime
import base64
import re


def get_body_from_parts(parts):
    if not parts:
        return ''
    for part in parts:
        if part.get('parts'):
            result = get_body_from_parts(part.get('parts'))
            if result:
                return result
        if part.get('mimeType') == 'text/plain':
            data = part.get('body', {}).get('data', '')
            if data:
                return base64.urlsafe_b64decode(data).decode('utf-8')
    return ''


def get_all_emails(access_token):
    creds = Credentials(token=access_token)
    service = build('gmail', 'v1', credentials=creds)
    messages = []
    query = 'in:inbox'

    try:
        response = service.users().messages().list(
            q=query, userId='me', maxResults=30).execute()
        if 'messages' in response:
            messages.extend(response['messages'])
        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(
                q=query, userId='me', pageToken=page_token).execute()
            if 'messages' in response:
                messages.extend(response['messages'])
        mail_list = []
        for msg in messages:
            try:
                msg_id = msg['id']
                message = service.users().messages().get(
                    userId='me', id=msg_id, format='full').execute()
                payload = message.get('payload', {})
                headers = payload.get('headers', [])
                parts = payload.get('parts', [])
                subject = next(
                    (header['value'] for header in headers if header['name'] == 'Subject'), '(No Subject)')
                from_ = next(
                    (header['value'] for header in headers if header['name'] == 'From'), 'Unknown')
                date = next(
                    (header['value'] for header in headers if header['name'] == 'Date'), None)

                match = re.match(r'(.*)<(.+)>', from_)
                if match:
                    your_name = match.group(1).strip().strip('"')
                    your_mail_address = match.group(2).strip()
                else:
                    your_name = from_.strip().strip('"')
                    your_mail_address = from_.strip()

                dt = parsedate_to_datetime(date)
                formatted_str = dt.strftime('%Y-%m-%d %H:%M:%S')

                body = get_body_from_parts(parts)
                mail_list.append([msg_id, subject, your_name,
                                 your_mail_address, body, formatted_str])
            except Exception as e:
                print(f'メッセージID {msg_id} の処理中にエラーが発生しました: {e}')
                continue
        return mail_list
    except Exception as error:
        print(f'エラーが発生しました: {error}')
        return []


def decode_base64(data):
    decoded_bytes = base64.urlsafe_b64decode(data.encode('ASCII'))
    try:
        decoded_str = decoded_bytes.decode('utf-8')
    except UnicodeDecodeError:
        decoded_str = decoded_bytes.decode('latin1')
    return decoded_str

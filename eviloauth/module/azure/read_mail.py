from typing import Any, List

import logging

import requests


def print_normal(emails, email_count):
    count = 0
    for email in emails:
        count += 1
        if count > email_count and email_count != -1:
            break
        print(email)


def print_emails(emails, email_count, mode='normal'):
    if mode == 'normal':
        print_normal(emails, email_count)


def __load__():
    print('LOADED read_mail')
    pass


def __run__(cache, i):
    print('RUNNING read_mail')
    access_tokens = list(cache.iterkeys())
    access_token_id = (access_tokens + [None])[0]

    if access_token_id:
        print(f'Using ID "{access_token_id}"')
        access_token = cache.get(access_token_id)

        email_count = 10

        graph_url = 'https://graph.microsoft.com/v1.0/me/messages'
        graph_headers = {
            'Authorization': f'Bearer {access_token.raw_token}'
        }

        emails: list[Any] = []

        # Download until count reached or no emails remaning
        # Always download 10 at a time
        while True:
            graph_response = requests.get(graph_url, headers=graph_headers)

            emails_resp = graph_response.json()

            emails_context = emails_resp.get('@odata.context')
            emails_value = emails_resp.get('value')
            emails_next_link = emails_resp.get('@odata.nextLink')

            emails = emails + emails_value

            if not emails_next_link or (email_count != -1 and len(emails) >= email_count):
                break

            graph_url = emails_next_link

        print_emails(emails, email_count)

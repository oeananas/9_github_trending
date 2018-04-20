import requests
import json
import datetime


def get_last_week_date():
    now_date = datetime.date.today()
    delta = datetime.timedelta(days=7)
    last_week_date = now_date - delta
    return last_week_date.isoformat()


def get_trending_repositories(last_week_date, top_size):
    params = {'q': 'created:>{}'.format(last_week_date), 'sort': 'stars'}
    response = requests.get(
        'https://api.github.com/search/repositories',
        params=params
    )
    repositories = json.loads(response.content)['items']
    top_repositories = repositories[:top_size]
    return top_repositories


def get_open_issues_amount(repo_full_name):
    response = requests.get(
        'https://api.github.com/repos/{}/issues'.format(repo_full_name)
    )
    for response_info in json.loads(response.content):
        return response_info['number']


if __name__ == '__main__':
    last_week_date = get_last_week_date()
    top_size = 20
    trending_repositories = get_trending_repositories(last_week_date, top_size)
    print('list of the most trending repositories for last week: \n')
    try:
        for repo_info in trending_repositories:
            full_name = repo_info['full_name']
            repo_url = repo_info['html_url']
            issues_count = get_open_issues_amount(full_name)
            print('url: {}, open issues: {}'.format(repo_url, issues_count))
    except TypeError:
        exit('query limit exceeded')

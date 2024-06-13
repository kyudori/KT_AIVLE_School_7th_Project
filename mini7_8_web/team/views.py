from django.shortcuts import render

def team_view(request):
    team_members = [
        {
            'name': '김아영',
            'track': 'AI Track',
            'role': 'Team Leader / Frontend',
            'image': 'images/member1.gif'
        },
        {
            'name': '김성규',
            'track': 'AI Track',
            'role': 'Backend',
            'image': 'images/member2.gif'
        },
        {
            'name': '문동규',
            'track': 'AI Track',
            'role': 'Backend',
            'image': 'images/member3.gif'
        },
        {
            'name': '박성훈',
            'track': 'AI Track',
            'role': 'Backend',
            'image': 'images/member4.gif'
        },
        {
            'name': '박종범',
            'track': 'AI Track',
            'role': 'Backend',
            'image': 'images/member5.gif'
        },
        {
            'name': '정주영',
            'track': 'AI Track',
            'role': 'Server Administrator',
            'image': 'images/member6.gif'
        },
        {
            'name': '하세호',
            'track': 'AI Track',
            'role': 'Frontend',
            'image': 'images/member7.gif'
        },
        {
            'name': '한규현',
            'track': 'AI Track',
            'role': 'Backend',
            'image': 'images/member8.gif'
        }
    ]
    return render(request, 'team/team.html', {'team_members': team_members})

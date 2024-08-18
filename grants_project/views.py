from django.shortcuts import render
from django.http import JsonResponse
from .models import Project, Grant
from rest_framework.decorators import api_view
from tr3_token.views import mint_token
from django.utils import timezone
from tr3_token.views import approve_token, revenue_commission, validator_reward

# Get projects scoped by grant
@api_view(['GET'])
def get_projects(request, grant_id):
    check_grant_end_date(grant_id)
    grant_filter = Grant.objects.filter(pk=grant_id)
    if not grant_filter.exists():
        return JsonResponse({'status': 'error', 'message': 'Grant not found'})
    
    grants = Grant.objects.get(pk=grant_id)
    projects = Project.objects.filter(grant = grants)
    data = []
    for project in projects:
        if project.days_remaining() <= 0:
            day = "Project has ended"
        else:
            day = project.days_remaining()

        data.append({
            'id': project.id,
            'project_name': project.name,
            'project_description': project.description,
            'start_time': project.start_time,
            'end_time': project.end_time,
            'current_fund': project.current_fund,
            'total_contributors': project.total_contributors,
            'team_members': project.team_members,
            'remaining_days': day,
            'created_by': project.created_by,
            'created_at': project.created_at,
            'updated_at': project.updated_at,
            'grant': project.grant.id,
            'aim': project.aim,
            'timeline': project.timeline,
            'status': project.status
        })
    return JsonResponse({'status': 'success', 'data': data})

# Get projects by id
@api_view(['GET'])
def get_project_by_id(request, project_id):
    project_filter = Project.objects.filter(pk=project_id)
    if not project_filter.exists():
        return JsonResponse({'status': 'error', 'message': 'Project not found'})
    
    project = Project.objects.get(pk=project_id)
    data = {
        'id': project.id,
        'project_name': project.name,
        'project_description': project.description,
        'start_time': project.start_time,
        'end_time': project.end_time,
        'current_fund': project.current_fund,
        'total_contributors': project.total_contributors,
        'team_members': project.team_members,
        'remaining_days': project.days_remaining(),
        'created_by': project.created_by,
        'created_at': project.created_at,
        'updated_at': project.updated_at,
        'grant': project.grant.id,
        'aim': project.aim,
        'timeline': project.timeline,
        'status': project.status
    }
    return JsonResponse({'status': 'success', 'data': data})

# Get all projects
@api_view(['GET'])
def get_all_projects(request):
    projects = Project.objects.all()
    data = []
    for project in projects:
        if project.days_remaining() <= 0:
            day = "Project has ended"
        else:
            day = project.days_remaining()

        data.append({
            'id': project.id,
            'project_name': project.name,
            'project_description': project.description,
            'start_time': project.start_time,
            'end_time': project.end_time,
            'current_fund': project.current_fund,
            'total_contributors': project.total_contributors,
            'team_members': project.team_members,
            'remaining_days': day,
            'pdf': project.pdf_uploaded,
            'created_by': project.created_by,
            'created_at': project.created_at,
            'updated_at': project.updated_at,
            'grant': project.grant.id,
            'aim': project.aim,
            'timeline': project.timeline,
            'status': project.status
        })
    return JsonResponse({'status': 'success', 'data': data})

# Get all grants
@api_view(['GET'])
def get_all_grants(request):
    grants = Grant.objects.all()
    print(grants)

    data = []
    for grant in grants:
        check_grant_end_date(grant.id)

        if grant.days_remaining() <= 0:
            day = "Grant has ended"
        else:
            day = grant.days_remaining()


        grant_data = {
            'id': grant.id,
            'organisation': grant.organisation,
            'program_name': grant.program_name,
            'description': grant.description,
            'start_fund': grant.start_fund,
            'end_fund': grant.end_fund,
            'remaining_days': day,
            'matching_pool': grant.matching_pool,
            'created_at': grant.created_at,
            'updated_at': grant.updated_at
        }
        data.append(grant_data)

    return JsonResponse({'status': 'success', 'data': data})

# Get grant by id
@api_view(['GET'])
def get_grant(request, grant_id):
    check_grant_end_date(grant_id)
    grant_filter = Grant.objects.filter(pk=grant_id)
    if not grant_filter.exists():
        return JsonResponse({'status': 'error', 'message': 'Grant not found'})
    
    grant = Grant.objects.get(pk=grant_id)

    if grant.days_remaining() <= 0:
        day = "Grant has ended"
    else:
        day = grant.days_remaining()

    data = {
        'id': grant.id,
        'organisation': grant.organisation,
        'program_name': grant.program_name,
        'description': grant.description,
        'start_fund': grant.start_fund,
        'end_fund': grant.end_fund,
        'remaining_days': day,
        'matching_pool': grant.matching_pool,
        'created_at': grant.created_at,
        'updated_at': grant.updated_at
    }
    return JsonResponse({'status': 'success', 'data': data})

@api_view(['POST'])
def create_grant(request):
    data = request.data

    organisation = data.get('organisation')
    program_name = data.get('program_name')
    description = data.get('description')
    start_fund = data.get('start_fund')
    end_fund = data.get('end_fund')
    matching_pool = data.get('matching_pool')

    if not organisation or not program_name or not description or not start_fund or not end_fund or not matching_pool:
        return JsonResponse({'status': 'error', 'message': 'Missing required fields'})

    existing_grant = Grant.objects.filter(program_name=program_name)
    if existing_grant.exists():
        return JsonResponse({'status': 'error', 'message': 'Grant already exists'})

    grant = Grant.objects.create(
        organisation=organisation,
        program_name=program_name,
        description=description,
        start_fund=start_fund,
        end_fund=end_fund,
        matching_pool=matching_pool
    )

    if not grant:
        return JsonResponse({'status': 'error', 'message': 'Failed to create grant'})
    
    # Mint token for the matching pool to temperory wallet
    mint_token(matching_pool)

    return JsonResponse({'status': 'success', 'message': 'Grant created successfully'})

# Always check grant end date
def check_grant_end_date(grant_id):
    grant = Grant.objects.get(pk=grant_id)
    if grant.end_fund < timezone.now():
        # Get list of projects
        projects = Project.objects.filter(grant=grant)
        for project in projects:
            # Grant has ended, approve the token
            approve_token(project.current_fund, grant.matching_pool)

            # Get Revenue
            revenue_commission(grant.id)

            # Reward Validator
            validator_reward(project.id)

            # Update project status
            project.status = 'completed funded'
            project.save()



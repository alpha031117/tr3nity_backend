from django.shortcuts import render
from django.http import JsonResponse
from .models import Vote, vote_history, Validator
from grants_project.models import Project
from datetime import datetime
from rest_framework.decorators import api_view

# Vote for project
@api_view(['POST'])
def vote_project(request):
    try:
        data = request.data
        project_id = data.get('project_id')
        validator_addrs = data.get('validator_address')
        vote_choice = data.get('vote_choice')

        # Check if all required fields are present
        if not project_id or not validator_addrs or not vote_choice:
            return JsonResponse({'status': 'error', 'message': 'Missing required fields'})
        
        # Validate validator's address is valid
        if not Validator.objects.filter(validator_address=validator_addrs).exists():
            return JsonResponse({'status': 'error', 'message': 'Validator not found'})
        
        # Get the project
        project = Project.objects.get(pk=project_id)

        # Check if the validator has already voted for this project
        if vote_history.objects.filter(project=project, validator_address=validator_addrs).exists():
            return JsonResponse({'status': 'error', 'message': 'Validator has already voted for this project'})
        
        # Validate vote choice
        if vote_choice.lower() not in ["yes", "no"]:
            return JsonResponse({'status': 'error', 'message': 'Invalid vote choice'})
        
        # Get the vote instance for the project
        vote = Vote.objects.get(project=project)

        # Update vote counts based on the choice
        if vote_choice.lower() == "yes":
            vote.total_yes += 1
            bridging_vote = 1
        else:
            vote.total_no += 1
            bridging_vote = 2
        
        vote.total_votes += 1
        
        # Save the updated vote counts
        vote.save()

        # Record the vote in history
        vote_history.objects.create(
            project=project,
            validator_address=validator_addrs,
            vote=vote,
            vote_result=bridging_vote,
            vote_date=datetime.now()
        )

        return JsonResponse({'status': 'success', 'message': 'Voted successfully'})
    
    except Project.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Project not found'})
    except Vote.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Vote not found for the project'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

# Get Validator's vote history
@api_view(['GET'])
def get_validator_vote_history(request, validator_address):
    try:
        # Check if validator exists
        if not Validator.objects.filter(validator_address=validator_address).exists():
            return JsonResponse({'status': 'error', 'message': 'Validator not found'})
        
        # Get the vote history for the validator
        vote_history_list = vote_history.objects.filter(validator_address=validator_address)
        
        data = []
        for vote in vote_history_list:
            data.append({
                'project_name': vote.project.name,
                'vote_result': vote.vote_result,
                'vote_date': vote.vote_date
            })
        
        return JsonResponse({'status': 'success', 'data': data})
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

# Get Validator's vote count
@api_view(['GET'])
def get_validator_vote_count(request, validator_address):
    try:
        # Check if validator exists
        if not Validator.objects.filter(validator_address=validator_address).exists():
            return JsonResponse({'status': 'error', 'message': 'Validator not found'})
        
        # Get the vote count for the validator
        vote_count = vote_history.objects.filter(validator_address=validator_address).count()
        
        return JsonResponse({'status': 'success', 'data': vote_count})
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

# Get Validator's reputation score
@api_view(['GET'])
def get_validator_reputation_score(request, validator_address):
    try:
        # Check if validator exists
        if not Validator.objects.filter(validator_address=validator_address).exists():
            return JsonResponse({'status': 'error', 'message': 'Validator not found'})
        
        # Get the reputation score for the validator
        reputation_score = Validator.objects.get(validator_address=validator_address).reputation_score
        
        return JsonResponse({'status': 'success', 'data': reputation_score})
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    
# # Calculate vote for project
# def summary_vote():
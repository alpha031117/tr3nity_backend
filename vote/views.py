from django.shortcuts import render
from django.http import JsonResponse
from .models import Project, Vote, vote_history
from datetime import datetime

# Vote for project
def vote_project(request, project_id, validator_addrs, vote_choice):
    try:
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

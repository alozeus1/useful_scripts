import boto3
import logging

workspaces_client = boto3.client('workspaces')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        logger.info("Fetching all WorkSpaces...")
        workspaces = get_all_workspaces()
        logger.info(f"Total WorkSpaces fetched: {len(workspaces)}")
        
        for workspace in workspaces:
            workspace_id = workspace['WorkspaceId']
            logger.info(f"Removing tag from WorkSpace ID: {workspace_id}")
            remove_email_tag(workspace_id)
    except Exception as e:
        logger.error(f"Error in removing tags from workspaces: {e}")

def get_all_workspaces():
    paginator = workspaces_client.get_paginator('describe_workspaces')
    workspaces = []
    
    for page in paginator.paginate():
        for workspace in page['Workspaces']:
            workspaces.append(workspace)
            logger.info(f"Fetched WorkSpace ID: {workspace['WorkspaceId']}")
        
    return workspaces

def remove_email_tag(workspace_id):
    try:
        workspaces_client.delete_tags(
            ResourceId=workspace_id,
            TagKeys=['UserEmail']
        )
        logger.info(f"Removed 'UserEmail' tag for WorkSpace ID {workspace_id}")
    except Exception as e:
        logger.error(f"Error removing tag for WorkSpace {workspace_id}: {e}")

## Note here that in this script the tag key value is "UserEmail" you can change it to your own tag key
## You can use this script with a python lambda function or in a python environment

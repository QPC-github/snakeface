from django.conf import settings
from django.contrib import messages

from rest_framework.renderers import JSONRenderer
from ratelimit.mixins import RatelimitMixin
from django.shortcuts import get_object_or_404

from snakeface.apps.main.models import Workflow, WorkflowStatus
from snakeface.settings import cfg
from snakeface.version import __version__
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import check_user_authentication


class ServiceInfo(RatelimitMixin, APIView):
    """Return a 200 response to indicate a running service. Note that we are
    not currently including all required fields. See:
    https://ga4gh.github.io/workflow-execution-service-schemas/docs/#operation/GetServiceInfo
    """

    ratelimit_key = "ip"
    ratelimit_rate = settings.VIEW_RATE_LIMIT
    ratelimit_block = settings.VIEW_RATE_LIMIT_BLOCK
    ratelimit_method = "GET"
    renderer_classes = (JSONRenderer,)

    def get(self, request):
        print("GET /service-info")

        data = {
            "id": "snakeface",
            "status": "running",  # Extra field looked for by Snakemake
            "name": "Snakemake Workflow Interface (SnakeFace)",
            "type": {"group": "org.ga4gh", "artifact": "beacon", "version": "1.0.0"},
            "description": "This service provides an interface to interact with Snakemake.",
            "organization": {"name": "Snakemake", "url": "https://snakemake.github.io"},
            "contactUrl": cfg.HELP_CONTACT_URL,
            "documentationUrl": "https://snakemake.github.io/snakeface",
            "createdAt": "2020-12-04T12:57:19Z",
            "updatedAt": cfg.UPDATED_AT,
            "environment": cfg.ENVIRONMENT,
            "version": __version__,
            "auth_instructions_url": "",
        }

        # Must make model json serializable
        return Response(status=200, data=data)


class CreateWorkflow(RatelimitMixin, APIView):
    """Create a snakemake workflow. Given that we provide an API token, we
    expect the workflow model to already be created and simply generate a run
    for it.
    """

    ratelimit_key = "ip"
    ratelimit_rate = settings.VIEW_RATE_LIMIT
    ratelimit_block = settings.VIEW_RATE_LIMIT_BLOCK
    ratelimit_method = "GET"
    renderer_classes = (JSONRenderer,)

    def get(self, request):
        print("GET /create_workflow")

        # If the request provides an id, check for workflow
        workflow = request.GET.get("id")
        user = None

        if workflow:
            workflow = get_object_or_404(Workflow, pk=workflow)

            # Remove old statuses here
            workflow.workflowstatus_set.all().delete()

        # Does the server require authentication?
        if cfg.REQUIRE_AUTH:
            user, response_code = check_user_authentication(request)
            if not user:
                return Response(status=response_code)

            # If we have a workflow, check that user has permission to use/update
            if workflow and user not in workflow.owners.all():
                return Response(status=403)

        # If we don't have a workflow, create one
        if not workflow:

            # TODO what other metadata can snakemake pass here?
            # snakefile
            # workdir
            # snakemake_id
            # name?
            workflow = Workflow()
            if user:
                workflow.owners.add(user)
            workflow.save()

        data = {"id": workflow.id}
        return Response(status=200, data=data)


class UpdateWorkflow(RatelimitMixin, APIView):
    """Update an existing snakemake workflow. Authentication is required,
    and the workflow must exist.
    """

    ratelimit_key = "ip"
    ratelimit_rate = settings.VIEW_RATE_LIMIT
    ratelimit_block = settings.VIEW_RATE_LIMIT_BLOCK
    ratelimit_method = "POST"
    renderer_classes = (JSONRenderer,)

    def post(self, request):
        print("POST /update_workflow_status")

        # We must have an existing workflow to update
        workflow = get_object_or_404(Workflow, pk=request.POST.get("id"))

        # Does the server require authentication?
        if cfg.REQUIRE_AUTH:
            user, response_code = check_user_authentication(request)
            if not user:
                return Response(response_code)

            # If we have a workflow, check that user has permission to use/update
            if workflow and user not in workflow.owners.all():
                return Response(403)

        # Update the workflow with a new status message
        workflow_status = WorkflowStatus.objects.create(
            workflow=workflow, msg=request.POST.get("msg", {})
        )
        return Response(status=200, data={})

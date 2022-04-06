### Tekton Pipeline for deploy WebSphere Application Server Apps ###

This is a sample pipeline that can be used for deploying an application to a tWAS container and deploying it to OCP.  The pipeline will do the following:

1. Download code from a [Git](https://github.com) repository
2. Compile the code using [Maven](https://maven.apache.org)
3. Use the [Dockerfile](https://docs.docker.com/engine/reference/builder/) to build a new tWAS image and store it in the OCP [ImageStreams](https://docs.openshift.com/container-platform/4.10/openshift_images/image-streams-manage.html) repository
4. Create a [Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/), [Autoscaler](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/), [Service](https://kubernetes.io/docs/concepts/services-networking/service/) and [Route](https://docs.openshift.com/container-platform/4.10/networking/routes/route-configuration.html).	

The first 3 items are done with Tasks from the [Tekton Hub](https://hub.tekton.dev).

The [OpenShift](https://mirror.openshift.com/pub/openshift-v4/clients/oc/latest/) and [Tekton](https://github.com/tektoncd/cli/releases) CLIs are needed to run commands and setup the pipeline.

1. Login to your OCP cluster
2. Install the Tekton Pipeline
```
oc apply -f tekton/tekton-pipelines-install.yaml
```
3. Install the necessary Tekton Tasks from the Tekton Hub
```
tkn hub install task git-clone -n <project>
tkn hub install task maven -n <project>
tkn hub install task kaniko -n <project>
```
4. Add task to format the app name (make lowercase, remove spaces)
```
oc apply -f tekton/was-pipeline-task-appname.yaml 
```
5. Add the custom Task
```
oc apply -f tekton/was-pipeline-task.yaml 
```
6. Add the PersistentVolumeClaim used to share between tasks.
```
oc apply -f tekton/was-pipeline-pvc.yaml
```
7. Install the Pipeline
```
oc apply -f tekton/was-pipeline.yaml
```

To run the pipeline, a sample Pipeline Run is included
```
oc apply -f tekton/was-pipeline-run.yaml
```
---
#### Setting up a trigger ####

In a true CI/CD pipeleine developers would not be submitting a Pipeline Run with the necessary data to kick off a pipeline, they would use an EventListener that would take some inputs and start the Pipeline Run.  

1. Setup the necessary ServiceAccount and cluster secuity to receive events and act upon them
```
oc apply -f was-triggers-security.yaml
```
2. Add the Trigger Template, which is an outline of how to handle the Trigger and what to run, which is similar to the Pipeline Run
```
oc apply -f was-triggers-template.yaml
```
3. Add the necessary bindings for this specific application.  This contains information to be passed to the Trigger Template
```
oc apply -f modresorts-triggers-bindings.yaml
```
4. Add the EventListener, which will startup a Pod and service to listen to Events for the trigger.  The Pod name will be prefixed with an `el` with the name of the EventListen.  In this sample it is called `el-was-triggers-eventlistener`.  The Service is given the same name as the Pod.
```
oc apply -f was-triggers-eventlistener.yaml
```
5. Create a Route so that the Trigger can be called from outside the cluster.
```
oc apply -f was-triggers-route.yaml
```
To test the Trigger, the Route endpoint can be called with the necessary JSON parameters. 
```
ROUTE_HOST=$(oc get route el-was-triggers-listener --template='http://{{.spec.host}}')
URL=https://github.com/bpaskin/WAS-Tekton.git
curl -v -H 'X-GitHub-Event: pull_request' -H 'Content-Type: application/json' -d '{ "repository": {"clone_url": "'"${URL}"'"}, "pull_request": {"head": {"sha": "master"}} }' ${ROUTE_HOST}
```
If the request is accepted successfully the HTTP response should be either a `201 Created` or `202 Accepted`. 
